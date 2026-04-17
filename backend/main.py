from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
from pydantic import BaseModel
import logging
import random
import os

from database import get_db, init_db
from models import Articulo, Cambio, Usuario, ProgresoUsuario, Oposicion, Tema, PreguntaTema, TiempoEstudio, TiempoEstudioDiario, Sugerencia, TokenRecuperacion, RachaDiaria, TemaCompletado, Simulacro, PushSuscripcion
from scraper import scrape_constitucion, check_boe_actualizaciones
from scheduler import iniciar_scheduler
from seed_data import QUIZ_PREGUNTAS
from auth import hash_password, verify_password, crear_token, get_current_user, verificar_token
from email_utils import ADMIN_EMAIL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_usuario_or_401(uid: int, db: Session) -> "Usuario":
    u = db.query(Usuario).filter(Usuario.id == uid).first()
    if not u:
        raise HTTPException(status_code=401, detail="Sesión expirada")
    return u


PLANES_PREMIUM = {"basico", "pro", "vitalicio"}

def tiene_acceso_premium(usuario: "Usuario") -> bool:
    """Devuelve True si el usuario tiene acceso premium activo (trial, plan de pago, o vitalicio)."""
    if usuario.plan == "vitalicio":
        return True
    if usuario.plan == "trial":
        if usuario.trial_expira and datetime.utcnow() < usuario.trial_expira:
            return True
        return False
    if usuario.plan in PLANES_PREMIUM:
        if usuario.plan_expira is None or datetime.utcnow() < usuario.plan_expira:
            return True
    return False

def es_admin(current_user: dict, db: Session) -> bool:
    uid = int(current_user["sub"])
    if uid == 1:
        return True
    usuario = db.query(Usuario).filter(Usuario.id == uid).first()
    return usuario is not None and usuario.email == ADMIN_EMAIL

# Rutas públicas que no requieren token
RUTAS_PUBLICAS = {"/api/auth/login", "/api/auth/registro", "/api/auth/recuperar", "/api/auth/reset", "/api/ranking", "/api/version", "/api/planes", "/api/push/vapid-key", "/api/stripe/webhook"}

app = FastAPI(title="Constitución App", version="1.0.0", docs_url=None, redoc_url=None)

# CORS restringido al dominio propio
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:8000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        # Solo proteger rutas /api/ que no sean públicas
        if path.startswith("/api/") and path not in RUTAS_PUBLICAS:
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return JSONResponse(status_code=401, content={"detail": "No autenticado"})
            try:
                verificar_token(auth.split(" ", 1)[1])
            except HTTPException as e:
                return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        return await call_next(request)


app.add_middleware(AuthMiddleware)


@app.on_event("startup")
async def startup():
    init_db()
    iniciar_scheduler()
    db = next(get_db())
    # Migrar columnas nuevas en PostgreSQL si no existen
    try:
        from sqlalchemy import text
        migraciones = [
            "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS plan VARCHAR(20) DEFAULT 'free'",
            "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS trial_expira TIMESTAMP",
            "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS plan_expira TIMESTAMP",
            "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR(200)",
            "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS stripe_subscription_id VARCHAR(200)",
            "ALTER TABLE push_suscripciones ADD COLUMN IF NOT EXISTS id SERIAL",
        ]
        for sql in migraciones:
            try:
                db.execute(text(sql))
            except Exception:
                pass
        # Crear tabla push_suscripciones si no existe (init_db la crea, pero por si acaso)
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS push_suscripciones (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER REFERENCES usuarios(id),
                endpoint TEXT NOT NULL,
                p256dh TEXT NOT NULL,
                auth TEXT NOT NULL,
                creado_en TIMESTAMP DEFAULT NOW(),
                UNIQUE(usuario_id, endpoint)
            )
        """))
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS simulacros (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER REFERENCES usuarios(id),
                tipo VARCHAR(50) DEFAULT 'constitucion',
                total_preguntas INTEGER DEFAULT 65,
                respondidas INTEGER DEFAULT 0,
                correctas INTEGER DEFAULT 0,
                incorrectas INTEGER DEFAULT 0,
                en_blanco INTEGER DEFAULT 0,
                puntuacion FLOAT,
                tiempo_segundos INTEGER,
                completado BOOLEAN DEFAULT FALSE,
                fecha TIMESTAMP DEFAULT NOW()
            )
        """))
        db.execute(text("UPDATE usuarios SET plan='free' WHERE plan IS NULL"))
        db.commit()
        logger.info("Migración DB OK")
    except Exception as e:
        logger.warning(f"Migración DB: {e}")
        db.rollback()
    try:
        count = db.query(Articulo).count()
        if count == 0:
            logger.info("DB vacía, cargando desde seed_data...")
            from seed import cargar_desde_seed_data
            cargar_desde_seed_data(db)
            try:
                _cargar_constitucion(db)
            except Exception as e:
                logger.warning(f"BOE no disponible en startup: {e}. Usando seed_data.")

        # Cargar temas de Policía Local si no existen
        try:
            from seed_temas import TEMAS_POLICIA_LOCAL
            count_temas = db.query(Tema).count()
            count_preguntas = db.query(PreguntaTema).count()
            if count_temas == 0:
                _cargar_temas_policia(db, TEMAS_POLICIA_LOCAL)
            elif count_preguntas == 0:
                # Temas ya cargados pero sin preguntas — cargar solo las preguntas
                logger.info("Cargando preguntas de temas existentes...")
                _cargar_preguntas_temas(db, TEMAS_POLICIA_LOCAL)
        except ImportError:
            logger.info("seed_temas.py no encontrado — temas se cargarán manualmente")
        except Exception as e:
            logger.warning(f"Error cargando temas: {e}")
        # Cargar temas de Guardia Civil si no existen
        try:
            from seed_temas_gc import TEMAS_GUARDIA_CIVIL
            op_gc = db.query(Oposicion).filter(Oposicion.slug == "guardia-civil").first()
            if op_gc is None or db.query(Tema).filter(Tema.oposicion_id == (op_gc.id if op_gc else -1)).count() == 0:
                _cargar_temas_gc(db, TEMAS_GUARDIA_CIVIL)
        except ImportError:
            logger.info("seed_temas_gc.py no encontrado — temas GC se cargarán manualmente")
        except Exception as e:
            logger.warning(f"Error cargando temas Guardia Civil: {e}")
        # Cargar oposiciones base si no existen
        _cargar_oposiciones_base(db)
    finally:
        db.close()


