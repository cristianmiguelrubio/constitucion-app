"""
Exporta los temas de Policía Local (con resúmenes y preguntas) a seed_temas.py
para que Railway los cargue automáticamente en el primer despliegue.

Uso:
  python exportar_temas_seed.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from database import SessionLocal
from models import Oposicion, Tema, PreguntaTema

db = SessionLocal()
temas = (
    db.query(Tema)
    .join(Oposicion)
    .filter(Oposicion.slug == "policia-local")
    .order_by(Tema.numero)
    .all()
)

lines = [
    "# Auto-generado por exportar_temas_seed.py — no editar manualmente\n",
    "TEMAS_POLICIA_LOCAL = [\n",
]

total_preguntas = 0
for t in temas:
    contenido = (t.contenido or "").replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    resumen   = (t.resumen   or "").replace("\\", "\\\\").replace('"""', '\\"\\"\\"')

    preguntas = db.query(PreguntaTema).filter(PreguntaTema.tema_id == t.id).all()
    total_preguntas += len(preguntas)

    preg_lines = []
    for p in preguntas:
        preg_lines.append(
            f'            {{'
            f'"seccion": {repr(p.seccion)}, '
            f'"pregunta": {repr(p.pregunta)}, '
            f'"respuesta_correcta": {repr(p.respuesta_correcta)}, '
            f'"opcion_b": {repr(p.opcion_b)}, '
            f'"opcion_c": {repr(p.opcion_c)}, '
            f'"opcion_d": {repr(p.opcion_d)}'
            f'}},'
        )

    lines.append(f'    {{\n')
    lines.append(f'        "numero": {t.numero},\n')
    lines.append(f'        "titulo": {repr(t.titulo)},\n')
    lines.append(f'        "contenido": """{contenido}""",\n')
    lines.append(f'        "resumen": """{resumen}""",\n')
    lines.append(f'        "preguntas": [\n')
    for pl in preg_lines:
        lines.append(f'        {pl}\n')
    lines.append(f'        ],\n')
    lines.append(f'    }},\n')

lines.append("]\n")

out = Path(__file__).parent / "seed_temas.py"
out.write_text("".join(lines), encoding="utf-8")
print(f"Exportados {len(temas)} temas, {total_preguntas} preguntas → {out}")
db.close()
