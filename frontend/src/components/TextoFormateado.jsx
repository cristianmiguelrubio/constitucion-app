/**
 * Parsea y renderiza texto OCR de temarios de oposiciones.
 * Detecta títulos, listas, viñetas y párrafos automáticamente.
 */

const PATRONES_BASURA = [
  /^GRUPO\s+\d+\s*[-–]\s*/i,      // "GRUPO 1 - DERECHO CONSTITUCIONAL TEMA 1"
  /^TEMA\s+\d+\s*$/i,              // líneas sueltas "TEMA 5"
  /^\d+\s*$/,                      // páginas sueltas "1", "2"
  /^[-–—]+\s*$/,                   // líneas de separación "---"
  /^www\./i,                       // URLs
  /^[.·•\s]{3,}$/,                 // líneas de puntos
]

function esBasura(linea) {
  const l = linea.trim()
  if (PATRONES_BASURA.some(p => p.test(l))) return true
  // Líneas con más de 40% de caracteres no alfanuméricos → basura OCR
  if (l.length > 3) {
    const letras = (l.match(/[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]/g) || []).length
    if (letras / l.length < 0.4 && l.length < 40) return true
  }
  return false
}

function esTitulo(linea) {
  const l = linea.trim()
  if (l.length < 4 || l.length > 120) return false
  // Mayúsculas puras (con acentos y ñ), al menos 4 letras mayúsculas
  const letras = l.replace(/[^a-záéíóúñüA-ZÁÉÍÓÚÑÜ]/g, '')
  if (letras.length < 4) return false
  const pctMayus = (l.match(/[A-ZÁÉÍÓÚÑÜ]/g) || []).length / letras.length
  return pctMayus > 0.75 && letras.length >= 4
}

function esViñeta(linea) {
  return /^[=•\-–*]\s+\S/.test(linea.trim()) ||
         /^e\s+[A-ZÁÉÍÓÚÑÜ]/.test(linea.trim())   // OCR lee "•" como "e "
}

function esItem(linea) {
  const l = linea.trim()
  return /^[a-záéíóúñ]\)\s+/i.test(l) ||
         /^\d+[\.\-–)]\s+[A-Za-záéíóúñÁÉÍÓÚÑ]/.test(l)
}

function limpiarViñeta(texto) {
  return texto.trim()
    .replace(/^[=•\-–*]\s+/, '')
    .replace(/^e\s+(?=[A-ZÁÉÍÓÚÑÜ])/, '')
    .trim()
}

function parsear(texto) {
  const lineas = texto.split('\n')
  const bloques = []
  let parrafo = []

  const flushParrafo = () => {
    const txt = parrafo.join(' ').trim()
    if (txt.length > 2) bloques.push({ tipo: 'parrafo', texto: txt })
    parrafo = []
  }

  for (let i = 0; i < lineas.length; i++) {
    const raw = lineas[i]
    const l = raw.trim()

    if (!l) { flushParrafo(); continue }
    if (esBasura(l)) continue

    if (esTitulo(l)) {
      flushParrafo()
      bloques.push({ tipo: 'titulo', texto: l })
      continue
    }

    if (esViñeta(l)) {
      flushParrafo()
      bloques.push({ tipo: 'bullet', texto: limpiarViñeta(l) })
      continue
    }

    if (esItem(l)) {
      flushParrafo()
      bloques.push({ tipo: 'item', texto: l })
      continue
    }

    // Línea corta que termina en punto = fin de párrafo, no la peguemos a la siguiente
    parrafo.push(l)
    if (l.endsWith('.') || l.endsWith(':')) {
      // Mirar si la siguiente línea empieza en mayúscula → párrafo nuevo
      const sig = lineas[i + 1]?.trim()
      if (sig && /^[A-ZÁÉÍÓÚÑÜ]/.test(sig) && !esViñeta(sig) && !esItem(sig)) {
        flushParrafo()
      }
    }
  }
  flushParrafo()

  // Agrupar bullets/items consecutivos en listas
  const agrupados = []
  let listaActual = null
  for (const b of bloques) {
    if (b.tipo === 'bullet' || b.tipo === 'item') {
      if (!listaActual) { listaActual = { tipo: 'lista', items: [] }; agrupados.push(listaActual) }
      listaActual.items.push(b.texto)
    } else {
      listaActual = null
      agrupados.push(b)
    }
  }
  return agrupados
}

// ── Componente ────────────────────────────────────────────────────────────────

const COLORES_TITULO = [
  'text-brand-700 border-brand-300 bg-brand-50',
  'text-indigo-700 border-indigo-300 bg-indigo-50',
  'text-emerald-700 border-emerald-300 bg-emerald-50',
  'text-amber-700 border-amber-300 bg-amber-50',
  'text-rose-700 border-rose-300 bg-rose-50',
]

export default function TextoFormateado({ texto }) {
  if (!texto) return (
    <div className="text-center py-10 text-gray-400">
      <p className="text-3xl mb-2">🚧</p>
      <p>Texto pendiente de procesamiento</p>
    </div>
  )

  const bloques = parsear(texto)
  let contadorTitulos = 0

  return (
    <div className="space-y-3 text-[15px] leading-relaxed">
      {bloques.map((b, i) => {
        if (b.tipo === 'titulo') {
          const color = COLORES_TITULO[contadorTitulos % COLORES_TITULO.length]
          contadorTitulos++
          return (
            <h2
              key={i}
              className={`font-bold text-sm uppercase tracking-wide px-3 py-2 rounded-lg border-l-4 mt-5 first:mt-0 ${color}`}
            >
              {b.texto}
            </h2>
          )
        }

        if (b.tipo === 'lista') {
          return (
            <ul key={i} className="space-y-1.5 pl-2">
              {b.items.map((item, j) => (
                <li key={j} className="flex gap-2 text-gray-700">
                  <span className="text-brand-400 mt-1 shrink-0">▸</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          )
        }

        if (b.tipo === 'parrafo') {
          return (
            <p key={i} className="text-gray-700">
              {b.texto}
            </p>
          )
        }

        return null
      })}
    </div>
  )
}
