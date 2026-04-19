import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Usa PostgreSQL en producción (Railway pone DATABASE_URL automáticamente)
# Si no hay DATABASE_URL, usa SQLite local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./constitucion.db")

# Railway usa postgres:// pero SQLAlchemy necesita postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from models import (  # noqa: F401
        Articulo, Cambio, Usuario, ProgresoUsuario, Oposicion, Tema,
        PreguntaTema, TiempoEstudio, TiempoEstudioDiario, Sugerencia,
        TokenRecuperacion, RachaDiaria, TemaCompletado, Simulacro, PushSuscripcion,
    )
    Base.metadata.create_all(bind=engine)
