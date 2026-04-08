"""
Genera preguntas de test automáticas para los 40 temas de Policía Local
usando el texto OCR. Al menos 10 preguntas por tema, agrupadas por sección.

Método: extrae afirmaciones clave de cada sección → la correcta es la propia
afirmación, las incorrectas son afirmaciones de otras secciones del mismo tema.

Uso:
  python generar_preguntas.py [--rango 1-40] [--min 10]
"""

import sys
import re
import random
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)
sys.path.insert(0, str(Path(__file__).parent))


# ── Parser de texto (misma lógica que el frontend) ───────────────────────────

BASURA = [
    re.compile(r'^GRUPO\s+\d+', re.I),
    re.compile(r'^TEMA\s+\d+\s*$', re.I),
    re.compile(r'^\d+\s*$'),
    re.compile(r'^[-–—=•]{2,}\s*$'),
]

def es_basura(l):
    if not l or len(l) < 6:
        return True
    for p in BASURA:
        if p.match(l):
            return True
    letras = sum(1 for c in l if c.isalpha())
    return letras / len(l) < 0.45 or letras < 5

def es_titulo(l):
    if len(l) < 5 or len(l) > 110:
        return False
    letras = re.sub(r'[^a-záéíóúñüA-ZÁÉÍÓÚÑÜ]', '', l)
    if len(letras) < 4:
        return False
    mayus = sum(1 for c in l if c in 'AÁEÉIÍOÓUÚÑÜ')
    return mayus / max(len(letras), 1) > 0.7

def es_vineta(l):
    return bool(re.match(r'^[=•\-–*]\s+\S', l) or re.match(r'^e\s+[A-ZÁÉÍÓÚÑÜ]', l))

def limpiar_vineta(l):
    return re.sub(r'^[=•\-–*e]\s+', '', l).strip()

def es_item(l):
    return bool(re.match(r'^[a-z]\)\s+', l, re.I) or re.match(r'^\d+[\.\-–)]\s+[A-Za-záéíóúñ]', l))


def parsear_secciones(texto):
    """Devuelve lista de (titulo_seccion, [frases_utiles])."""
    secciones = []
    seccion_actual = {'titulo': None, 'frases': []}

    for linea in texto.split('\n'):
        l = linea.strip()
        if not l or es_basura(l):
            continue
        if es_titulo(l):
            if seccion_actual['frases']:
                secciones.append(seccion_actual)
            seccion_actual = {'titulo': l.title(), 'frases': []}
            continue
        if es_vineta(l):
            frase = limpiar_vineta(l)
        elif es_item(l):
            frase = l
        else:
            frase = l

        # Solo frases con contenido real (>40 chars, terminan en punto o son listas)
        if len(frase) >= 40:
            seccion_actual['frases'].append(frase)

    if seccion_actual['frases']:
        secciones.append(seccion_actual)

    return secciones


# ── Generador de preguntas ────────────────────────────────────────────────────

PLANTILLAS = [
    "¿Cuál de las siguientes afirmaciones es CORRECTA?",
    "Señala la opción CORRECTA:",
    "¿Cuál de las siguientes opciones es VERDADERA?",
    "Indica la afirmación CORRECTA:",
    "¿Qué afirmación es CORRECTA según el temario?",
]

def generar_preguntas_tema(secciones, min_preguntas=10):
    """
    Por cada sección selecciona frases clave.
    Correcta = la frase real. Incorrectas = frases de otras secciones.
    """
    # Recopilar todas las frases por sección
    todas = []  # [(seccion_titulo, frase)]
    for s in secciones:
        for f in s['frases']:
            todas.append((s['titulo'], f))

    if len(todas) < 4:
        return []

    preguntas = []
    random.shuffle(todas)

    for titulo_sec, frase_correcta in todas:
        # Buscar 3 incorrectas de OTRAS secciones
        incorrectas = [f for (t, f) in todas if t != titulo_sec and f != frase_correcta]
        if len(incorrectas) < 3:
            incorrectas = [f for (_, f) in todas if f != frase_correcta]
        if len(incorrectas) < 3:
            continue

        ops_incorrectas = random.sample(incorrectas, 3)
        pregunta_txt = random.choice(PLANTILLAS)

        preguntas.append({
            'seccion': titulo_sec,
            'pregunta': pregunta_txt,
            'respuesta_correcta': frase_correcta,
            'opcion_b': ops_incorrectas[0],
            'opcion_c': ops_incorrectas[1],
            'opcion_d': ops_incorrectas[2],
        })

        if len(preguntas) >= max(min_preguntas, len(secciones) * 2):
            break

    # Si no llegamos al mínimo, rellena con más preguntas de las secciones que tengan frases
    if len(preguntas) < min_preguntas:
        extras = [(t, f) for (t, f) in todas if not any(p['respuesta_correcta'] == f for p in preguntas)]
        for titulo_sec, frase_correcta in extras:
            incorrectas = random.sample([f for (_, f) in todas if f != frase_correcta], min(3, len(todas) - 1))
            if len(incorrectas) < 3:
                continue
            preguntas.append({
                'seccion': titulo_sec,
                'pregunta': random.choice(PLANTILLAS),
                'respuesta_correcta': frase_correcta,
                'opcion_b': incorrectas[0],
                'opcion_c': incorrectas[1],
                'opcion_d': incorrectas[2],
            })
            if len(preguntas) >= min_preguntas:
                break

    return preguntas


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rango', default='1-40')
    parser.add_argument('--min', type=int, default=10, dest='min_preguntas')
    args = parser.parse_args()

    if '-' in args.rango:
        inicio, fin = map(int, args.rango.split('-'))
    else:
        inicio = fin = int(args.rango)

    from database import SessionLocal, init_db
    from models import Tema, Oposicion, PreguntaTema

    init_db()  # crea columna seccion si no existe en tabla nueva
    db = SessionLocal()
    errores = []

    try:
        for num in range(inicio, fin + 1):
            tema = (
                db.query(Tema).join(Oposicion)
                .filter(Oposicion.slug == 'policia-local', Tema.numero == num)
                .first()
            )
            if not tema or not tema.contenido:
                log.warning(f"Tema {num}: sin contenido")
                errores.append(num)
                continue

            # Borrar preguntas anteriores de este tema
            db.query(PreguntaTema).filter(PreguntaTema.tema_id == tema.id).delete()

            secciones = parsear_secciones(tema.contenido)
            preguntas = generar_preguntas_tema(secciones, args.min_preguntas)

            if not preguntas:
                log.warning(f"Tema {num}: no se generaron preguntas")
                errores.append(num)
                continue

            for p in preguntas:
                db.add(PreguntaTema(
                    tema_id=tema.id,
                    seccion=p['seccion'],
                    pregunta=p['pregunta'],
                    respuesta_correcta=p['respuesta_correcta'],
                    opcion_b=p['opcion_b'],
                    opcion_c=p['opcion_c'],
                    opcion_d=p['opcion_d'],
                ))

            db.commit()
            log.info(f"Tema {num}: {len(preguntas)} preguntas generadas ({len(secciones)} secciones)")

    finally:
        db.close()

    log.info(f"\n{'='*50}")
    total = fin - inicio + 1
    log.info(f"Procesados: {total - len(errores)}/{total} temas")
    if errores:
        log.warning(f"Fallaron: {errores}")


if __name__ == '__main__':
    main()
