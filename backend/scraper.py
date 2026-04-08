"""
Scraper robusto de la Constitución Española desde el BOE.
URL oficial texto consolidado: https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229

El BOE renderiza el texto mediante XSLT. Las clases CSS relevantes son:
  - div#textoxslt  → contenedor principal
  - p.dct-title     → títulos estructurales
  - p.dct-chapter   → capítulos
  - p.dct-section   → secciones
  - p.dct-article   → encabezado del artículo
  - p.parrafo       → párrafos de contenido
  - p.dct-parrafo   → párrafos de contenido (variante)

Si esas clases no están presentes se cae a un parser por regex sobre el texto plano.
"""
import httpx
from bs4 import BeautifulSoup, Tag
import re
import logging
from datetime import datetime, date
import time

logger = logging.getLogger(__name__)

BOE_CONSTITUCION_URL = "https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229"
BOE_SUMARIO_URL      = "https://www.boe.es/datosabiertos/api/boe/sumario/{fecha}"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# ── Helpers ────────────────────────────────────────────────────────────────

_RE_ART   = re.compile(r'^Art[íi]culo\s+(\d+[.\s]?\w*)[.\s]*(.*)?$', re.IGNORECASE)
_RE_TITU  = re.compile(r'^T[ÍI]TULO\s+(PRELIMINAR|[IVXLCDM]+)', re.IGNORECASE)
_RE_CAP   = re.compile(r'^CAP[ÍI]TULO\s+', re.IGNORECASE)
_RE_SEC   = re.compile(r'^SECCI[OÓ]N\s+\d+', re.IGNORECASE)
_RE_DISP  = re.compile(r'^DISPOSICI[OÓ]N\s+(ADICIONAL|TRANSITORIA|DEROGATORIA|FINAL)', re.IGNORECASE)
_RE_NUM   = re.compile(r'^\d+[\.\)]?\s')


def _limpiar(texto: str) -> str:
    return re.sub(r'[ \t]+', ' ', texto).strip()


def _numero_limpio(raw: str) -> str:
    """'1. ' → '1',  '10bis' → '10bis', '   1  ' → '1'"""
    return raw.strip().rstrip('.')


# ── Parser principal (clases CSS del BOE) ─────────────────────────────────

def _parsear_por_clases(soup: BeautifulSoup) -> list[dict]:
    """Intenta parsear usando las clases CSS oficiales del BOE."""
    contenedor = (
        soup.find("div", id="textoxslt")
        or soup.find("div", class_="textoDisposicion")
        or soup.find("div", id="texto")
    )
    if not contenedor:
        return []

    articulos = []
    titulo_actual = capitulo_actual = seccion_actual = None
    art_actual: dict | None = None

    for elem in contenedor.descendants:
        if not isinstance(elem, Tag):
            continue

        # Solo procesar elementos de bloque directos (evitar duplicados)
        if elem.name not in ("p", "h1", "h2", "h3", "h4", "h5", "div"):
            continue
        if elem.find_parent(["p", "h1", "h2", "h3", "h4", "h5"]):
            continue  # es hijo de otro elemento ya procesado

        texto = _limpiar(elem.get_text(" ", strip=True))
        if not texto or len(texto) < 2:
            continue

        clases = elem.get("class", [])

        # Detectar estructura jerárquica por clase
        if any(c in clases for c in ("dct-title", "titulo", "parte")):
            if art_actual:
                articulos.append(art_actual); art_actual = None
            titulo_actual  = texto
            capitulo_actual = seccion_actual = None
            continue

        if any(c in clases for c in ("dct-chapter", "capitulo")):
            if art_actual:
                articulos.append(art_actual); art_actual = None
            capitulo_actual = texto
            seccion_actual  = None
            continue

        if any(c in clases for c in ("dct-section", "seccion")):
            if art_actual:
                articulos.append(art_actual); art_actual = None
            seccion_actual = texto
            continue

        # Artículo — puede estar en clase "dct-article" o "articulo"
        if any(c in clases for c in ("dct-article", "articulo")):
            if art_actual:
                articulos.append(art_actual)
            m = _RE_ART.match(texto)
            numero = _numero_limpio(m.group(1)) if m else texto[:20]
            titulo_art = _limpiar(m.group(2)) if m and m.group(2) else None
            art_actual = {
                "numero": numero,
                "titulo": titulo_art,
                "contenido": texto,
                "titulo_titulo":   titulo_actual,
                "titulo_capitulo": capitulo_actual,
                "titulo_seccion":  seccion_actual,
            }
            continue

        # Párrafos de contenido
        if art_actual and any(c in clases for c in ("parrafo", "dct-parrafo", "apartado")):
            art_actual["contenido"] += "\n" + texto
            continue

        # Sin clase específica: intentar detectar por regex
        m_art = _RE_ART.match(texto)
        if m_art:
            if art_actual:
                articulos.append(art_actual)
            numero = _numero_limpio(m_art.group(1))
            titulo_art = _limpiar(m_art.group(2)) if m_art.group(2) else None
            art_actual = {
                "numero": numero,
                "titulo": titulo_art,
                "contenido": texto,
                "titulo_titulo":   titulo_actual,
                "titulo_capitulo": capitulo_actual,
                "titulo_seccion":  seccion_actual,
            }
            continue

        if _RE_TITU.match(texto):
            if art_actual:
                articulos.append(art_actual); art_actual = None
            titulo_actual = texto
            capitulo_actual = seccion_actual = None
            continue

        if _RE_CAP.match(texto):
            if art_actual:
                articulos.append(art_actual); art_actual = None
            capitulo_actual = texto
            seccion_actual  = None
            continue

        if _RE_SEC.match(texto):
            if art_actual:
                articulos.append(art_actual); art_actual = None
            seccion_actual = texto
            continue

        # Párrafo que pertenece al artículo actual
        if art_actual and texto:
            art_actual["contenido"] += "\n" + texto

    if art_actual:
        articulos.append(art_actual)

    return articulos