def _cargar_temas_policia(db: Session, temas: list):
    op = db.query(Oposicion).filter(Oposicion.slug == "policia-local").first()
    if not op:
        op = Oposicion(
            slug="policia-local", nombre="Policía Local",
            descripcion="Temario oficial para oposiciones a Policía Local",
            icono="👮", activa=True, orden=1,
        )
        db.add(op)
        db.flush()
    for t in temas:
        existe = db.query(Tema).filter(Tema.oposicion_id == op.id, Tema.numero == t["numero"]).first()
        if not existe:
            nuevo = Tema(
                oposicion_id=op.id,
                numero=t["numero"],
                titulo=t["titulo"],
                contenido=t["contenido"],
                resumen=t.get("resumen"),
            )
            db.add(nuevo)
            db.flush()
            for p in t.get("preguntas", []):
                db.add(PreguntaTema(
                    tema_id=nuevo.id,
                    seccion=p.get("seccion"),
                    pregunta=p["pregunta"],
                    respuesta_correcta=p["respuesta_correcta"],
                    opcion_b=p["opcion_b"],
                    opcion_c=p["opcion_c"],
                    opcion_d=p["opcion_d"],
                ))
    db.commit()
    logger.info(f"Cargados {len(temas)} temas de Policía Local")


def _cargar_preguntas_temas(db: Session, temas: list):
    op = db.query(Oposicion).filter(Oposicion.slug == "policia-local").first()
    if not op:
        return
    total = 0
    for t in temas:
        tema = db.query(Tema).filter(Tema.oposicion_id == op.id, Tema.numero == t["numero"]).first()
        if not tema:
            continue
        for p in t.get("preguntas", []):
            db.add(PreguntaTema(
                tema_id=tema.id,
                seccion=p.get("seccion"),
                pregunta=p["pregunta"],
                respuesta_correcta=p["respuesta_correcta"],
                opcion_b=p["opcion_b"],
                opcion_c=p["opcion_c"],
                opcion_d=p["opcion_d"],
            ))
            total += 1
    db.commit()
    logger.info(f"Cargadas {total} preguntas en temas existentes")


def _cargar_temas_gc(db: Session, temas: list):
    op = db.query(Oposicion).filter(Oposicion.slug == "guardia-civil").first()
    if not op:
        op = Oposicion(
            slug="guardia-civil", nombre="Guardia Civil",
            descripcion="Temario oficial para oposiciones a la Guardia Civil",
            icono="⭐", activa=True, orden=3,
        )
        db.add(op)
        db.flush()
    for t in temas:
        existe = db.query(Tema).filter(Tema.oposicion_id == op.id, Tema.numero == t["numero"]).first()
        if not existe:
            nuevo = Tema(
                oposicion_id=op.id,
                numero=t["numero"],
                titulo=t["titulo"],
                contenido=t["contenido"],
                resumen=t.get("resumen"),
            )
            db.add(nuevo)
            db.flush()
            for p in t.get("preguntas", []):
                db.add(PreguntaTema(
                    tema_id=nuevo.id,
                    seccion=p.get("seccion"),
                    pregunta=p["pregunta"],
                    respuesta_correcta=p["respuesta_correcta"],
                    opcion_b=p["opcion_b"],
                    opcion_c=p["opcion_c"],
                    opcion_d=p["opcion_d"],
                ))
    db.commit()
    logger.info(f"Cargados {len(temas)} temas de Guardia Civil")


OPOSICIONES_BASE = [
    {"slug": "policia-local",    "nombre": "Policía Local",    "icono": "👮", "orden": 1, "descripcion": "Oposición a Policía Local"},
    {"slug": "policia-nacional", "nombre": "Policía Nacional", "icono": "🛡️", "orden": 2, "descripcion": "Oposición a Policía Nacional del Estado"},
    {"slug": "guardia-civil",    "nombre": "Guardia Civil",    "icono": "⭐", "orden": 3, "descripcion": "Oposición a la Guardia Civil"},
    {"slug": "correos",          "nombre": "Correos",          "icono": "📮", "orden": 4, "descripcion": "Oposición a Correos y Telégrafos"},
    {"slug": "bomberos",         "nombre": "Bomberos",         "icono": "🚒", "orden": 5, "descripcion": "Oposición a Bombero"},
]

def _cargar_oposiciones_base(db: Session):
    for op in OPOSICIONES_BASE:
        existe = db.query(Oposicion).filter(Oposicion.slug == op["slug"]).first()
        if not existe:
            db.add(Oposicion(**op, activa=True))
    try:
        db.commit()
    except Exception:
        db.rollback()


def _cargar_constitucion(db: Session):
    try:
        articulos = scrape_constitucion()
        for datos in articulos:
            existente = db.query(Articulo).filter(Articulo.numero == datos["numero"]).first()
            if not existente:
                db.add(Articulo(**datos))
        db.commit()
        logger.info(f"Cargados artículos del BOE en DB")
    except Exception as e:
        logger.error(f"Error cargando Constitución: {e}")
        db.rollback()


# ── Pydantic schemas ────────────────────────────────────────────────────────

class RegistroRequest(BaseModel):
    email: str
    password: str
    nombre: str | None = None

class LoginRequest(BaseModel):
    email: str
    password: str

class ProgresoRequest(BaseModel):
    articulo_numero: str
    estudiado: bool = False
    nota: str | None = None


# ── Auth ────────────────────────────────────────────────────────────────────

