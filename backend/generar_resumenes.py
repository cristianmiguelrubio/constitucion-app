"""
Genera resúmenes automáticos (TextRank) para todos los temas de Policía Local
y los guarda en el campo `resumen` de la tabla temas.

Uso:
  python generar_resumenes.py [--rango 1-40] [--frases 7]
"""

import sys
import re
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).parent))


def es_ruido(linea: str) -> bool:
    """Detecta líneas con demasiado ruido OCR para no incluirlas en el resumen."""
    l = linea.strip()
    if not l or len(l) < 8:
        return True
    # Cabeceras de página
    if re.match(r'^GRUPO\s+\d+', l, re.I):
        return True
    # Viñetas OCR sueltas (e Título, e Capítulo...)
    if re.match(r'^e\s+[A-ZÁÉÍÓÚÑÜ]', l):
        return True
    # Líneas con símbolo % que debería ser º/° (artefacto OCR)
    if l.count('%') >= 2:
        return True
    # Líneas que empiezan por = (viñeta OCR)
    if l.startswith('=') or l.startswith('e Cap') or l.startswith('e T'):
        return True
    # Ratio de letras muy bajo
    letras = sum(1 for c in l if c.isalpha())
    if letras < 6 or letras / len(l) < 0.45:
        return True
    return False


def limpiar_para_resumen(texto: str) -> str:
    """Quita ruido OCR antes de resumir."""
    lineas = []
    for linea in texto.split('\n'):
        if not es_ruido(linea):
            lineas.append(linea.strip())
    return ' '.join(lineas)


def es_frase_valida(frase: str) -> bool:
    """Descarta frases del resumen que aún contengan ruido OCR."""
    f = frase.strip()
    if re.match(r'^e\s+[A-ZÁÉÍÓÚÑÜ]', f):
        return False
    if f.count('%') >= 2:
        return False
    if f.startswith('=') or f.startswith('e Cap') or f.startswith('e T'):
        return False
    letras = sum(1 for c in f if c.isalpha())
    if letras < 20 or letras / max(len(f), 1) < 0.45:
        return False
    return True


def resumir(texto: str, num_frases: int = 7) -> str:
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.text_rank import TextRankSummarizer
    from sumy.nlp.stemmers import Stemmer
    from sumy.utils import get_stop_words

    texto_limpio = limpiar_para_resumen(texto)
    if len(texto_limpio) < 200:
        return texto_limpio

    parser = PlaintextParser.from_string(texto_limpio, Tokenizer('spanish'))
    stemmer = Stemmer('spanish')
    summarizer = TextRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words('spanish')

    # Pedir más frases para poder filtrar las malas y quedarnos con las buenas
    frases_raw = summarizer(parser.document, num_frases + 5)
    vistas = set()
    unicas = []
    for f in frases_raw:
        txt = str(f).strip()
        if not es_frase_valida(txt):
            continue
        clave = txt[:80]
        if clave not in vistas:
            vistas.add(clave)
            unicas.append(txt)
        if len(unicas) >= num_frases:
            break

    return '\n\n'.join(unicas)


def main():
    parser = argparse.ArgumentParser(description="Genera resúmenes TextRank para temas de Policía Local")
    parser.add_argument('--rango', default='1-40')
    parser.add_argument('--frases', type=int, default=7, help='Número de frases en el resumen')
    args = parser.parse_args()

    if '-' in args.rango:
        inicio, fin = map(int, args.rango.split('-'))
    else:
        inicio = fin = int(args.rango)

    from database import SessionLocal
    from models import Tema, Oposicion

    db = SessionLocal()
    errores = []

    try:
        for num in range(inicio, fin + 1):
            tema = (
                db.query(Tema)
                .join(Oposicion)
                .filter(Oposicion.slug == 'policia-local', Tema.numero == num)
                .first()
            )
            if not tema:
                log.warning(f"Tema {num} no encontrado en BD")
                errores.append(num)
                continue
            if not tema.contenido:
                log.warning(f"Tema {num} sin contenido")
                errores.append(num)
                continue

            log.info(f"Resumiendo tema {num}: {tema.titulo[:60]}...")
            try:
                resumen = resumir(tema.contenido, args.frases)
                tema.resumen = resumen
                db.commit()
                log.info(f"  → {len(resumen)} caracteres guardados")
            except Exception as e:
                log.error(f"  ERROR tema {num}: {e}")
                db.rollback()
                errores.append(num)

    finally:
        db.close()

    log.info(f"\n{'='*50}")
    total = fin - inicio + 1
    log.info(f"Resumidos: {total - len(errores)}/{total} temas")
    if errores:
        log.warning(f"Fallaron: {errores}")


if __name__ == '__main__':
    main()