# ── Parser de fallback (texto plano) ───────────────────────────────────────

def _parsear_texto_plano(html: str) -> list[dict]:
    """
    Parser de último recurso: extrae el texto completo y lo divide
    buscando 'Artículo N.' como separador.
    """
    soup = BeautifulSoup(html, "lxml")
    # Quitar scripts y estilos
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()

    texto_completo = soup.get_text("\n")
    lineas = [_limpiar(l) for l in texto_completo.splitlines() if _limpiar(l)]

    articulos = []
    titulo_actual = capitulo_actual = seccion_actual = None
    art_actual: dict | None = None

    for linea in lineas:
        if _RE_TITU.match(linea):
            if art_actual:
                articulos.append(art_actual); art_actual = None
            titulo_actual = linea
            capitulo_actual = seccion_actual = None
            continue

        if _RE_CAP.match(linea):
            if art_actual:
                articulos.append(art_actual); art_actual = None
            capitulo_actual = linea
            seccion_actual  = None
            continue

        if _RE_SEC.match(linea):
            if art_actual:
                articulos.append(art_actual); art_actual = None
            seccion_actual = linea
            continue

        m_art = _RE_ART.match(linea)
        if m_art:
            if art_actual:
                articulos.append(art_actual)
            numero = _numero_limpio(m_art.group(1))
            titulo_art = _limpiar(m_art.group(2)) if m_art.group(2) else None
            art_actual = {
                "numero": numero,
                "titulo": titulo_art,
                "contenido": linea,
                "titulo_titulo":   titulo_actual,
                "titulo_capitulo": capitulo_actual,
                "titulo_seccion":  seccion_actual,
            }
            continue

        if art_actual and linea:
            art_actual["contenido"] += "\n" + linea

    if art_actual:
        articulos.append(art_actual)

    return articulos


# ── Post-procesado ─────────────────────────────────────────────────────────

def _postprocesar(articulos: list[dict]) -> list[dict]:
    """
    Limpia y deduplica la lista de artículos.
    - Elimina entradas que no sean artículos reales (número vacío, etc.)
    - Elimina contenido duplicado al inicio de cada artículo
    - Ordena por número
    """
    vistos = set()
    resultado = []
    for art in articulos:
        num = art.get("numero", "").strip()
        if not num or not num[0].isdigit():
            continue
        if num in vistos:
            continue
        vistos.add(num)
        # Eliminar duplicado del número al inicio del contenido
        contenido = art.get("contenido", "").strip()
        resultado.append({**art, "numero": num, "contenido": contenido})

    # Orden numérico
    def _orden(a):
        try:
            return int(re.search(r'\d+', a["numero"]).group())
        except Exception:
            return 9999

    resultado.sort(key=_orden)
    return resultado


