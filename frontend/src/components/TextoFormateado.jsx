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

// ── Agrupa bloques en secciones ───────────────────────────────────────────────

const COLORES = [
  { borde: 'border-brand-400',   fondo: 'bg-brand-50',   texto: 'text-brand-700'   },
  { borde: 'border-indigo-400',  fondo: 'bg-indigo-50',  texto: 'text-indigo-700'  },
  { borde: 'border-emerald-400', fondo: 'bg-emerald-50', texto: 'text-emerald-700' },
  { borde: 'border-amber-400',   fondo: 'bg-amber-50',   texto: 'text-amber-700'   },
  { borde: 'border-rose-400',    fondo: 'bg-rose-50',    texto: 'text-rose-700'    },
]

function agruparEnSecciones(bloques) {
  const secciones = []
  let actual = { titulo: null, contenido: [] }

  for (const b of bloques) {
    if (b.tipo === 'titulo') {
      if (actual.contenido.length > 0 || actual.titulo) secciones.push(actual)
      actual = { titulo: b.texto, contenido: [] }
    } else {
      actual.contenido.push(b)
    }
  }
  if (actual.contenido.length > 0 || actual.titulo) secciones.push(actual)
  return secciones
}

// ── Subcomponente: bloque de contenido ───────────────────────────────────────

function BloqueContenido({ b }) {
  if (b.tipo === 'lista') {
    return (
      <ul className="space-y-1.5 my-2 pl-1">
        {b.items.map((item, j) => (
          <li key={j} className="flex gap-2 text-gray-700 text-[14px]">
            <span className="text-brand-400 mt-0.5 shrink-0 text-xs">▸</span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    )
  }
  if (b.tipo === 'parrafo') {
    return <p className="text-gray-700 text-[14px] leading-relaxed my-2">{b.texto}</p>
  }
  return null
}

// ── Subcomponente: sección plegable ──────────────────────────────────────────

function Seccion({ seccion, colorIdx, abiertaInicial }) {
  const [abierta, setAbierta] = useState(abiertaInicial)
  const c = COLORES[colorIdx % COLORES.length]

  if (!seccion.titulo) {
    // Bloques sin título van siempre visibles (intro del tema)
    return (
      <div className="space-y-1 mb-3">
        {seccion.contenido.map((b, i) => <BloqueContenido key={i} b={b} />)}
      </div>
    )
  }

  return (
    <div className={`rounded-xl border ${abierta ? 'border-gray-200' : 'border-gray-100'} overflow-hidden mb-2`}>
      <button
        onClick={() => setAbierta(v => !v)}
        className={`w-full flex items-center gap-3 px-4 py-3 text-left transition-colors ${
          abierta ? `${c.fondo} ${c.texto}` : 'bg-gray-50 text-gray-600 active:bg-gray-100'
        }`}
      >
        <span className={`shrink-0 w-1.5 h-5 rounded-full ${c.borde} border-2`} />
        <span className="flex-1 font-semibold text-[13px] uppercase tracking-wide leading-snug">
          {seccion.titulo}
        </span>
        <span className="text-xs opacity-50 shrink-0">{abierta ? '▲' : '▼'}</span>
      </button>

      {abierta && (
        <div className="px-4 pb-4 pt-2 bg-white border-t border-gray-100">
          {seccion.contenido.map((b, i) => <BloqueContenido key={i} b={b} />)}
        </div>
      )}
    </div>
  )
}

// ── Componente principal ──────────────────────────────────────────────────────

import { useState } from 'react'

export default function TextoFormateado({ texto }) {
  if (!texto) return (
    <div className="text-center py-10 text-gray-400">
      <p className="text-3xl mb-2">🚧</p>
      <p>Texto pendiente de procesamiento</p>
    </div>
  )

  const bloques = parsear(texto)
  const secciones = agruparEnSecciones(bloques)
  let colorIdx = 0

  return (
    <div>
      {/* Índice rápido */}
      {secciones.filter(s => s.titulo).length > 1 && (
        <div className="bg-gray-50 rounded-xl p-3 mb-4 border border-gray-100">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Contenido</p>
          <div className="space-y-1">
            {secciones.filter(s => s.titulo).map((s, i) => {
              const c = COLORES[i % COLORES.length]
              return (
                <p key={i} className={`text-xs font-medium ${c.texto} flex items-center gap-1.5`}>
                  <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${c.borde} border-2`} />
                  {s.titulo}
                </p>
              )
            })}
          </div>
        </div>
      )}

      {/* Secciones */}
      {secciones.map((s, i) => (
        <Seccion
          key={i}
          seccion={s}
          colorIdx={s.titulo ? colorIdx++ : 0}
          abiertaInicial={i === 0 || !s.titulo}
        />
      ))}
    </div>
  )
}
