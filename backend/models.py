from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, UniqueConstraint, Boolean, Float
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
    # Freemium
    plan: Mapped[str] = mapped_column(String(20), default="trial")  # trial | free | basico | pro | vitalicio
    trial_expira: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    plan_expira: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    stripe_customer_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    stripe_subscription_id: Mapped[str | None] = mapped_column(String(200), nullable=True)


class Oposicion(Base):
    __tablename__ = "oposiciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)  # "policia-local", "bomberos"
    nombre: Mapped[str] = mapped_column(String(200))
    descripcion: Mapped[str | None] = mapped_column(String(500))
    icono: Mapped[str | None] = mapped_column(String(10))  # emoji
    activa: Mapped[bool] = mapped_column(default=True)
    orden: Mapped[int] = mapped_column(Integer, default=0)

    temas: Mapped[list["Tema"]] = relationship("Tema", back_populates="oposicion")


class Tema(Base):
    __tablename__ = "temas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    oposicion_id: Mapped[int] = mapped_column(ForeignKey("oposiciones.id"))
    numero: Mapped[int] = mapped_column(Integer)
    titulo: Mapped[str] = mapped_column(String(500))
    contenido: Mapped[str | None] = mapped_column(Text)       # texto extraído
    resumen: Mapped[str | None] = mapped_column(Text)          # resumen manual/auto
    pdf_path: Mapped[str | None] = mapped_column(String(500))  # ruta al PDF
    actualizado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    oposicion: Mapped["Oposicion"] = relationship("Oposicion", back_populates="temas")
    preguntas: Mapped[list["PreguntaTema"]] = relationship("PreguntaTema", back_populates="tema")


class PreguntaTema(Base):
    __tablename__ = "preguntas_temas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tema_id: Mapped[int] = mapped_column(ForeignKey("temas.id"))
    seccion: Mapped[str | None] = mapped_column(String(300))   # título de sección
    pregunta: Mapped[str] = mapped_column(Text)
    respuesta_correcta: Mapped[str] = mapped_column(Text)
    opcion_b: Mapped[str] = mapped_column(Text)
    opcion_c: Mapped[str] = mapped_column(Text)
    opcion_d: Mapped[str] = mapped_column(Text)

    tema: Mapped["Tema"] = relationship("Tema", back_populates="preguntas")


class ProgresoUsuario(Base):
    __tablename__ = "progreso_usuarios"
    __table_args__ = (UniqueConstraint("usuario_id", "articulo_numero"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    articulo_numero: Mapped[str] = mapped_column(String(20), index=True)
    estudiado: Mapped[bool] = mapped_column(default=False)
    nota: Mapped[str | None] = mapped_column(Text)
    actualizado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TiempoEstudio(Base):
    __tablename__ = "tiempo_estudio"
    __table_args__ = (UniqueConstraint("usuario_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    segundos_total: Mapped[int] = mapped_column(Integer, default=0)
    ultima_actualizacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    usuario: Mapped["Usuario"] = relationship("Usuario")


class TemaCompletado(Base):
    __tablename__ = "temas_completados"
    __table_args__ = (UniqueConstraint("usuario_id", "slug", "numero"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    slug: Mapped[str] = mapped_column(String(50))
    numero: Mapped[int] = mapped_column(Integer)
    completado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TiempoEstudioDiario(Base):
    __tablename__ = "tiempo_estudio_diario"
    __table_args__ = (UniqueConstraint("usuario_id", "fecha"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    fecha: Mapped[datetime] = mapped_column(DateTime)  # solo la fecha (sin hora)
    segundos: Mapped[int] = mapped_column(Integer, default=0)


class RachaDiaria(Base):
    __tablename__ = "racha_diaria"
    __table_args__ = (UniqueConstraint("usuario_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    racha_actual: Mapped[int] = mapped_column(Integer, default=1)
    racha_maxima: Mapped[int] = mapped_column(Integer, default=1)
    ultimo_dia: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    usuario: Mapped["Usuario"] = relationship("Usuario")


class TokenRecuperacion(Base):
    __tablename__ = "tokens_recuperacion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), index=True)
    token: Mapped[str] = mapped_column(String(6))
    expira: Mapped[datetime] = mapped_column(DateTime)
    usado: Mapped[bool] = mapped_column(default=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Sugerencia(Base):
    __tablename__ = "sugerencias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    texto: Mapped[str] = mapped_column(Text)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Simulacro(Base):
    __tablename__ = "simulacros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    tipo: Mapped[str] = mapped_column(String(50), default="constitucion")  # constitucion | policia-local | mixto
    total_preguntas: Mapped[int] = mapped_column(Integer, default=65)
    respondidas: Mapped[int] = mapped_column(Integer, default=0)
    correctas: Mapped[int] = mapped_column(Integer, default=0)
    incorrectas: Mapped[int] = mapped_column(Integer, default=0)
    en_blanco: Mapped[int] = mapped_column(Integer, default=0)
    puntuacion: Mapped[float | None] = mapped_column(Float, nullable=True)
    tiempo_segundos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completado: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    usuario: Mapped["Usuario"] = relationship("Usuario")