# ── Función pública principal ──────────────────────────────────────────────

def scrape_constitucion() -> list[dict]:
    """
    Descarga y parsea la Constitución Española desde el BOE.
    Intenta primero el parser por clases CSS, luego el de texto plano.
    Lanza excepción si obtiene menos de 100 artículos (señal de fallo).
    """
    logger.info("Descargando Constitución desde BOE: %s", BOE_CONSTITUCION_URL)

    html = None
    for intento in range(1, 4):
        try:
            with httpx.Client(headers=HEADERS, timeout=40, follow_redirects=True) as client:
                resp = client.get(BOE_CONSTITUCION_URL)
                resp.raise_for_status()
                html = resp.text
                break
        except httpx.HTTPError as e:
            logger.warning("Intento %d/3 fallido: %s", intento, e)
            if intento < 3:
                time.sleep(2 * intento)

    if not html:
        raise RuntimeError("No se pudo descargar la Constitución del BOE tras 3 intentos")

    soup = BeautifulSoup(html, "lxml")

    # Intentar parser por clases CSS primero
    articulos = _parsear_por_clases(soup)
    if len(articulos) >= 100:
        logger.info("Parser CSS: %d artículos extraídos", len(articulos))
        return _postprocesar(articulos)

    # Fallback: texto plano
    logger.warning("Parser CSS solo obtuvo %d artículos, usando fallback texto plano", len(articulos))
    articulos = _parsear_texto_plano(html)
    if len(articulos) >= 100:
        logger.info("Parser texto plano: %d artículos extraídos", len(articulos))
        return _postprocesar(articulos)

    raise RuntimeError(
        f"Scraper obtuvo solo {len(articulos)} artículos — "
        "puede que el BOE haya cambiado su estructura HTML"
    )


# ── Comprobación diaria del BOE ────────────────────────────────────────────

def check_boe_actualizaciones(fecha: date | None = None) -> list[dict]:
    """
    Consulta el sumario del BOE de un día y devuelve entradas
    que afecten a la Constitución (BOE-A-1978-31229).
    """
    if fecha is None:
        fecha = datetime.utcnow().date()

    url = BOE_SUMARIO_URL.format(fecha=fecha.strftime("%Y%m%d"))
    logger.info("Consultando sumario BOE %s", fecha)

    try:
        with httpx.Client(headers=HEADERS, timeout=15) as client:
            resp = client.get(url)
            if resp.status_code == 404:
                return []
            resp.raise_for_status()
            data = resp.json()
    except (httpx.HTTPError, ValueError) as e:
        logger.warning("Error consultando sumario BOE: %s", e)
        return []

    entradas = []
    try:
        # Navegar la estructura JSON del BOE
        diario = data.get("data", {}).get("sumario", {}).get("diario", {})
        secciones = diario.get("seccion", [])
        if isinstance(secciones, dict):
            secciones = [secciones]

        for seccion in secciones:
            departamentos = seccion.get("departamento", [])
            if isinstance(departamentos, dict):
                departamentos = [departamentos]
            for dep in departamentos:
                epigrafes = dep.get("epigrafe", [])
                if isinstance(epigrafes, dict):
                    epigrafes = [epigrafes]
                for epi in epigrafes:
                    items = epi.get("item", [])
                    if isinstance(items, dict):
                        items = [items]
                    for item in items:
                        titulo_item = item.get("titulo", "")
                        boe_id = item.get("id", "")
                        if (
                            "constituci" in titulo_item.lower()
                            or "BOE-A-1978-31229" in str(item)
                            or "reforma constitucional" in titulo_item.lower()
                        ):
                            entradas.append({
                                "id":      boe_id,
                                "titulo":  titulo_item,
                                "url_pdf": item.get("url_pdf", ""),
                            })
    except Exception as e:
        logger.warning("Error parseando sumario BOE: %s", e)

    return entradas
