import { useState, useEffect, useRef } from 'react'
import { apiFetch } from '../utils/api'
import { useNavigate } from 'react-router-dom'
import TutorIA from '../components/TutorIA'

const TIEMPO_TOTAL = 30 * 60 // 30 minutos en segundos

function formatTiempo(seg) {
  const m = Math.floor(seg / 60).toString().padStart(2, '0')
  const s = (seg % 60).toString().padStart(2, '0')
  return `${m}:${s}`
}

export default function Simulacro({ usuario }) {
  const navigate = useNavigate()
  const [fase, setFase] = useState('config') // config | examen | resultado
  const [tipo, setTipo] = useState('constitucion')
  const [nPreguntas, setNPreguntas] = useState(65)
  const [preguntas, setPreguntas] = useState([])
  const [respuestas, setRespuestas] = useState({}) // id -> opcion elegida
  const [indice, setIndice] = useState(0)
  const [tiempoRestante, setTiempoRestante] = useState(TIEMPO_TOTAL)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState('')
  const [resultado, setResultado] = useState(null)
  const [bloqueado, setBloqueado] = useState(false)
  const timerRef = useRef(null)

  // Verificar acceso premium
  useEffect(() => {
    apiFetch('/api/plan').then(r => r.json()).then(data => {
      if (!data.premium) setBloqueado(true)
    }).catch(() => {})
  }, [])

  const iniciarSimulacro = async () => {
    setCargando(true)
    setError('')
    try {
      const r = await apiFetch(`/api/simulacros/preguntas?tipo=${tipo}&n=${nPreguntas}`)
      if (r.status === 403) { setBloqueado(true); return }
      if (!r.ok) { setError('Error al cargar preguntas'); return }
      const data = await r.json()
      setPreguntas(data)
      setRespuestas({})
      setIndice(0)
      setTiempoRestante(TIEMPO_TOTAL)
      setFase('examen')
    } catch {
      setError('Error de conexión')
    } finally {
      setCargando(false)
    }
  }

  // Timer del examen
  useEffect(() => {
    if (fase !== 'examen') return
    timerRef.current = setInterval(() => {
      setTiempoRestante(t => {
        if (t <= 1) { clearInterval(timerRef.current); return 0 }
        return t - 1
      })
    }, 1000)
    return () => clearInterval(timerRef.current)
  }, [fase])

  // Finalizar cuando el temporizador llega a 0
  useEffect(() => {
    if (fase === 'examen' && tiempoRestante === 0) {
      finalizarSimulacro()
    }
    // finalizarSimulacro se omite de deps: el efecto re-corre cada segundo
    // y captura la versión más reciente al llegar a 0
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tiempoRestante, fase])

  const finalizarSimulacro = async () => {
    clearInterval(timerRef.current)
    let correctas = 0, incorrectas = 0, en_blanco = 0
    preguntas.forEach(p => {
      const r = respuestas[p.id]
      if (!r) en_blanco++
      else if (r === p.correcta) correctas++
      else incorrectas++
    })
    const tiempoUsado = TIEMPO_TOTAL - tiempoRestante
    const puntuacion = correctas - (incorrectas / 3)

    setResultado({ correctas, incorrectas, en_blanco, puntuacion: puntuacion.toFixed(2), tiempoUsado })
    setFase('resultado')

    await apiFetch('/api/simulacros', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tipo, correctas, incorrectas, en_blanco, tiempo_segundos: tiempoUsado }),
    }).catch(() => {})
  }

  const elegirRespuesta = (id, opcion) => {
    setRespuestas(prev => ({ ...prev, [id]: opcion }))
  }

  if (bloqueado) return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md text-center">
        <div className="text-5xl mb-4">🔒</div>
        <h2 className="text-xl font-bold text-gray-800 mb-2">Acceso premium requerido</h2>
        <p className="text-gray-500 mb-6">Los simulacros de examen oficial requieren un plan de pago.</p>
        <button onClick={() => navigate('/planes')} className="bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold hover:bg-blue-700">
          Ver planes
        </button>
      </div>
    </div>
  )

  if (fase === 'config') return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md w-full">
        <h1 className="text-2xl font-bold text-gray-800 mb-1">Simulacro oficial</h1>
        <p className="text-gray-500 mb-6 text-sm">Examen cronometrado con penalización 1/3</p>

        <div className="mb-5">
          <label className="block text-sm font-medium text-gray-700 mb-2">Tipo de examen</label>
          <div className="grid grid-cols-3 gap-2">
            {[['constitucion','Constitución','📜'], ['policia-local','Policía Local','👮'], ['mixto','Mixto','🎯']].map(([val, label, emoji]) => (
              <button key={val} onClick={() => setTipo(val)}
                className={`py-2 px-3 rounded-xl border-2 text-sm font-medium transition-colors ${tipo === val ? 'border-blue-500 bg-blue-50 text-blue-700' : 'border-gray-200 text-gray-600 hover:border-gray-300'}`}>
                {emoji} {label}
              </button>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Número de preguntas: <span className="text-blue-600 font-bold">{nPreguntas}</span></label>
          <input type="range" min={10} max={100} step={5} value={nPreguntas}
            onChange={e => setNPreguntas(Number(e.target.value))}
            className="w-full accent-blue-600" />
          <div className="flex justify-between text-xs text-gray-400 mt-1"><span>10</span><span>65 (oficial)</span><span>100</span></div>
        </div>

        <div className="bg-amber-50 border border-amber-200 rounded-xl p-3 mb-6 text-sm text-amber-700">
          <strong>Reglas:</strong> 30 minutos · Cada error descuenta 1/3 de acierto · En blanco no penaliza
        </div>

        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

        <button onClick={iniciarSimulacro} disabled={cargando}
          className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold text-lg hover:bg-blue-700 disabled:opacity-50 transition-colors">
          {cargando ? 'Cargando...' : 'Comenzar examen'}
        </button>
      </div>
    </div>
  )

  if (fase === 'examen') {
    const pregunta = preguntas[indice]
    const respondidas = Object.keys(respuestas).length
    const pct = Math.round((respondidas / preguntas.length) * 100)
    const tiempoUrgente = tiempoRestante < 300

    return (
      <div className="min-h-screen bg-gray-50 pb-20">
        {/* Header fijo */}
        <div className={`sticky top-0 z-10 px-4 py-3 shadow-sm ${tiempoUrgente ? 'bg-red-600' : 'bg-blue-600'} text-white`}>
          <div className="flex items-center justify-between max-w-2xl mx-auto">
            <span className="text-sm font-medium">{indice + 1}/{preguntas.length}</span>
            <span className="text-2xl font-mono font-bold">{formatTiempo(tiempoRestante)}</span>
            <span className="text-sm">{respondidas} resp.</span>
          </div>
          <div className="mt-2 bg-white/30 rounded-full h-1.5 max-w-2xl mx-auto">
            <div className="bg-white rounded-full h-1.5 transition-all" style={{ width: `${pct}%` }} />
          </div>
        </div>

        <div className="max-w-2xl mx-auto px-4 py-6">
          <p className="text-gray-800 font-medium text-base leading-relaxed mb-6 whitespace-normal break-words">
            {pregunta.pregunta}
          </p>

          <div className="space-y-3">
            {pregunta.opciones.map((op, i) => {
              const letra = ['A', 'B', 'C', 'D'][i]
              const elegida = respuestas[pregunta.id] === op
              return (
                <button key={i} onClick={() => elegirRespuesta(pregunta.id, op)}
                  className={`w-full text-left px-4 py-3 rounded-xl border-2 transition-colors text-sm whitespace-normal break-words
                    ${elegida ? 'border-blue-500 bg-blue-50 text-blue-800 font-medium' : 'border-gray-200 bg-white text-gray-700 hover:border-blue-300'}`}>
                  <span className="font-bold mr-2">{letra}.</span>{op}
                </button>
              )
            })}
          </div>

          {/* Nav preguntas */}
          <div className="flex justify-between mt-8 gap-3">
            <button onClick={() => setIndice(i => Math.max(0, i - 1))} disabled={indice === 0}
              className="flex-1 py-2.5 rounded-xl border border-gray-200 text-sm font-medium text-gray-600 disabled:opacity-40 hover:bg-gray-50">
              ← Anterior
            </button>
            {indice < preguntas.length - 1 ? (
              <button onClick={() => setIndice(i => i + 1)}
                className="flex-1 py-2.5 rounded-xl bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700">
                Siguiente →
              </button>
            ) : (
              <button onClick={finalizarSimulacro}
                className="flex-1 py-2.5 rounded-xl bg-green-600 text-white text-sm font-semibold hover:bg-green-700">
                Entregar examen
              </button>
            )}
          </div>

          {/* Mapa de preguntas */}
          <div className="mt-6">
            <p className="text-xs text-gray-500 mb-2">Navegar por pregunta:</p>
            <div className="flex flex-wrap gap-1.5">
              {preguntas.map((p, i) => (
                <button key={i} onClick={() => setIndice(i)}
                  className={`w-8 h-8 rounded-lg text-xs font-bold transition-colors
                    ${i === indice ? 'bg-blue-600 text-white' : respuestas[p.id] ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
                  {i + 1}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (fase === 'resultado' && resultado) {
    const nota = parseFloat(resultado.puntuacion)
    const aprobado = nota >= (nPreguntas * 0.5)
    const falladas = preguntas.filter(p => respuestas[p.id] && respuestas[p.id] !== p.correcta)
    const enBlanco = preguntas.filter(p => !respuestas[p.id])
    return (
      <div className="bg-gray-50 min-h-screen pb-10">
        <div className="max-w-2xl mx-auto px-4 pt-6">
          {/* Cabecera resultado */}
          <div className="bg-white rounded-2xl shadow-sm p-6 mb-4 text-center">
            <div className="text-5xl mb-2">{aprobado ? '🎉' : '📚'}</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-0.5">{aprobado ? '¡Aprobado!' : 'Sigue practicando'}</h2>
            <p className="text-gray-400 text-sm">Tiempo: {formatTiempo(resultado.tiempoUsado)}</p>

            <div className="mt-4 mb-2">
              <span className={`text-5xl font-black ${aprobado ? 'text-green-600' : 'text-red-500'}`}>{nota}</span>
              <span className="text-gray-400 text-lg ml-1">/ {nPreguntas}</span>
            </div>
            <p className="text-xs text-gray-400 mb-4">Aciertos − (Errores ÷ 3) = {nota}</p>

            <div className="grid grid-cols-3 gap-2 text-center">
              <div className="bg-green-50 rounded-xl p-3">
                <div className="text-2xl font-bold text-green-600">{resultado.correctas}</div>
                <div className="text-xs text-green-500 mt-0.5">Correctas</div>
              </div>
              <div className="bg-red-50 rounded-xl p-3">
                <div className="text-2xl font-bold text-red-500">{resultado.incorrectas}</div>
                <div className="text-xs text-red-400 mt-0.5">Incorrectas</div>
              </div>
              <div className="bg-gray-100 rounded-xl p-3">
                <div className="text-2xl font-bold text-gray-500">{resultado.en_blanco}</div>
                <div className="text-xs text-gray-400 mt-0.5">En blanco</div>
              </div>
            </div>

            <div className="flex gap-3 mt-5">
              <button onClick={() => setFase('config')} className="flex-1 py-2.5 border border-gray-200 rounded-xl text-sm font-medium text-gray-600">
                Nuevo simulacro
              </button>
              <button onClick={() => navigate('/')} className="flex-1 py-2.5 bg-brand-700 text-white rounded-xl text-sm font-semibold">
                Inicio
              </button>
            </div>
          </div>

          {/* Repaso de fallos */}
          {falladas.length > 0 && (
            <div className="mb-4">
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3 px-1">
                Preguntas falladas ({falladas.length})
              </p>
              <div className="space-y-3">
                {falladas.map((p, i) => (
                  <div key={p.id} className="bg-white rounded-2xl shadow-sm p-4 border-l-4 border-red-400">
                    <p className="text-sm font-medium text-gray-800 mb-3 leading-relaxed">{i + 1}. {p.pregunta}</p>
                    <div className="space-y-1.5 mb-2">
                      {p.opciones.map((op, oi) => {
                        const esCorrecta = op === p.correcta
                        const elegida = respuestas[p.id] === op
                        return (
                          <div key={oi} className={`px-3 py-2 rounded-xl text-xs leading-relaxed flex gap-2 items-start
                            ${esCorrecta ? 'bg-green-50 text-green-700 font-medium' : elegida ? 'bg-red-50 text-red-600' : 'text-gray-400'}`}>
                            <span className="shrink-0 font-bold">{esCorrecta ? '✓' : elegida ? '✗' : ['A','B','C','D'][oi]+'.'}</span>
                            <span className="whitespace-normal break-words">{op}</span>
                          </div>
                        )
                      })}
                    </div>
                    <TutorIA pregunta={p.pregunta} respuestaUsuario={respuestas[p.id]} respuestaCorrecta={p.correcta} />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* En blanco */}
          {enBlanco.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3 px-1">
                Sin responder ({enBlanco.length})
              </p>
              <div className="space-y-2">
                {enBlanco.map((p, i) => (
                  <div key={p.id} className="bg-white rounded-xl p-3 border border-gray-100">
                    <p className="text-sm text-gray-600 leading-relaxed">{i + 1}. {p.pregunta}</p>
                    <p className="text-xs text-green-600 font-medium mt-1.5">✓ {p.correcta}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    )
  }

  return null
}
