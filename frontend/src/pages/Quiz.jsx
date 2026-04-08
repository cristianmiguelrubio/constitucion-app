import { useEffect, useState, useCallback } from 'react'

const TOTAL_PREGUNTAS = 10

export default function Quiz() {
  const [fase, setFase] = useState('selector') // selector | jugando | resultado
  const [temas, setTemas] = useState([])
  const [temaSeleccionado, setTemaSeleccionado] = useState(null) // null = todos
  const [preguntas, setPreguntas] = useState([])
  const [indice, setIndice] = useState(0)
  const [seleccionada, setSeleccionada] = useState(null)
  const [correctas, setCorrectas] = useState(0)
  const [historial, setHistorial] = useState([])
  const [cargando, setCargando] = useState(false)

  // Cargar temas disponibles
  useEffect(() => {
    fetch('/api/quiz/temas')
      .then(r => r.json())
      .then(setTemas)
      .catch(() => {})
  }, [])

  const iniciarQuiz = useCallback(() => {
    setCargando(true)
    const url = temaSeleccionado
      ? `/api/quiz?limite=${TOTAL_PREGUNTAS}&tema=${encodeURIComponent(temaSeleccionado)}`
      : `/api/quiz?limite=${TOTAL_PREGUNTAS}`

    fetch(url)
      .then(r => r.json())
      .then(data => {
        const mezcladas = data.map(p => ({
          ...p,
          opciones: [...p.opciones].sort(() => Math.random() - 0.5),
        }))
        setPreguntas(mezcladas)
        setIndice(0)
        setSeleccionada(null)
        setCorrectas(0)
        setHistorial([])
        setFase('jugando')
        setCargando(false)
      })
      .catch(() => setCargando(false))
  }, [temaSeleccionado])

  const responder = (opcion) => {
    if (seleccionada) return
    setSeleccionada(opcion)
    const p = preguntas[indice]
    if (opcion === p.respuesta_correcta) setCorrectas(c => c + 1)
    setHistorial(h => [...h, {
      pregunta: p.pregunta,
      correcta: p.respuesta_correcta,
      elegida: opcion,
      articulo: p.articulo,
    }])
  }

  const siguiente = () => {
    if (indice + 1 >= preguntas.length) {
      setFase('resultado')
    } else {
      setIndice(i => i + 1)
      setSeleccionada(null)
    }
  }

  const reiniciar = () => {
    setFase('selector')
    setPreguntas([])
  }

  // ── Selector de tema ──────────────────────────────────────────────────────
  if (fase === 'selector') {
    return (
      <div className="max-w-xl mx-auto">
        <h1 className="text-xl font-bold text-brand-700 mb-2">Test de la Constitución</h1>
        <p className="text-sm text-gray-500 mb-6">{TOTAL_PREGUNTAS} preguntas · 4 opciones · Corrección inmediata</p>

        <div className="card mb-4">
          <h2 className="font-semibold text-gray-700 mb-3">Elige el tema</h2>
          <div className="space-y-2">
            {/* Opción: todos los temas */}
            <button
              onClick={() => setTemaSeleccionado(null)}
              className={`w-full text-left px-4 py-3 rounded-xl border-2 transition-all text-sm ${
                temaSeleccionado === null
                  ? 'border-brand-500 bg-brand-50 text-brand-700 font-semibold'
                  : 'border-gray-200 hover:border-brand-300 text-gray-700'
              }`}
            >
              <span className="mr-2">🎯</span>
              <span className="font-medium">Todos los temas</span>
              <span className="ml-2 text-xs text-gray-400">({temas.reduce((s, t) => s + t.preguntas, 0)} preguntas)</span>
            </button>

            {/* Temas específicos */}
            {temas.map(t => (
              <button
                key={t.tema}
                onClick={() => setTemaSeleccionado(t.tema)}
                className={`w-full text-left px-4 py-3 rounded-xl border-2 transition-all text-sm ${
                  temaSeleccionado === t.tema
                    ? 'border-brand-500 bg-brand-50 text-brand-700 font-semibold'
                    : 'border-gray-200 hover:border-brand-300 text-gray-700'
                }`}
              >
                <span className="font-medium">{t.tema}</span>
                <span className="ml-2 text-xs text-gray-400">({t.preguntas} preguntas)</span>
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={iniciarQuiz}
          disabled={cargando}
          className="btn-primary w-full py-3 text-base disabled:opacity-60"
        >
          {cargando ? 'Preparando...' : `Empezar test${temaSeleccionado ? ` · ${temaSeleccionado.split('.')[0]}` : ''} →`}
        </button>
      </div>
    )
  }

  // ── Resultado ─────────────────────────────────────────────────────────────
  if (fase === 'resultado') {
    const porcentaje = Math.round((correctas / preguntas.length) * 100)
    const nivel = porcentaje >= 80 ? 'Excelente' : porcentaje >= 60 ? 'Bien' : porcentaje >= 40 ? 'Regular' : 'Sigue practicando'
    const colorNivel = porcentaje >= 80 ? 'text-green-600' : porcentaje >= 60 ? 'text-blue-600' : porcentaje >= 40 ? 'text-amber-600' : 'text-red-500'

    return (
      <div className="max-w-xl mx-auto">
        <div className="card text-center mb-6">
          <div className="text-5xl mb-3">{porcentaje >= 80 ? '🏆' : porcentaje >= 60 ? '👍' : porcentaje >= 40 ? '📚' : '💪'}</div>
          <h2 className="text-2xl font-bold text-brand-700 mb-1">{correctas} / {preguntas.length}</h2>
          {temaSeleccionado && <p className="text-xs text-gray-400 mb-1">{temaSeleccionado}</p>}
          <p className={`text-lg font-semibold mb-4 ${colorNivel}`}>{nivel}</p>
          <div className="w-full bg-gray-100 rounded-full h-3 mb-4">
            <div
              className={`h-3 rounded-full transition-all ${porcentaje >= 80 ? 'bg-green-500' : porcentaje >= 60 ? 'bg-blue-500' : porcentaje >= 40 ? 'bg-amber-400' : 'bg-red-400'}`}
              style={{ width: `${porcentaje}%` }}
            />
          </div>
          <div className="flex gap-2">
            <button onClick={iniciarQuiz} className="btn-primary flex-1">Repetir</button>
            <button onClick={reiniciar} className="flex-1 border border-gray-200 text-gray-600 hover:bg-gray-50 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
              Cambiar tema
            </button>
          </div>
        </div>

        <h3 className="font-semibold text-gray-600 mb-3">Repaso de respuestas</h3>
        <div className="space-y-3">
          {historial.map((h, i) => (
            <div key={i} className={`card border-l-4 ${h.elegida === h.correcta ? 'border-green-400' : 'border-red-400'}`}>
              <p className="text-xs text-gray-400 mb-1">Art. {h.articulo}</p>
              <p className="text-sm font-medium text-gray-700 mb-2">{h.pregunta}</p>
              {h.elegida !== h.correcta && (
                <p className="text-xs text-red-500 mb-1">Tu respuesta: {h.elegida}</p>
              )}
              <p className="text-xs text-green-600 font-medium">✓ {h.correcta}</p>
            </div>
          ))}
        </div>
      </div>
    )
  }

  // ── Pregunta activa ───────────────────────────────────────────────────────
  if (preguntas.length === 0) return <p className="text-center text-gray-400 mt-16">Sin preguntas para este tema.</p>

  const pregunta = preguntas[indice]
  return (
    <div className="max-w-xl mx-auto">
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm text-gray-400">
          {temaSeleccionado ? temaSeleccionado.split('.')[0] + ' · ' : ''}
          {indice + 1}/{preguntas.length}
        </span>
        <span className="text-sm font-medium text-green-600">{correctas} correctas</span>
      </div>
      <div className="w-full bg-gray-100 rounded-full h-1.5 mb-5">
        <div
          className="bg-brand-500 h-1.5 rounded-full transition-all"
          style={{ width: `${(indice / preguntas.length) * 100}%` }}
        />
      </div>

      <div className="card mb-4">
        <p className="text-xs text-gray-400 mb-2">Artículo {pregunta.articulo}</p>
        <p className="font-semibold text-gray-800 leading-snug">{pregunta.pregunta}</p>
      </div>

      <div className="space-y-2 mb-5">
        {pregunta.opciones.map((opcion, i) => {
          let clases = 'w-full text-left px-4 py-3 rounded-xl border-2 text-sm font-medium transition-all '
          if (!seleccionada) {
            clases += 'border-gray-200 hover:border-brand-500 hover:bg-blue-50 text-gray-700'
          } else if (opcion === pregunta.respuesta_correcta) {
            clases += 'border-green-400 bg-green-50 text-green-800'
          } else if (opcion === seleccionada) {
            clases += 'border-red-400 bg-red-50 text-red-700'
          } else {
            clases += 'border-gray-100 bg-gray-50 text-gray-400'
          }
          return (
            <button key={i} onClick={() => responder(opcion)} className={clases}>
              <span className="mr-2 font-bold text-gray-400">{String.fromCharCode(65 + i)}.</span>
              {opcion}
              {seleccionada && opcion === pregunta.respuesta_correcta && ' ✓'}
              {seleccionada && opcion === seleccionada && opcion !== pregunta.respuesta_correcta && ' ✗'}
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
