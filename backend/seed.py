"""
Script de carga inicial de la Constitución.
Intenta primero el scraper del BOE. Si falla, usa los datos hardcoded.
Ejecutar: python seed.py
"""
import sys
import logging
from database import init_db, SessionLocal
from models import Articulo
from seed_data import CONSTITUCION

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def cargar_desde_seed_data(db) -> int:
    """Carga los artículos desde seed_data.py."""
    for datos in CONSTITUCION:
        existente = db.query(Articulo).filter(Articulo.numero == datos["numero"]).first()
        if existente:
            # Actualizar si el contenido cambió
            if existente.contenido != datos["contenido"]:
                existente.contenido = datos["contenido"]
                existente.titulo = datos.get("titulo")
                existente.titulo_titulo = datos.get("titulo_titulo")
                existente.titulo_capitulo = datos.get("titulo_capitulo")
                existente.titulo_seccion = datos.get("titulo_seccion")
        else:
            db.add(Articulo(**datos))
    db.commit()
    return db.query(Articulo).count()


def cargar_desde_boe(db) -> int:
    """Intenta cargar desde el BOE."""
    from scraper import scrape_constitucion
    articulos = scrape_constitucion()
    if len(articulos) < 50:  # Sanity check
        raise ValueError(f"Demasiados pocos artículos obtenidos del BOE: {len(articulos)}")
    for datos in articulos:
        existente = db.query(Articulo).filter(Articulo.numero == datos["numero"]).first()
        if not existente:
            db.add(Articulo(**datos))
    db.commit()
    return db.query(Articulo).count()


def main():
    init_db()
    db = SessionLocal()
    try:
        count = db.query(Articulo).count()
        if count > 0 and "--forzar" not in sys.argv:
            logger.info(f"DB ya tiene {count} artículos. Usa --forzar para recargar.")
            return

        if "--solo-seed" not in sys.argv:
            logger.info("Intentando cargar desde el BOE...")
            try:
                total = cargar_desde_boe(db)
                logger.info(f"✓ Cargados {total} artículos desde BOE")
                return
            except Exception as e:
                logger.warning(f"BOE no disponible ({e}). Usando datos locales.")

        logger.info("Cargando datos locales (seed_data.py)...")
        total = cargar_desde_seed_data(db)
        logger.info(f"✓ Cargados {total} artículos desde seed_data")

    finally:
        db.close()


if __name__ == "__main__":
    main()