@app.post("/api/auth/registro")
def registro(data: RegistroRequest, db: Session = Depends(get_db)):
    email = data.email.strip().lower()
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Email no válido")
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres")

    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(status_code=409, detail="Este email ya está registrado")

    usuario = Usuario(
        email=email,
        nombre=data.nombre,
        password_hash=hash_password(data.password),
        plan="trial",
        trial_expira=datetime.utcnow() + timedelta(hours=24),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    token = crear_token(usuario.id, usuario.email)
    # Enviar push de bienvenida si tiene suscripción (registro desde PWA)
    try:
        subs = db.query(PushSuscripcion).filter(PushSuscripcion.usuario_id == usuario.id).all()
        for s in subs:
            enviar_push(s, "¡Bienvenido! 🎉", "Tienes 24 horas de acceso gratuito completo.", "/planes")
    except Exception:
        pass
    return {
        "token": token, "email": usuario.email, "nombre": usuario.nombre,
        "plan": usuario.plan, "trial_expira": usuario.trial_expira.isoformat() if usuario.trial_expira else None,
    }


@app.post("/api/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    email = data.email.strip().lower()
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario or not verify_password(data.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    usuario.ultima_visita = datetime.utcnow()
    usuario.visitas += 1
    db.commit()

    token = crear_token(usuario.id, usuario.email)
    return {
        "token": token, "email": usuario.email, "nombre": usuario.nombre,
        "plan": usuario.plan, "trial_expira": usuario.trial_expira.isoformat() if usuario.trial_expira else None,
        "plan_expira": usuario.plan_expira.isoformat() if usuario.plan_expira else None,
        "premium": tiene_acceso_premium(usuario),
    }


# ── Recuperación de contraseña ──────────────────────────────────────────────

class RecuperarIn(BaseModel):
    email: str

class ResetIn(BaseModel):
    email: str
    codigo: str
    nueva_password: str

@app.post("/api/auth/recuperar")
def solicitar_recuperacion(data: RecuperarIn, db: Session = Depends(get_db)):
    from datetime import timedelta
    import random as _random

    email = data.email.strip().lower()
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    # Siempre devolver OK para no revelar si el email existe
    if not usuario:
        return {"ok": True, "dev_codigo": None}

    # Invalidar tokens anteriores
    db.query(TokenRecuperacion).filter(
        TokenRecuperacion.email == email, TokenRecuperacion.usado == False
    ).update({"usado": True})

    codigo = str(_random.randint(100000, 999999))
    expira = datetime.utcnow() + timedelta(minutes=15)
    db.add(TokenRecuperacion(email=email, token=codigo, expira=expira))
    db.commit()

    # Mostrar siempre el código en pantalla
    return {"ok": True, "dev_codigo": codigo}


@app.post("/api/auth/reset")
def resetear_password(data: ResetIn, db: Session = Depends(get_db)):
    email = data.email.strip().lower()
    if len(data.nueva_password) < 6:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres")

    token = db.query(TokenRecuperacion).filter(
        TokenRecuperacion.email == email,
        TokenRecuperacion.token == data.codigo,
        TokenRecuperacion.usado == False,
        TokenRecuperacion.expira > datetime.utcnow(),
    ).first()

    if not token:
        raise HTTPException(status_code=400, detail="Código incorrecto o caducado")

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404)

    usuario.password_hash = hash_password(data.nueva_password)
    token.usado = True
    db.commit()

    jwt_token = crear_token(usuario.id, usuario.email)
    return {"ok": True, "token": jwt_token, "email": usuario.email, "nombre": usuario.nombre}


# ── Progreso (requiere auth) ────────────────────────────────────────────────

@app.get("/api/progreso")
def obtener_progreso(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    usuario_id = int(current_user["sub"])
    registros = db.query(ProgresoUsuario).filter(
        ProgresoUsuario.usuario_id == usuario_id
    ).all()
    return {
        "estudiados": {r.articulo_numero: r.estudiado for r in registros},
        "notas": {r.articulo_numero: r.nota for r in registros if r.nota},
    }


@app.post("/api/progreso")
def guardar_progreso(
    data: ProgresoRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    usuario_id = int(current_user["sub"])
    registro = db.query(ProgresoUsuario).filter(
        ProgresoUsuario.usuario_id == usuario_id,
        ProgresoUsuario.articulo_numero == data.articulo_numero,
    ).first()

    if registro:
        registro.estudiado = data.estudiado
        registro.nota = data.nota
        registro.actualizado_en = datetime.utcnow()
    else:
        db.add(ProgresoUsuario(
            usuario_id=usuario_id,
            articulo_numero=data.articulo_numero,
            estudiado=data.estudiado,
            nota=data.nota,
        ))
    db.commit()
    return {"ok": True}


@app.get("/api/temas-completados")
def obtener_temas_completados(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    registros = db.query(TemaCompletado).filter(TemaCompletado.usuario_id == uid).all()
    return [{"slug": r.slug, "numero": r.numero} for r in registros]


@app.post("/api/temas-completados")
def marcar_tema_completado(
    slug: str, numero: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    uid = int(current_user["sub"])
    existe = db.query(TemaCompletado).filter(
        TemaCompletado.usuario_id == uid,
        TemaCompletado.slug == slug,
        TemaCompletado.numero == numero,
    ).first()
    if not existe:
        db.add(TemaCompletado(usuario_id=uid, slug=slug, numero=numero))
        db.commit()
    return {"ok": True}


@app.get("/api/admin/usuarios")
def listar_usuarios(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not es_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Acceso denegado")
    usuarios = db.query(Usuario).order_by(Usuario.fecha_registro.desc()).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "nombre": u.nombre,
            "fecha_registro": u.fecha_registro.isoformat(),
            "ultima_visita": u.ultima_visita.isoformat(),
            "visitas": u.visitas,
        }
        for u in usuarios
    ]


# ── Endpoints de contenido ──────────────────────────────────────────────────

@app.get("/api/articulos")
def listar_articulos(db: Session = Depends(get_db)):
    articulos = db.query(Articulo).order_by(Articulo.id).all()
    return [_serializar_articulo(a, breve=True) for a in articulos]


@app.get("/api/articulos/{numero}")
def obtener_articulo(numero: str, db: Session = Depends(get_db)):
    art = db.query(Articulo).filter(Articulo.numero == numero).first()
    if not art:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return _serializar_articulo(art)


@app.get("/api/buscar")
def buscar(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    termino = f"%{q}%"
    resultados = db.query(Articulo).filter(
        or_(
            Articulo.contenido.ilike(termino),
            Articulo.titulo.ilike(termino),
            Articulo.numero.ilike(termino),
        )
    ).limit(30).all()
    return [_serializar_articulo(a, breve=True) for a in resultados]


@app.get("/api/cambios")
def listar_cambios(limit: int = 20, db: Session = Depends(get_db)):
    cambios = db.query(Cambio).order_by(Cambio.fecha.desc()).limit(limit).all()
    return [
        {
            "id": c.id,
            "articulo_numero": c.articulo.numero,
            "descripcion": c.descripcion,
            "boe_referencia": c.boe_referencia,
            "fecha": c.fecha.isoformat(),
        }
        for c in cambios
    ]


@app.get("/api/estructura")
def obtener_estructura(db: Session = Depends(get_db)):
    articulos = db.query(
        Articulo.numero, Articulo.titulo,
        Articulo.titulo_titulo, Articulo.titulo_capitulo, Articulo.titulo_seccion,
    ).order_by(Articulo.id).all()

    estructura = {}
    for a in articulos:
        t = a.titulo_titulo or "Sin título"
        c = a.titulo_capitulo or ""
        s = a.titulo_seccion or ""
        if t not in estructura:
            estructura[t] = {}
        bloque = c or s or "_"
        if bloque not in estructura[t]:
            estructura[t][bloque] = []
        estructura[t][bloque].append({"numero": a.numero, "titulo": a.titulo})
    return estructura


@app.get("/api/quiz/temas")
def obtener_temas_quiz():
    """Devuelve los temas disponibles para el quiz."""
    temas = {}
    for p in QUIZ_PREGUNTAS:
        art_num = int(p["articulo"])
        if art_num <= 9:
            tema = "TÍTULO PRELIMINAR"
        elif art_num <= 55:
            tema = "TÍTULO I. Derechos y deberes"
        elif art_num <= 65:
            tema = "TÍTULO II. La Corona"
        elif art_num <= 96:
            tema = "TÍTULO III. Cortes Generales"
        elif art_num <= 107:
            tema = "TÍTULO IV. Gobierno"
        elif art_num <= 116:
            tema = "TÍTULO V. Gobierno y Cortes"
        elif art_num <= 127:
            tema = "TÍTULO VI. Poder Judicial"
        elif art_num <= 136:
            tema = "TÍTULO VII. Economía"
        elif art_num <= 158:
            tema = "TÍTULO VIII. Organización Territorial"
        elif art_num <= 165:
            tema = "TÍTULO IX. Tribunal Constitucional"
        else:
            tema = "TÍTULO X. Reforma Constitucional"
        temas[tema] = temas.get(tema, 0) + 1

    return [{"tema": k, "preguntas": v} for k, v in temas.items()]


@app.get("/api/quiz")
def obtener_preguntas(
    tema: str | None = None,
    articulo: str | None = None,
    limite: int = 10,
):
    preguntas = list(QUIZ_PREGUNTAS)

    if articulo:
        preguntas = [p for p in preguntas if p["articulo"] == articulo]
    elif tema:
        def _tema_de(num_str):
            n = int(num_str)
            if n <= 9:   return "TÍTULO PRELIMINAR"
            if n <= 55:  return "TÍTULO I. Derechos y deberes"
            if n <= 65:  return "TÍTULO II. La Corona"
            if n <= 96:  return "TÍTULO III. Cortes Generales"
            if n <= 107: return "TÍTULO IV. Gobierno"
            if n <= 116: return "TÍTULO V. Gobierno y Cortes"
            if n <= 127: return "TÍTULO VI. Poder Judicial"
            if n <= 136: return "TÍTULO VII. Economía"
            if n <= 158: return "TÍTULO VIII. Organización Territorial"
            if n <= 165: return "TÍTULO IX. Tribunal Constitucional"
            return "TÍTULO X. Reforma Constitucional"
        preguntas = [p for p in preguntas if _tema_de(p["articulo"]) == tema]

    random.shuffle(preguntas)
    resultado = []
    for p in preguntas[:limite]:
        # Normalizar: si tiene 'opciones' array, extraer opcion_b/c/d
        if 'opciones' in p and 'opcion_b' not in p:
            ops = [o for o in p['opciones'] if o != p['respuesta_correcta']]
            random.shuffle(ops)
            resultado.append({
                'articulo': p.get('articulo'),
                'seccion': p.get('seccion'),
                'pregunta': p['pregunta'],
                'respuesta_correcta': p['respuesta_correcta'],
                'opcion_b': ops[0] if len(ops) > 0 else '',
                'opcion_c': ops[1] if len(ops) > 1 else '',
                'opcion_d': ops[2] if len(ops) > 2 else '',
            })
        else:
            resultado.append(p)
    return resultado


# ── Oposiciones ────────────────────────────────────────────────────────────

@app.get("/api/oposiciones")
def listar_oposiciones(db: Session = Depends(get_db)):
    ops = db.query(Oposicion).filter(Oposicion.activa == True).order_by(Oposicion.orden).all()
    return [
        {
            "id": o.id, "slug": o.slug, "nombre": o.nombre,
            "descripcion": o.descripcion, "icono": o.icono,
            "total_temas": len(o.temas),
        }
        for o in ops
    ]


@app.get("/api/oposiciones/{slug}/temas")
def listar_temas(slug: str, db: Session = Depends(get_db)):
    op = db.query(Oposicion).filter(Oposicion.slug == slug).first()
    if not op:
        raise HTTPException(status_code=404, detail="Oposición no encontrada")
    temas = db.query(Tema).filter(Tema.oposicion_id == op.id).order_by(Tema.numero).all()
    return {
        "oposicion": {"slug": op.slug, "nombre": op.nombre, "icono": op.icono},
        "temas": [
            {
                "id": t.id, "numero": t.numero, "titulo": t.titulo,
                "tiene_pdf": t.pdf_path is not None,
                "tiene_contenido": t.contenido is not None,
                "tiene_resumen": t.resumen is not None,
                "total_preguntas": len(t.preguntas),
            }
            for t in temas
        ]
    }


@app.get("/api/oposiciones/{slug}/temas/{numero}")
def obtener_tema(slug: str, numero: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    usuario = get_usuario_or_401(uid, db)
    # Trial solo puede acceder al tema 1
    if numero > 1:
        es_trial_activo = (
            usuario.plan == "trial"
            and usuario.trial_expira is not None
            and datetime.utcnow() < usuario.trial_expira
        )
        if es_trial_activo or not tiene_acceso_premium(usuario):
            raise HTTPException(status_code=403, detail="trial_only_tema1")
    op = db.query(Oposicion).filter(Oposicion.slug == slug).first()
    if not op:
        raise HTTPException(status_code=404, detail="Oposición no encontrada")
    tema = db.query(Tema).filter(
        Tema.oposicion_id == op.id, Tema.numero == numero
    ).first()
    if not tema:
        raise HTTPException(status_code=404, detail="Tema no encontrado")
    return {
        "id": tema.id, "numero": tema.numero, "titulo": tema.titulo,
        "contenido": tema.contenido, "resumen": tema.resumen,
        "tiene_pdf": tema.pdf_path is not None,
        "total_preguntas": len(tema.preguntas),
    }


@app.get("/api/oposiciones/{slug}/temas/{numero}/pdf")
def descargar_pdf(
    slug: str, numero: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Sirve el PDF del tema — solo a usuarios autenticados."""
    op = db.query(Oposicion).filter(Oposicion.slug == slug).first()
    if not op:
        raise HTTPException(status_code=404)
    tema = db.query(Tema).filter(
        Tema.oposicion_id == op.id, Tema.numero == numero
    ).first()
    if not tema or not tema.pdf_path:
        raise HTTPException(status_code=404, detail="PDF no disponible")
    if not os.path.exists(tema.pdf_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(
        tema.pdf_path,
        media_type="application/pdf",
        filename=f"{slug}-tema-{numero}.pdf",
    )


@app.get("/api/oposiciones/{slug}/quiz")
def quiz_oposicion(slug: str, tema_id: int | None = None, limite: int = 10, db: Session = Depends(get_db)):
    op = db.query(Oposicion).filter(Oposicion.slug == slug).first()
    if not op:
        raise HTTPException(status_code=404)

    query = db.query(PreguntaTema).join(Tema).filter(Tema.oposicion_id == op.id)
    if tema_id:
        query = query.filter(PreguntaTema.tema_id == tema_id)

    preguntas = query.all()
    random.shuffle(preguntas)
    preguntas = preguntas[:limite]

    return [
        {
            "id": p.id,
            "tema_id": p.tema_id,
            "tema_numero": p.tema.numero,
            "tema_titulo": p.tema.titulo,
            "seccion": p.seccion,
            "pregunta": p.pregunta,
            "respuesta_correcta": p.respuesta_correcta,
            "opcion_b": p.opcion_b,
            "opcion_c": p.opcion_c,
            "opcion_d": p.opcion_d,
        }
        for p in preguntas
    ]


@app.get("/api/oposiciones/{slug}/temas/{numero}/quiz")
def quiz_tema(slug: str, numero: int, limite: int = 10, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    usuario = get_usuario_or_401(uid, db)
    # Trial solo puede acceder al quiz del tema 1
    if numero > 1:
        es_trial_activo = (
            usuario.plan == "trial"
            and usuario.trial_expira is not None
            and datetime.utcnow() < usuario.trial_expira
        )
        if es_trial_activo or not tiene_acceso_premium(usuario):
            raise HTTPException(status_code=403, detail="trial_only_tema1")
    op = db.query(Oposicion).filter(Oposicion.slug == slug).first()
    if not op:
        raise HTTPException(status_code=404)
    tema = db.query(Tema).filter(
        Tema.oposicion_id == op.id, Tema.numero == numero
    ).first()
    if not tema:
        raise HTTPException(status_code=404, detail="Tema no encontrado")

    preguntas = list(tema.preguntas)
    random.shuffle(preguntas)
    preguntas = preguntas[:limite]

    resultado = []
    for p in preguntas:
        opciones = [p.respuesta_correcta, p.opcion_b, p.opcion_c, p.opcion_d]
        random.shuffle(opciones)
        # La clave 'a' siempre apunta a respuesta_correcta para que el front sepa cuál es
        resultado.append({
            "id": p.id,
            "seccion": p.seccion,
            "pregunta": p.pregunta,
            "respuesta_correcta": p.respuesta_correcta,
            "opcion_b": p.opcion_b,
            "opcion_c": p.opcion_c,
            "opcion_d": p.opcion_d,
        })
    return resultado


class SugerenciaIn(BaseModel):
    texto: str

@app.post("/api/sugerencias")
def enviar_sugerencia(body: SugerenciaIn, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not body.texto or len(body.texto.strip()) < 5:
        raise HTTPException(status_code=400, detail="Sugerencia demasiado corta")
    uid = int(current_user["sub"])
    usuario = get_usuario_or_401(uid, db)
    db.add(Sugerencia(usuario_id=uid, texto=body.texto.strip()[:1000]))
    db.commit()
    # Notificar al admin por email
    try:
        from email_utils import enviar_notificacion_sugerencia
        email_usuario = usuario.email
        enviar_notificacion_sugerencia(body.texto.strip()[:1000], email_usuario)
    except Exception:
        pass
    return {"ok": True}


class TiempoIn(BaseModel):
    segundos: int

@app.post("/api/tiempo")
def registrar_tiempo(body: TiempoIn, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if body.segundos <= 0:
        return {"ok": True}
    uid = int(current_user["sub"])
    get_usuario_or_401(uid, db)
    ahora = datetime.utcnow()

    # Tiempo total acumulado
    registro = db.query(TiempoEstudio).filter(TiempoEstudio.usuario_id == uid).first()
    if registro:
        registro.segundos_total += body.segundos
        registro.ultima_actualizacion = ahora
    else:
        db.add(TiempoEstudio(usuario_id=uid, segundos_total=body.segundos))

    # Tiempo diario (fecha sin hora, en UTC)
    from datetime import date
    hoy = datetime(ahora.year, ahora.month, ahora.day)
    diario = db.query(TiempoEstudioDiario).filter(
        TiempoEstudioDiario.usuario_id == uid,
        TiempoEstudioDiario.fecha == hoy,
    ).first()
    if diario:
        diario.segundos += body.segundos
    else:
        db.add(TiempoEstudioDiario(usuario_id=uid, fecha=hoy, segundos=body.segundos))

    db.commit()
    return {"ok": True}


@app.post("/api/racha")
def registrar_racha(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    from datetime import date, timedelta
    uid = int(current_user["sub"])
    get_usuario_or_401(uid, db)
    hoy = date.today()
    registro = db.query(RachaDiaria).filter(RachaDiaria.usuario_id == uid).first()
    if not registro:
        db.add(RachaDiaria(usuario_id=uid, racha_actual=1, racha_maxima=1, ultimo_dia=datetime.utcnow()))
        db.commit()
        return {"racha": 1, "maxima": 1, "nueva": True}
    ultimo = registro.ultimo_dia.date()
    if ultimo == hoy:
        return {"racha": registro.racha_actual, "maxima": registro.racha_maxima, "nueva": False}
    elif ultimo == hoy - timedelta(days=1):
        registro.racha_actual += 1
        registro.racha_maxima = max(registro.racha_maxima, registro.racha_actual)
        registro.ultimo_dia = datetime.utcnow()
        db.commit()
        return {"racha": registro.racha_actual, "maxima": registro.racha_maxima, "nueva": True}
    else:
        registro.racha_actual = 1
        registro.ultimo_dia = datetime.utcnow()
        db.commit()
        return {"racha": 1, "maxima": registro.racha_maxima, "nueva": False}


@app.get("/api/racha")
def obtener_racha(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    registro = db.query(RachaDiaria).filter(RachaDiaria.usuario_id == uid).first()
    if not registro:
        return {"racha": 0, "maxima": 0}
    return {"racha": registro.racha_actual, "maxima": registro.racha_maxima}


@app.get("/api/admin/sugerencias")
def ver_sugerencias(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Solo admin (primer usuario registrado, id=1)
    if not es_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Acceso denegado")
    sug = db.query(Sugerencia, Usuario).outerjoin(Usuario, Sugerencia.usuario_id == Usuario.id)\
        .order_by(Sugerencia.fecha.desc()).limit(100).all()
    return [
        {
            "id": s.id,
            "texto": s.texto,
            "fecha": s.fecha.isoformat(),
            "usuario": u.nombre or u.email if u else "Anónimo",
        }
        for s, u in sug
    ]


@app.get("/api/version")
def version():
    return {"version": "3.0", "build": "freemium"}


# ── Plan / Freemium ─────────────────────────────────────────────────────────

@app.get("/api/plan")
def obtener_plan(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    usuario = get_usuario_or_401(uid, db)
    premium = tiene_acceso_premium(usuario)
    es_trial = (
        usuario.plan == "trial"
        and usuario.trial_expira is not None
        and datetime.utcnow() < usuario.trial_expira
    )
    return {
        "plan": usuario.plan,
        "premium": premium,
        "es_trial": es_trial,
        "trial_expira": usuario.trial_expira.isoformat() if usuario.trial_expira else None,
        "plan_expira": usuario.plan_expira.isoformat() if usuario.plan_expira else None,
    }


# ── Simulacros ───────────────────────────────────────────────────────────────

class SimulacroResultadoIn(BaseModel):
    tipo: str = "constitucion"
    correctas: int
    incorrectas: int
    en_blanco: int
    tiempo_segundos: int

@app.post("/api/simulacros")
def guardar_simulacro(body: SimulacroResultadoIn, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    usuario = get_usuario_or_401(uid, db)
    if not tiene_acceso_premium(usuario):
        raise HTTPException(status_code=403, detail="Suscripción requerida")
    total = body.correctas + body.incorrectas + body.en_blanco
    # Fórmula oficial: aciertos - (errores / 3)
    puntuacion = round(body.correctas - (body.incorrectas / 3), 3)
    s = Simulacro(
        usuario_id=uid,
        tipo=body.tipo,
        total_preguntas=total,
        respondidas=body.correctas + body.incorrectas,
        correctas=body.correctas,
        incorrectas=body.incorrectas,
        en_blanco=body.en_blanco,
        puntuacion=puntuacion,
        tiempo_segundos=body.tiempo_segundos,
        completado=True,
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return {"id": s.id, "puntuacion": puntuacion, "ok": True}

@app.get("/api/simulacros")
def mis_simulacros(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    lista = db.query(Simulacro).filter(Simulacro.usuario_id == uid, Simulacro.completado == True)\
        .order_by(Simulacro.fecha.desc()).limit(20).all()
    return [
        {
            "id": s.id,
            "tipo": s.tipo,
            "correctas": s.correctas,
            "incorrectas": s.incorrectas,
            "en_blanco": s.en_blanco,
            "puntuacion": s.puntuacion,
            "tiempo_segundos": s.tiempo_segundos,
            "fecha": s.fecha.isoformat(),
        }
        for s in lista
    ]

@app.get("/api/simulacros/preguntas")
def preguntas_simulacro(
    tipo: str = "constitucion",
    n: int = Query(65, ge=10, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    uid = int(current_user["sub"])
    usuario = get_usuario_or_401(uid, db)
    if not tiene_acceso_premium(usuario):
        raise HTTPException(status_code=403, detail="Suscripción requerida")

    preguntas: list = []
    if tipo == "constitucion" or tipo == "mixto":
        sample = random.sample(QUIZ_PREGUNTAS, min(n, len(QUIZ_PREGUNTAS)))
        for p in sample:
            if "opcion_b" in p:
                opciones = [p["respuesta_correcta"], p["opcion_b"], p["opcion_c"], p["opcion_d"]]
            else:
                ops = [o for o in p["opciones"] if o != p["respuesta_correcta"]]
                opciones = [p["respuesta_correcta"]] + ops[:3]
            random.shuffle(opciones)
            preguntas.append({
                "id": f"c_{QUIZ_PREGUNTAS.index(p)}",
                "pregunta": p["pregunta"],
                "opciones": opciones,
                "correcta": p["respuesta_correcta"],
            })
    if tipo == "policia-local" or tipo == "mixto":
        op = db.query(Oposicion).filter(Oposicion.slug == "policia-local").first()
        if op:
            pp = db.query(PreguntaTema).join(Tema).filter(Tema.oposicion_id == op.id).all()
            if pp:
                sample2 = random.sample(pp, min(n - len(preguntas), len(pp)))
                for p in sample2:
                    opciones = [p.respuesta_correcta, p.opcion_b, p.opcion_c, p.opcion_d]
                    random.shuffle(opciones)
                    preguntas.append({
                        "id": f"p_{p.id}",
                        "pregunta": p.pregunta,
                        "opciones": opciones,
                        "correcta": p.respuesta_correcta,
                    })
    random.shuffle(preguntas)
    return preguntas[:n]


@app.get("/api/ranking")
def ranking(periodo: str = "total", db: Session = Depends(get_db)):
    from sqlalchemy import func
    from datetime import date, timedelta

    if periodo in ("hoy", "semana"):
        if periodo == "hoy":
            hoy = datetime.utcnow()
            fecha_inicio = datetime(hoy.year, hoy.month, hoy.day)
        else:
            hace7 = datetime.utcnow() - timedelta(days=7)
            fecha_inicio = datetime(hace7.year, hace7.month, hace7.day)

        registros = (
            db.query(
                TiempoEstudioDiario.usuario_id,
                func.sum(TiempoEstudioDiario.segundos).label("total"),
                Usuario.nombre,
                Usuario.email,
            )
            .join(Usuario, TiempoEstudioDiario.usuario_id == Usuario.id)
            .filter(TiempoEstudioDiario.fecha >= fecha_inicio)
            .group_by(TiempoEstudioDiario.usuario_id, Usuario.nombre, Usuario.email)
            .order_by(func.sum(TiempoEstudioDiario.segundos).desc())
            .limit(20)
            .all()
        )
        return [
            {
                "posicion": i + 1,
                "nombre": r.nombre or r.email.split("@")[0],
                "segundos": r.total or 0,
            }
            for i, r in enumerate(registros)
        ]

    # Total histórico
    registros = (
        db.query(TiempoEstudio, Usuario)
        .join(Usuario, TiempoEstudio.usuario_id == Usuario.id)
        .order_by(TiempoEstudio.segundos_total.desc())
        .limit(20)
        .all()
    )
    return [
        {
            "posicion": i + 1,
            "nombre": u.nombre or u.email.split("@")[0],
            "segundos": t.segundos_total,
        }
        for i, (t, u) in enumerate(registros)
    ]


# ── Stripe Pagos ────────────────────────────────────────────────────────────

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_BASICO = os.getenv("STRIPE_PRICE_BASICO", "")   # price_xxx mensual básico
STRIPE_PRICE_PRO = os.getenv("STRIPE_PRICE_PRO", "")          # price_xxx mensual pro
STRIPE_PRICE_VITALICIO = os.getenv("STRIPE_PRICE_VITALICIO", "")  # price_xxx pago único

PRECIOS_INFO = {
    "basico": {"nombre": "Básico", "precio": "4,99€/mes", "descripcion": "Acceso completo sin límites"},
    "pro": {"nombre": "Pro", "precio": "9,99€/mes", "descripcion": "Básico + Simulacros + IA tutora"},
    "vitalicio": {"nombre": "Vitalicio", "precio": "49,99€ único", "descripcion": "Acceso de por vida"},
}

@app.post("/api/stripe/checkout")
def crear_checkout(
    body: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    import stripe as stripe_lib
    stripe_lib.api_key = STRIPE_SECRET_KEY
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=503, detail="Pagos no configurados")

    uid = int(current_user["sub"])
    usuario = get_usuario_or_401(uid, db)
    plan = body.get("plan", "basico")
    price_map = {"basico": STRIPE_PRICE_BASICO, "pro": STRIPE_PRICE_PRO, "vitalicio": STRIPE_PRICE_VITALICIO}
    price_id = price_map.get(plan)
    if not price_id:
        raise HTTPException(status_code=400, detail="Plan no válido")

    base_url = os.getenv("BASE_URL", "https://oposiciones-del-estado.up.railway.app")
    mode = "payment" if plan == "vitalicio" else "subscription"

    session = stripe_lib.checkout.Session.create(
        customer_email=usuario.email,
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode=mode,
        success_url=f"{base_url}/pago-ok?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{base_url}/planes",
        metadata={"usuario_id": str(uid), "plan": plan},
    )
    return {"url": session.url}


@app.post("/api/stripe/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    import stripe as stripe_lib
    stripe_lib.api_key = STRIPE_SECRET_KEY
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    try:
        event = stripe_lib.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
    except Exception:
        raise HTTPException(status_code=400, detail="Webhook inválido")

    if event["type"] in ("checkout.session.completed", "invoice.payment_succeeded"):
        obj = event["data"]["object"]
        meta = obj.get("metadata") or {}
        uid = meta.get("usuario_id")
        plan = meta.get("plan")
        if uid and plan:
            usuario = db.query(Usuario).filter(Usuario.id == int(uid)).first()
            if usuario:
                usuario.plan = plan
                if plan == "vitalicio":
                    usuario.plan_expira = None
                else:
                    usuario.plan_expira = datetime.utcnow() + timedelta(days=32)
                if obj.get("customer"):
                    usuario.stripe_customer_id = obj["customer"]
                if obj.get("subscription"):
                    usuario.stripe_subscription_id = obj["subscription"]
                db.commit()
                logger.info(f"Plan '{plan}' activado para usuario {uid}")

    elif event["type"] == "customer.subscription.deleted":
        sub = event["data"]["object"]
        usuario = db.query(Usuario).filter(Usuario.stripe_subscription_id == sub["id"]).first()
        if usuario:
            usuario.plan = "free"
            usuario.plan_expira = datetime.utcnow()
            db.commit()
            logger.info(f"Suscripción cancelada para usuario {usuario.id}")

    return {"ok": True}


@app.get("/api/planes")
def obtener_planes():
    return PRECIOS_INFO


# ── IA Tutora ────────────────────────────────────────────────────────────────

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

class TutorIn(BaseModel):
    pregunta: str
    respuesta_usuario: str
    respuesta_correcta: str
    contexto: str | None = None

@app.post("/api/tutor")
def ia_tutora(body: TutorIn, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    usuario = get_usuario_or_401(uid, db)
    if usuario.plan not in ("pro", "vitalicio"):
        raise HTTPException(status_code=403, detail="La IA tutora requiere plan Pro o Vitalicio")
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="IA no configurada")

    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-flash-latest")

    prompt = f"""Eres un tutor experto en oposiciones del Estado español. El alumno ha fallado una pregunta.

Pregunta: {body.pregunta}
Respuesta del alumno: {body.respuesta_usuario}
Respuesta correcta: {body.respuesta_correcta}
{f'Contexto adicional: {body.contexto}' if body.contexto else ''}

Explica de forma clara y concisa (máx 3 párrafos):
1. Por qué la respuesta correcta es correcta
2. Por qué la respuesta del alumno es incorrecta
3. Un truco o regla mnemotécnica para recordarlo

Responde en español, tono cercano y motivador."""

    response = model.generate_content(prompt)
    return {"explicacion": response.text}


# ── Push Notifications ──────────────────────────────────────────────────────

VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY", "")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY", "")
VAPID_CLAIMS_SUB = os.getenv("VAPID_CLAIMS_SUB", "mailto:admin@oposapp.es")

def enviar_push(suscripcion: "PushSuscripcion", titulo: str, body: str, url: str = "/"):
    if not VAPID_PUBLIC_KEY or not VAPID_PRIVATE_KEY:
        return False
    try:
        from pywebpush import webpush, WebPushException
        import json as _json
        subscription_info = {
            "endpoint": suscripcion.endpoint,
            "keys": {"p256dh": suscripcion.p256dh, "auth": suscripcion.auth},
        }
        webpush(
            subscription_info=subscription_info,
            data=_json.dumps({"title": titulo, "body": body, "url": url}),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": VAPID_CLAIMS_SUB},
        )
        return True
    except Exception as e:
        logger.warning(f"Push error: {e}")
        return False

@app.get("/api/push/vapid-key")
def obtener_vapid_key():
    return {"publicKey": VAPID_PUBLIC_KEY}

class PushSuscripcionIn(BaseModel):
    endpoint: str
    p256dh: str
    auth: str

@app.post("/api/push/subscribe")
def suscribir_push(body: PushSuscripcionIn, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    get_usuario_or_401(uid, db)
    existente = db.query(PushSuscripcion).filter(
        PushSuscripcion.usuario_id == uid,
        PushSuscripcion.endpoint == body.endpoint,
    ).first()
    if not existente:
        db.add(PushSuscripcion(usuario_id=uid, endpoint=body.endpoint, p256dh=body.p256dh, auth=body.auth))
        db.commit()
    return {"ok": True}


# ── Chatbot IA ───────────────────────────────────────────────────────────────

class ChatMensaje(BaseModel):
    rol: str
    texto: str

class ChatIn(BaseModel):
    mensaje: str
    historial: list[ChatMensaje] = []

@app.post("/api/chat")
def chatbot(body: ChatIn, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    usuario = get_usuario_or_401(uid, db)
    if not tiene_acceso_premium(usuario):
        raise HTTPException(status_code=403, detail="El chatbot requiere suscripción activa")
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="IA no configurada")

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            "gemini-flash-latest",
            system_instruction="""Eres un asistente experto en oposiciones del Estado español.
Conoces en profundidad: la Constitución Española de 1978, temarios de Policía Local, Policía Nacional, Guardia Civil, Correos y otras oposiciones del Estado.
Responde siempre en español, de forma clara, precisa y motivadora.
Si no sabes algo con certeza, dilo claramente. Máximo 200 palabras por respuesta."""
        )
        history = []
        for m in body.historial:
            history.append({"role": "user" if m.rol == "user" else "model", "parts": [m.texto]})
        chat = model.start_chat(history=history)
        response = chat.send_message(body.mensaje)
        return {"respuesta": response.text}
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Error IA: {str(e)[:100]}")


# ── Perfil usuario ───────────────────────────────────────────────────────────

class PerfilIn(BaseModel):
    nombre: str | None = None
    email: str | None = None
    foto_url: str | None = None

class CambiarPasswordIn(BaseModel):
    password_actual: str
    nueva_password: str

@app.get("/api/perfil")
def obtener_perfil(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    u = get_usuario_or_401(uid, db)
    return {
        "email": u.email, "nombre": u.nombre, "foto_url": getattr(u, "foto_url", None),
        "plan": u.plan, "premium": tiene_acceso_premium(u),
        "trial_expira": u.trial_expira.isoformat() if u.trial_expira else None,
        "plan_expira": u.plan_expira.isoformat() if u.plan_expira else None,
        "fecha_registro": u.fecha_registro.isoformat(),
    }

@app.post("/api/perfil")
def actualizar_perfil(body: PerfilIn, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    u = get_usuario_or_401(uid, db)
    if body.nombre is not None:
        u.nombre = body.nombre.strip()[:100]
    if body.email is not None:
        nuevo_email = body.email.strip().lower()
        if "@" not in nuevo_email:
            raise HTTPException(status_code=400, detail="Email no válido")
        existente = db.query(Usuario).filter(Usuario.email == nuevo_email, Usuario.id != uid).first()
        if existente:
            raise HTTPException(status_code=409, detail="Ese email ya está en uso")
        u.email = nuevo_email
    db.commit()
    return {"ok": True, "nombre": u.nombre, "email": u.email}

@app.post("/api/perfil/password")
def cambiar_password(body: CambiarPasswordIn, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    u = get_usuario_or_401(uid, db)
    if not verify_password(body.password_actual, u.password_hash):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    if len(body.nueva_password) < 6:
        raise HTTPException(status_code=400, detail="La nueva contraseña debe tener al menos 6 caracteres")
    u.password_hash = hash_password(body.nueva_password)
    db.commit()
    return {"ok": True}

@app.post("/api/perfil/cancelar-plan")
def cancelar_plan(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = int(current_user["sub"])
    u = get_usuario_or_401(uid, db)
    if u.stripe_subscription_id and STRIPE_SECRET_KEY:
        try:
            import stripe as stripe_lib
            stripe_lib.api_key = STRIPE_SECRET_KEY
            stripe_lib.Subscription.cancel(u.stripe_subscription_id)
        except Exception as e:
            logger.warning(f"Error cancelando Stripe: {e}")
    u.plan = "free"
    u.plan_expira = datetime.utcnow()
    u.stripe_subscription_id = None
    db.commit()
    return {"ok": True}


@app.post("/api/admin/actualizar")
def forzar_actualizacion(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not es_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Acceso denegado")
    from scheduler import ejecutar_comprobacion_boe
    ejecutar_comprobacion_boe()
    return {"ok": True, "mensaje": "Comprobación iniciada"}


# ── Servir frontend compilado (producción) ─────────────────────────────────
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(STATIC_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_frontend(full_path: str):
        # No interceptar rutas de la API
        if full_path.startswith("api/"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404)
        # Servir archivos estáticos del raíz (hero.jpg, favicon.ico, etc.)
        safe_path = full_path.replace("\\", "/").lstrip("/")
        static_file = os.path.join(STATIC_DIR, safe_path)
        if os.path.isfile(static_file):
            return FileResponse(static_file)
        index = os.path.join(STATIC_DIR, "index.html")
        return FileResponse(index)


# ── Helpers ────────────────────────────────────────────────────────────────

def _serializar_articulo(a: Articulo, breve: bool = False) -> dict:
    base = {
        "id": a.id,
        "numero": a.numero,
        "titulo": a.titulo,
        "titulo_titulo": a.titulo_titulo,
        "titulo_capitulo": a.titulo_capitulo,
        "titulo_seccion": a.titulo_seccion,
        "contenido": a.contenido,
        "actualizado_en": a.actualizado_en.isoformat(),
    }
    if not breve:
        base["cambios"] = [
            {
                "id": c.id,
                "descripcion": c.descripcion,
                "fecha": c.fecha.isoformat(),
                "boe_referencia": c.boe_referencia,
            }
            for c in a.cambios
        ]
    return base
