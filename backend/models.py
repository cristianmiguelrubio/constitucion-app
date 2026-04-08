from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Articulo(Base):
    __tablename__ = "articulos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    titulo: Mapped[str | None] = mapped_column(String(500))
    contenido: Mapped[str] = mapped_column(Text)
    titulo_seccion: Mapped[str | None] = mapped_column(String(300))
    titulo_capitulo: Mapped[str | None] = mapped_column(String(300))
    titulo_titulo: Mapped[str | None] = mapped_column(String(300))
    actualizado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    cambios: Mapped[list["Cambio"]] = relationship("Cambio", back_populates="articulo")


class Cambio(Base):
    __tablename__ = "cambios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    articulo_id: Mapped[int] = mapped_column(ForeignKey("articulos.id"))
    contenido_anterior: Mapped[str] = mapped_column(Text)
    contenido_nuevo: Mapped[str] = mapped_column(Text)
    descripcion: Mapped[str | None] = mapped_column(String(500))
    boe_referencia: Mapped[str | None] = mapped_column(String(200))
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    articulo: Mapped["Articulo"] = relationship("Articulo", back_populates="cambios")


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    nombre: Mapped[str | None] = mapped_column(String(200))
    password_hash: Mapped[str] = mapped_column(String(255))
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ultima_visita: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    visitas: Mapped[int] = mapped_column(Integer, default=1)


class ProgresoUsuario(Base):
    __tablename__ = "progreso_usuarios"
    __table_args__ = (UniqueConstraint("usuario_id", "articulo_numero"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    articulo_numero: Mapped[str] = mapped_column(String(20), index=True)
    estudiado: Mapped[bool] = mapped_column(default=False)
    nota: Mapped[str | None] = mapped_column(Text)
    actualizado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
