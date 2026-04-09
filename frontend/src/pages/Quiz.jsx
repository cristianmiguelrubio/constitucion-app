import { apiFetch } from '../utils/api'
import { useEffect, useState, useCallback } from 'react'

const TOTAL = 10

// ── Quiz engine (compartido) ──────────────────────────────────────────────────
function QuizEngine({ fetchPreguntas, onSalir, titulo }) {
  const [fase, setFase] = useState('cargando')
  const [preguntas, setPreguntas] = useState([])
  const [indice, setIndice] = useState(0)
  const [seleccionada, setSeleccionada] = useState(null)
  const [correctas, setCorrectas] = useState(0)
  const [historial, setHistorial] = useState([])

  useEffect(() => {
    fetchPreguntas().then(data => {
      if (!data?.length) { setFase('vacio'); return }
      setPreguntas(data.map(p => ({
        ...p,
        opciones: [p.respuesta_correcta, p.opcion_b, p.opcion_c, p.opcion_d]
          .sort(() => Math.random() - 0.5),
      })))
      setFase('jugando')
    }).catch(() => setFase('vacio'))
  }, [])

  const responder = (opcion) => {
    if (seleccionada) return
    setSeleccionada(opcion)
    const p = preguntas[indice]
    if (opcion === p.respuesta_correcta) setCorrectas(c => c + 1)
    setHistorial(h => [...h, { pregunta: p.pregunta, correcta: p.respuesta_correcta, elegida: opcion, ref: p.articulo || p.seccion }])
  }

  const siguiente = () => {
    if (indice + 1 >= preguntas.length) setFase('resultado')
    else { setIndice(i => i + 1); setSeleccionada(null) }
  }

  if (fase === 'cargando') return <div className="flex justify-center mt-16"><div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" /></div>
  if (fase === 'vacio') return <div className="card text-center mt-10 text-gray-400"><p className="text-3xl mb-2">📭</p><p>Sin preguntas disponibles</p><button onClick={onSalir} className="mt-3 text-sm text-brand-500">← Volver</button></div>

  if (fase === 'resultado') {
    const pct = Math.round(correctas / preguntas.length * 100)
    return (
      <div className="max-w-xl mx-auto">
        <div className="card text-center mb-5">
          <p className="text-5xl mb-3">{pct >= 80 ? '🏆' : pct >= 60 ? '👍' : pct >= 40 ? '📚' : '💪'}</p>
          <p className="text-2xl font-bold text-brand-700">{correctas}/{preguntas.length}</p>
          <p className="text-sm text-gray-500 mt-1">{pct}% correcto</p>
          <div className="w-full bg-gray-100 rounded-full h-2 my-3">
            <div className={`h-2 rounded-full ${pct >= 60 ? 'bg-green-500' : pct >= 40 ? 'bg-amber-400' : 'bg-red-400'}`} style={{ width: `${pct}%` }} />
          </div>
          <div className="flex gap-2 mt-2">
            <button onClick={() => { setFase('cargando'); setIndice(0); setCorrectas(0); setHistorial([]); setSeleccionada(null)
              fetchPreguntas().then(data => { setPreguntas(data.map(p => ({ ...p, opciones: [p.respuesta_correcta, p.opcion_b, p.opcion_c, p.opcion_d].sort(() => Math.random() - 0.5) }))); setFase('jugando') }) }}
              className="btn-primary flex-1">Repetir</button>
            <button onClick={onSalir} className="flex-1 border border-gray-200 text-gray-600 px-4 py-2 rounded-xl text-sm font-medium">← Salir</button>
          </div>
        </div>
        <h3 className="font-semibold text-gray-600 mb-3 text-sm">Repaso</h3>
        <div className="space-y-2">
          {historial.map((h, i) => (
            <div key={i} className={`card border-l-4 py-3 ${h.elegida === h.correcta ? 'border-green-400' : 'border-red-400'}`}>
              {h.ref && <p className="text-xs text-gray-400 mb-1">{h.ref}</p>}
              <p className="text-sm text-gray-700 mb-1">{h.pregunta}</p>
              {h.elegida !== h.correcta && <p className="text-xs text-red-500">✗ {h.elegida}</p>}
              <p className="text-xs text-green-600 font-medium">✓ {h.correcta}</p>
            </div>
          ))}
        </div>
      </div>
    )
  }

  const p = preguntas[indice]
  return (
    <div className="max-w-xl mx-auto">
      <div className="flex items-center justify-between mb-2">
        <button onClick={onSalir} className="text-xs text-gray-400">← {titulo}</button>
        <span className="text-sm text-gray-500">{indice + 1}/{preguntas.length} · <span className="text-green-600 font-medium">{correctas} ✓</span></span>
      </div>
      <div className="w-full bg-gray-100 rounded-full h-1.5 mb-4">
        <div className="bg-brand-500 h-1.5 rounded-full" style={{ width: `${(indice / preguntas.length) * 100}%` }} />
      </div>
      <div className="card mb-4">
        {p.articulo && <p className="text-xs text-gray-400 mb-1">Art. {p.articulo}</p>}
        {p.seccion && <p className="text-xs text-indigo-400 mb-1">{p.seccion}</p>}
        <p className="font-semibold text-gray-800 leading-snug">{p.pregunta}</p>
      </div>
      <div className="space-y-2 mb-5">
        {p.opciones.map((op, i) => {
          let cls = 'w-full text-left px-4 py-3 rounded-xl border-2 text-sm font-medium transition-all '
          if (!seleccionada) cls += 'border-gray-200 active:border-brand-400 active:bg-brand-50 text-gray-700'
          else if (op === p.respuesta_correcta) cls += 'border-green-400 bg-green-50 text-green-800'
          else if (op === seleccionada) cls += 'border-red-400 bg-red-50 text-red-700'
          else cls += 'border-gray-100 text-gray-400'
          return (
            <button key={i} onClick={() => responder(op)} className={cls}>
              <span className="font-bold text-gray-400 mr-2">{String.fromCharCode(65 + i)}.</span>
              {op}
              {seleccionada && op === p.respuesta_correcta && ' ✓'}
              {seleccionada && op === seleccionada && op !== p.respuesta_correcta && ' ✗'}
            </button>
          )
        })}
      </div>
      {seleccionada && (
        <button onClick={siguiente} className="btn-primary w-full">
          {indice + 1 >= preguntas.length ? 'Ver resultado' : 'Siguiente →'}
        </button>
      )}
    </div>
  )
}

