"""
Comprueba el BOE cada día a las 9:00 para detectar cambios en la Constitución.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logger = logging.getLogger(__name__)
_scheduler = BackgroundScheduler()


def ejecutar_comprobacion_boe():
    from database import SessionLocal
    from models import Articulo, Cambio
    from scraper import check_boe_actualizaciones, scrape_constitucion
    from datetime import datetime

    logger.info("Comprobando BOE para actualizaciones...")
    db = SessionLocal()
    try:
        entradas = check_boe_actualizaciones()
        if not entradas:
            logger.info("Sin cambios en la Constitución hoy.")
            return

        logger.info(f"Detectadas {len(entradas)} entradas relevantes en BOE")

        # Re-scrapear la Constitución completa y comparar
        nuevos = scrape_constitucion()
        for datos in nuevos:
            art = db.query(Articulo).filter(Articulo.numero == datos["numero"]).first()
            if art and art.contenido != datos["contenido"]:
                # Registrar cambio
                cambio = Cambio(
                    articulo_id=art.id,
                    contenido_anterior=art.contenido,
                    contenido_nuevo=datos["contenido"],
                    descripcion=f"Actualización detectada en BOE: {', '.join(e['titulo'] for e in entradas[:2])}",
                    boe_referencia=entradas[0]["id"] if entradas else None,
                    fecha=datetime.utcnow(),
                )
                db.add(cambio)
                art.contenido = datos["contenido"]
                art.actualizado_en = datetime.utcnow()
                logger.info(f"Artículo {art.numero} actualizado")

        db.commit()
    except Exception as e:
        logger.error(f"Error en comprobación BOE: {e}")
        db.rollback()
    finally:
        db.close()


def iniciar_scheduler():
    _scheduler.add_job(
        ejecutar_comprobacion_boe,
        CronTrigger(hour=9, minute=0),
        id="boe_check",
        replace_existing=True,
    )
    _scheduler.start()
    logger.info("Scheduler iniciado - comprobación BOE diaria a las 9:00")
