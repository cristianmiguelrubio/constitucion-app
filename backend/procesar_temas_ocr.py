"""
Script para extraer texto de los 40 PDFs de Policía Local mediante OCR
y cargarlos en la base de datos como Temas estructurados.

Requisitos previos:
  1. Instalar Tesseract OCR (como administrador):
       winget install UB-Mannheim.TesseractOCR
  2. Instalar dependencias Python (ya instaladas):
       pip install pytesseract pymupdf pillow

Uso:
  python procesar_temas_ocr.py [--carpeta "C:/oposicion policia"] [--rango 1-40]
"""

import sys
import os
import re
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

# ── Añadir Tesseract al PATH si está en la ubicación por defecto de Windows ──
TESSERACT_DEFAULT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(TESSERACT_DEFAULT):
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_DEFAULT


def extraer_texto_pdf(ruta_pdf: str) -> str:
    """Extrae todo el texto de un PDF escaneado usando pypdfium2 + Tesseract OCR.
    pypdfium2 convierte cada página a imagen sin necesitar Poppler ni otros binarios."""
    try:
        import pypdfium2 as pdfium
        import pytesseract
    except ImportError:
        log.error("Faltan dependencias. Ejecuta: pip install pytesseract pypdfium2 pillow")
        sys.exit(1)

    log.info(f"  OCR: {Path(ruta_pdf).name} ...")
    doc = pdfium.PdfDocument(ruta_pdf)
    texto_paginas = []

    for i, page in enumerate(doc):
        bitmap = page.render(scale=200 / 72)  # 200 DPI
        img = bitmap.to_pil()

        txt = pytesseract.image_to_string(img, lang="spa", config="--psm 6")
        texto_paginas.append(txt)
        log.info(f"    Página {i+1}/{len(doc)} — {len(txt)} caracteres")

    doc.close()
    return "\n\n".join(texto_paginas)


def limpiar_texto(texto: str) -> str:
    """Limpia artefactos típicos del OCR."""
    # Eliminar líneas con solo símbolos raros
    lines = texto.split("\n")
    limpias = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            limpias.append("")
            continue
        # Descartar líneas casi vacías con símbolos OCR indeseados
        letras = sum(1 for c in stripped if c.isalpha())
        if letras / max(len(stripped), 1) < 0.3 and len(stripped) > 3:
            continue
        limpias.append(line)
    texto = "\n".join(limpias)
    # Colapsar más de 3 saltos de línea consecutivos
    texto = re.sub(r"\n{4,}", "\n\n\n", texto)
    return texto.strip()


def extraer_titulo(texto: str, numero: int) -> str:
    """Intenta detectar el título del tema desde las primeras líneas."""
    lines = [l.strip() for l in texto.split("\n") if l.strip()][:20]
    for line in lines:
        # Busca algo como "TEMA 1 - LA CONSTITUCIÓN ESPAÑOLA..."
        if re.search(r"TEMA\s*\d", line, re.IGNORECASE):
            # Tomar lo que viene después del número de tema
            titulo = re.sub(r"(?i)TEMA\s*\d+\s*[-–—.]?\s*", "", line).strip()
            if len(titulo) > 10:
                return titulo[:300]
    # Si no, usar la línea más larga de las primeras 10 como título
    candidatos = [l for l in lines[:10] if len(l) > 15 and l[0].isupper()]
    if candidatos:
        return max(candidatos, key=len)[:300]
    return f"Tema {numero}"


def cargar_en_db(numero: int, titulo: str, contenido: str, oposicion_slug: str = "policia-local"):
    """Inserta o actualiza el tema en la base de datos."""
    # Importar dentro de la función para que el script sea ejecutable
    # desde la carpeta backend (donde está database.py)
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))

    from database import SessionLocal
    from models import Oposicion, Tema

    db = SessionLocal()
    try:
        oposicion = db.query(Oposicion).filter(Oposicion.slug == oposicion_slug).first()
        if not oposicion:
            oposicion = Oposicion(
                slug=oposicion_slug,
                nombre="Policía Local",
                descripcion="Temario oficial para oposiciones a Policía Local",
                icono="👮",
                activa=True,
                orden=1,
            )
            db.add(oposicion)
            db.flush()
            log.info(f"  Oposición '{oposicion_slug}' creada")

        tema = db.query(Tema).filter(
            Tema.oposicion_id == oposicion.id,
            Tema.numero == numero,
        ).first()

        if tema:
            tema.titulo = titulo
            tema.contenido = contenido
            log.info(f"  Tema {numero} actualizado en BD")
        else:
            tema = Tema(
                oposicion_id=oposicion.id,
                numero=numero,
                titulo=titulo,
                contenido=contenido,
            )
            db.add(tema)
            log.info(f"  Tema {numero} insertado en BD")

        db.commit()
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="OCR de temas Policía Local → BD")
    parser.add_argument(
        "--carpeta",
        default=r"C:\oposicion policia",
        help="Carpeta con los PDFs (default: C:\\oposicion policia)",
    )
    parser.add_argument(
        "--rango",
        default="1-40",
        help="Rango de temas a procesar, ej: 1-10 o 5 (default: 1-40)",
    )
    parser.add_argument(
        "--solo-texto",
        action="store_true",
        help="Solo extraer texto (no cargar en BD), guarda en /temas_txt/",
    )
    args = parser.parse_args()

    # Parsear rango
    if "-" in args.rango:
        inicio, fin = map(int, args.rango.split("-"))
    else:
        inicio = fin = int(args.rango)

    carpeta = Path(args.carpeta)
    if not carpeta.exists():
        log.error(f"Carpeta no encontrada: {carpeta}")
        sys.exit(1)

    if args.solo_texto:
        out_dir = Path("temas_txt")
        out_dir.mkdir(exist_ok=True)

    errores = []
    for num in range(inicio, fin + 1):
        # Preferir TEMA-N.pdf sobre TEMA-N (1).pdf
        candidatos = [
            carpeta / f"TEMA-{num}.pdf",
            carpeta / f"TEMA-{num} (1).pdf",
        ]
        pdf = next((p for p in candidatos if p.exists()), None)
        if not pdf:
            log.warning(f"Tema {num}: PDF no encontrado en {carpeta}")
            errores.append(num)
            continue

        log.info(f"\n=== Procesando Tema {num} ({pdf.name}) ===")
        try:
            texto_raw = extraer_texto_pdf(str(pdf))
            texto = limpiar_texto(texto_raw)
            titulo = extraer_titulo(texto, num)
            log.info(f"  Título detectado: {titulo}")
            log.info(f"  Texto extraído: {len(texto)} caracteres")

            if args.solo_texto:
                out_file = out_dir / f"tema_{num:02d}.txt"
                out_file.write_text(texto, encoding="utf-8")
                log.info(f"  Guardado en {out_file}")
            else:
                cargar_en_db(num, titulo, texto)

        except Exception as e:
            log.error(f"  ERROR en tema {num}: {e}")
            errores.append(num)
            continue

    log.info(f"\n{'='*50}")
    log.info(f"Procesados: {fin - inicio + 1 - len(errores)}/{fin - inicio + 1} temas")
    if errores:
        log.warning(f"Fallaron los temas: {errores}")
    else:
        log.info("Todos los temas cargados correctamente.")


if __name__ == "__main__":
    main()