// ── Pantalla de selección ─────────────────────────────────────────────────────
const MODOS = [
  {
    id: 'constitucion',
    titulo: 'Constitución Española',
    descripcion: 'Preguntas sobre los 169 artículos',
    icono: '📜',
    gradient: 'from-brand-700 to-brand-500',
  },
  {
    id: 'policia-local',
    titulo: 'Policía Local',
    descripcion: '40 temas · Preguntas por sección',
    icono: '👮',
    gradient: 'from-indigo-700 to-indigo-500',
  },
]

export default function Quiz() {
  const [modo, setModo] = useState(null) // null | 'constitucion' | 'policia-local'
  const [temasCons, setTemasCons] = useState([])
  const [temaSeleccionado, setTemaSeleccionado] = useState(null)
  const [temasPoliciaOk, setTemasPoliciaOk] = useState(0)

  useEffect(() => {
    apiFetch('/api/quiz/temas').then(r => r.json()).then(setTemasCons).catch(() => {})
    const ok = Object.keys(localStorage).filter(k => k.startsWith('quiz_ok_policia-local_')).length
    setTemasPoliciaOk(ok)
  }, [])

  // Fetch preguntas constitución
  const fetchConstitucion = useCallback(() => {
    const url = temaSeleccionado
      ? `/api/quiz?limite=${TOTAL}&tema=${encodeURIComponent(temaSeleccionado)}`
      : `/api/quiz?limite=${TOTAL}`
    return apiFetch(url).then(r => r.json())
  }, [temaSeleccionado])

  // Fetch preguntas policía local
  const fetchPolicia = useCallback(() =>
    apiFetch(`/api/oposiciones/policia-local/quiz?limite=${TOTAL}`).then(r => r.json())
  , [])

  // ── Selector de modo ─────────────────────────────────────────────────────
  if (!modo) {
    return (
      <div className="max-w-xl mx-auto">
        <h1 className="text-xl font-bold text-brand-700 mb-1">Test</h1>
        <p className="text-sm text-gray-400 mb-5">Elige de qué quieres hacer el test</p>

        <div className="space-y-3 mb-6">
          {MODOS.map(m => (
            <button
              key={m.id}
              onClick={() => setModo(m.id)}
              className={`w-full bg-gradient-to-r ${m.gradient} rounded-2xl p-4 flex items-center gap-4 shadow-md active:opacity-90`}
            >
              <span className="text-4xl shrink-0">{m.icono}</span>
              <div className="text-left flex-1">
                <p className="font-bold text-white">{m.titulo}</p>
                <p className="text-white/60 text-xs mt-0.5">{m.descripcion}</p>
              </div>
              <span className="text-white/40 text-xl">›</span>
            </button>
          ))}
        </div>

        {/* Resumen progreso */}
        <div className="card">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">Tu progreso en tests</p>
          <div className="flex items-center gap-3">
            <span className="text-2xl">👮</span>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-700">{temasPoliciaOk}/40 temas Policía Local superados</p>
              <div className="mt-1 bg-gray-100 rounded-full h-1.5">
                <div className="bg-indigo-500 h-1.5 rounded-full" style={{ width: `${temasPoliciaOk / 40 * 100}%` }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // ── Sub-selector Constitución (por tema) ─────────────────────────────────
  if (modo === 'constitucion-selector') {
    return (
      <div className="max-w-xl mx-auto">
        <button onClick={() => setModo(null)} className="text-xs text-gray-400 mb-4">← Volver</button>
        <h2 className="text-lg font-bold text-brand-700 mb-4">Elige el tema</h2>
        <div className="space-y-2 mb-4">
          <button onClick={() => { setTemaSeleccionado(null); setModo('constitucion') }}
            className={`w-full text-left px-4 py-3 rounded-xl border-2 text-sm ${!temaSeleccionado ? 'border-brand-500 bg-brand-50 text-brand-700 font-semibold' : 'border-gray-200 text-gray-700'}`}>
            🎯 Todos los temas
          </button>
          {temasCons.map(t => (
            <button key={t.tema} onClick={() => { setTemaSeleccionado(t.tema); setModo('constitucion') }}
              className={`w-full text-left px-4 py-3 rounded-xl border-2 text-sm ${temaSeleccionado === t.tema ? 'border-brand-500 bg-brand-50 text-brand-700 font-semibold' : 'border-gray-200 text-gray-700'}`}>
              {t.tema} <span className="text-xs text-gray-400">({t.preguntas})</span>
            </button>
          ))}
        </div>
      </div>
    )
  }

  // ── Quiz activo ──────────────────────────────────────────────────────────
  if (modo === 'constitucion') {
    return <QuizEngine
      titulo="Constitución"
      fetchPreguntas={fetchConstitucion}
      onSalir={() => setModo(null)}
    />
  }

  if (modo === 'policia-local') {
    return <QuizEngine
      titulo="Policía Local"
      fetchPreguntas={fetchPolicia}
      onSalir={() => setModo(null)}
    />
  }

  return null
}
