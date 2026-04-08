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


def limpiar_para_resumen(texto: str) -> str:
    """Quita ruido OCR antes de resumir."""
    lineas = []
    for linea in texto.split('\n'):
        l = linea.strip()
        if not l:
            continue
        # Descartar líneas de cabecera de página
        if re.match(r'^GRUPO\s+\d+', l, re.I):
            continue
        # Descartar líneas con muy pocas letras
        letras = sum(1 for c in l if c.isalpha())
        if letras < 4:
            continue
        lineas.append(l)
    return ' '.join(lineas)


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

    frases = summarizer(parser.document, num_frases)
    # Eliminar duplicados manteniendo orden
    vistas = set()
    unicas = []
    for f in frases:
        txt = str(f).strip()
        clave = txt[:80]
        if clave not in vistas:
            vistas.add(clave)
            unicas.append(txt)

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
