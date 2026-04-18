import { useEffect, useState, useRef } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import TextoFormateado from '../components/TextoFormateado'
import { apiFetch } from '../utils/api'
import { usePlan } from '../hooks/usePlan'
import TutorIA from '../components/TutorIA'

const COLORES_NUM = [
  'bg-brand-100 text-brand-700',
  'bg-indigo-100 text-indigo-700',
  'bg-emerald-100 text-emerald-700',
  'bg-amber-100 text-amber-700',
  'bg-rose-100 text-rose-700',
  'bg-purple-100 text-purple-700',
  'bg-teal-100 text-teal-700',
]

const COLORES_SEC = [
  { bg: 'bg-brand-50',   border: 'border-brand-300',   text: 'text-brand-700'   },
  { bg: 'bg-indigo-50',  border: 'border-indigo-300',  text: 'text-indigo-700'  },
  { bg: 'bg-emerald-50', border: 'border-emerald-300', text: 'text-emerald-700' },
  { bg: 'bg-amber-50',   border: 'border-amber-300',   text: 'text-amber-700'   },
  { bg: 'bg-rose-50',    border: 'border-rose-300',    text: 'text-rose-700'    },
]

function clavePregunta(slug, numero) {
  return `quiz_ok_${slug}_${numero}`
}

export default function TemaDetalle() {
  const { slug, numero } = useParams()
  const navigate = useNavigate()
  const plan = usePlan()
  const [tema, setTema] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [vista, setVista] = useState('contenido')
  const [quiz, setQuiz] = useState(null)
  const [respuestas, setRespuestas] = useState({})
  const [enviado, setEnviado] = useState(false)
  const [completado, setCompletado] = useState(false)
  const [cronometro, setCronometro] = useState(0)
  const cronRef = useRef(null)

  const num = parseInt(numero)

  useEffect(() => {
    setCargando(true)
    setCompletado(!!localStorage.getItem(clavePregunta(slug, numero)))
    apiFetch(`/api/oposiciones/${slug}/temas/${numero}`)
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(data => { setTema(data); setCargando(false) })
      .catch(() => setCargando(false))
  }, [slug, numero])

  const cargarQuiz = () => {
    apiFetch(`/api/oposiciones/${slug}/temas/${numero}/quiz?limite=20`)
      .then(r => r.json())
      .then(data => {
        // Mezclar las opciones de cada pregunta manteniendo rastro de cuál es correcta
        const mezcladas = data.map(p => {
          const opciones = [
            { key: 'correcta', texto: p.respuesta_correcta },
            { key: 'b', texto: p.opcion_b },
            { key: 'c', texto: p.opcion_c },
            { key: 'd', texto: p.opcion_d },
          ]
          // Mezclar
          for (let i = opciones.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [opciones[i], opciones[j]] = [opciones[j], opciones[i]]
          }
          return { ...p, opciones }
        })
        setQuiz(mezcladas)
        setRespuestas({})
        setEnviado(false)
        setCronometro(0)
        clearInterval(cronRef.current)
        cronRef.current = setInterval(() => setCronometro(s => s + 1), 1000)
        setVista('quiz')
      })
  }

  const elegir = (pregId, key) => {
    if (respuestas[pregId]) return  // ya respondida
    setRespuestas(prev => {
      const nuevo = { ...prev, [pregId]: key }
      if (quiz && Object.keys(nuevo).length === quiz.length) {
        const ac = quiz.filter(p => nuevo[p.id] === 'correcta').length
        if (ac / quiz.length >= 0.3) {
          localStorage.setItem(clavePregunta(slug, numero), '1')
          setCompletado(true)
          // Sincronizar con servidor
          apiFetch(`/api/temas-completados?slug=${slug}&numero=${numero}`, { method: 'POST' }).catch(() => {})
        }
        clearInterval(cronRef.current)
        setEnviado(true)
      }
      return nuevo
    })
  }

  const aciertos = quiz ? quiz.filter(p => respuestas[p.id] === 'correcta').length : 0
  const pct = quiz ? Math.round((aciertos / quiz.length) * 100) : 0

  const enviarQuiz = () => {
    clearInterval(cronRef.current)
    setEnviado(true)
    if (quiz && aciertos / quiz.length >= 0.3) {
      localStorage.setItem(clavePregunta(slug, numero), '1')
      setCompletado(true)
      apiFetch(`/api/temas-completados?slug=${slug}&numero=${numero}`, { method: 'POST' }).catch(() => {})
    }
  }

  // Agrupar preguntas del quiz por sección
  const seccionesQuiz = quiz ? quiz.reduce((acc, p) => {
    const sec = p.seccion || 'General'
    if (!acc[sec]) acc[sec] = []
    acc[sec].push(p)
    return acc
  }, {}) : {}

  // Trial: bloquear temas > 1
  if (plan && plan.es_trial && num > 1) {
    return (
      <div className="max-w-xl mx-auto">
        <div className="flex items-center gap-1 text-xs text-gray-400 mb-3">
          <Link to="/oposiciones" className="hover:text-brand-500">Oposiciones</Link>
          <span>/</span>
          <Link to={`/oposiciones/${slug}`} className="hover:text-brand-500 capitalize">{slug.replace(/-/g,' ')}</Link>
          <span>/</span>
          <span className="text-gray-600">Tema {numero}</span>
        </div>
        <div className="min-h-[60vh] flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-lg p-8 max-w-sm w-full text-center border border-gray-100">
            <div className="w-16 h-16 bg-amber-50 rounded-2xl flex items-center justify-center mx-auto mb-4 text-3xl">🔒</div>
            <h2 className="text-lg font-bold text-gray-800 mb-2">Solo disponible con suscripción</h2>
            <p className="text-gray-500 text-sm mb-2 leading-relaxed">
              Tu periodo de prueba incluye acceso al <strong>Tema 1</strong> de cada oposición.
            </p>
            <p className="text-gray-400 text-sm mb-6">
              Suscríbete para desbloquear los {slug === 'policia-local' ? '40' : 'todos los'} temas completos con test.
            </p>
            <button
              onClick={() => navigate('/planes')}
              className="w-full bg-gray-900 text-white py-3 rounded-xl font-semibold text-sm hover:bg-gray-800 transition-colors mb-3">
              Ver planes →
            </button>
            <button
              onClick={() => navigate(`/oposiciones/${slug}/temas/1`)}
              className="w-full border border-gray-200 text-gray-600 py-2.5 rounded-xl text-sm font-medium">
              ← Ir al Tema 1
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (cargando) return (
    <div className="flex justify-center mt-24">
      <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  if (!tema) return (
    <div className="card text-center mt-16">
      <p className="text-red-500">Tema no encontrado</p>
      <Link to={`/oposiciones/${slug}`} className="text-brand-500 text-sm mt-2 inline-block">← Volver</Link>
    </div>
  )

  let numPregGlobal = 0

  return (
    <div className="max-w-2xl mx-auto">
      {/* Breadcrumb */}
      <div className="flex items-center gap-1 text-xs text-gray-400 mb-3 overflow-x-auto whitespace-nowrap pb-1">
        <Link to="/oposiciones" className="hover:text-brand-500 shrink-0">Oposiciones</Link>
        <span>/</span>
        <Link to={`/oposiciones/${slug}`} className="hover:text-brand-500 shrink-0 capitalize">{slug.replace(/-/g,' ')}</Link>
        <span>/</span>
        <span className="text-gray-600">Tema {numero}</span>
      </div>

      {/* Cabecera */}
      <div className="card mb-4 flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h1 className="text-xl font-bold text-brand-700 mb-0.5">Tema {numero}</h1>
          <p className="text-sm text-gray-600 leading-snug">{tema.titulo}</p>
        </div>
        {completado && (
          <span className="shrink-0 bg-green-100 text-green-700 text-xs font-bold px-2.5 py-1.5 rounded-xl">
            ✓ Test superado
          </span>
        )}
      </div>

      {/* Tabs */}
      <div className="flex rounded-xl overflow-hidden border border-gray-200 mb-4">
        {[
          { id: 'contenido', label: '📄 Texto' },
          { id: 'resumen',   label: '📝 Resumen' },
          { id: 'quiz',      label: completado ? '✓ Test' : '🧠 Test' },
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => { window.scrollTo(0, 0); tab.id === 'quiz' ? cargarQuiz() : setVista(tab.id) }}
            className={`flex-1 py-2.5 text-sm font-semibold transition-colors ${
              vista === tab.id
                ? 'bg-brand-700 text-white'
                : 'text-gray-500 active:bg-gray-50'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Contenido */}
      {vista === 'contenido' && (
        <div className="card mb-4">
          <TextoFormateado texto={tema.contenido} />
        </div>
      )}

      {/* Resumen */}
      {vista === 'resumen' && (
        <div className="mb-4">
          {tema.resumen ? (
            <>
              <div className="flex items-center gap-2 mb-3 px-1">
                <span className="text-lg">📝</span>
                <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
                  Puntos clave del tema
                </p>
              </div>
              <div className="space-y-2">
                {tema.resumen.split('\n\n').filter(s => s.trim().length > 10).map((frase, i) => (
                  <div key={i} className="bg-white rounded-xl border border-gray-100 shadow-sm flex gap-3 p-4">
                    <span className={`shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${COLORES_NUM[i % 7]}`}>
                      {i + 1}
                    </span>
                    <p className="text-[14px] text-gray-700 leading-relaxed">{frase.trim()}</p>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="card text-center py-10 text-gray-400">
              <p className="text-3xl mb-3">✍️</p>
              <p className="font-medium">Resumen no disponible aún</p>
            </div>
          )}
        </div>
      )}

      {/* Quiz */}
      {vista === 'quiz' && quiz && (
        <div className="mb-4">
          {/* Info test + cronómetro */}
          {!enviado && (
            <div className="bg-brand-50 border border-brand-100 rounded-xl px-4 py-3 mb-4 flex items-center gap-3">
              <span className="text-2xl">🧠</span>
              <div className="flex-1">
                <p className="text-sm font-semibold text-brand-700">{quiz.length} preguntas · mín. 30% para superar</p>
                <p className="text-xs text-brand-400">{Object.keys(respuestas).length}/{quiz.length} respondidas</p>
              </div>
              <div className="shrink-0 text-right">
                <p className="text-lg font-bold text-brand-700 tabular-nums">
                  {String(Math.floor(cronometro / 60)).padStart(2,'0')}:{String(cronometro % 60).padStart(2,'0')}
                </p>
                <p className="text-[10px] text-brand-400">tiempo</p>
              </div>
            </div>
          )}

          {/* Preguntas agrupadas por sección */}
          {Object.entries(seccionesQuiz).map(([seccion, preguntas], secIdx) => {
            const c = COLORES_SEC[secIdx % COLORES_SEC.length]
            return (
              <div key={seccion} className="mb-6">
                {/* Cabecera de sección */}
                <div className={`flex items-center gap-2 px-3 py-2 rounded-xl ${c.bg} border ${c.border} mb-3`}>
                  <span className={`text-xs font-bold uppercase tracking-wide ${c.text}`}>
                    {seccion}
                  </span>
                </div>

                <div className="space-y-3">
                  {preguntas.map(p => {
                    numPregGlobal++
                    const n = numPregGlobal
                    return (
                      <div key={p.id} className="card">
                        <p className="font-semibold text-sm text-gray-800 mb-3 leading-relaxed">
                          {n}. {p.pregunta}
                        </p>
                        <div className="space-y-2">
                          {p.opciones.map(({ key, texto }, oi) => {
                            const letra = ['A', 'B', 'C', 'D'][oi]
                            const elegida = respuestas[p.id] === key
                            const esCorrecta = key === 'correcta'
                            const yaRespondida = !!respuestas[p.id]
                            let cls = 'w-full text-left px-3 py-2.5 rounded-xl border text-[13px] leading-relaxed transition-colors flex gap-2 items-start '
                            if (!yaRespondida) {
                              cls += 'border-gray-200 text-gray-700 active:bg-gray-50'
                            } else {
                              if (esCorrecta) cls += 'border-green-400 bg-green-50 text-green-700 font-medium'
                              else if (elegida) cls += 'border-red-300 bg-red-50 text-red-600'
                              else cls += 'border-gray-100 text-gray-400'
                            }
                            return (
                              <button key={key} onClick={() => elegir(p.id, key)} className={cls}>
                                <span className="shrink-0 font-bold text-[11px] mt-0.5 w-4">
                                  {yaRespondida && esCorrecta ? '✓' : yaRespondida && elegida && !esCorrecta ? '✗' : letra+'.'}
                                </span>
                                <span className="flex-1 whitespace-normal break-words">{texto}</span>
                              </button>
                            )
                          })}
                        </div>
                        {respuestas[p.id] && respuestas[p.id] !== 'correcta' && (
                          <TutorIA
                            pregunta={p.pregunta}
                            respuestaUsuario={p.opciones.find(o => o.key === respuestas[p.id])?.texto}
                            respuestaCorrecta={p.opciones.find(o => o.key === 'correcta')?.texto}
                          />
                        )}
                      </div>
                    )
                  })}
                </div>
              </div>
            )
          })}

          {/* Progreso y botón entregar */}
          {!enviado && (
            <div className="flex items-center justify-between px-1 py-2">
              <span className="text-xs text-gray-400">{Object.keys(respuestas).length}/{quiz.length} respondidas</span>
              {Object.keys(respuestas).length > 0 && (
                <button
                  onClick={enviarQuiz}
                  className="text-xs font-semibold bg-brand-700 text-white px-4 py-2 rounded-xl active:bg-brand-900"
                >
                  Entregar test →
                </button>
              )}
            </div>
          )}
          {enviado && (
            <div className={`card text-center border-2 ${pct >= 30 ? 'border-green-300' : 'border-red-200'}`}>
              <p className="text-4xl mb-2">{pct >= 70 ? '🎉' : pct >= 30 ? '👍' : '📚'}</p>
              <p className={`text-3xl font-bold mb-1 ${pct >= 30 ? 'text-green-600' : 'text-red-500'}`}>
                {aciertos}/{quiz.length}
              </p>
              <p className={`text-lg font-semibold mb-1 ${pct >= 30 ? 'text-green-600' : 'text-red-500'}`}>
                {pct}%
              </p>
              <p className="text-xs text-gray-400 mb-1">
                ⏱ {String(Math.floor(cronometro / 60)).padStart(2,'0')}:{String(cronometro % 60).padStart(2,'0')} empleados
              </p>
              {pct >= 30 ? (
                <p className="text-sm text-green-600 font-medium">✓ Test superado — tema marcado como completado</p>
              ) : (
                <p className="text-sm text-red-500">Necesitas al menos un 30% para superar el test</p>
              )}
              <button onClick={cargarQuiz} className="mt-4 text-sm text-brand-500 font-medium">
                Repetir test →
              </button>
            </div>
          )}
        </div>
      )}

      {/* Navegación entre temas */}
      <div className="flex justify-between gap-3 mt-2 mb-8">
        {num > 1 ? (
          <button
            onClick={() => navigate(`/oposiciones/${slug}/temas/${num - 1}`)}
            className="flex-1 py-3 border border-gray-200 rounded-xl text-sm text-brand-500 font-medium active:bg-gray-50"
          >
            ← Tema {num - 1}
          </button>
        ) : (
          <Link to={`/oposiciones/${slug}`} className="flex-1 py-3 border border-gray-200 rounded-xl text-sm text-brand-500 font-medium active:bg-gray-50 text-center">
            ← Índice
          </Link>
        )}
        {plan?.es_trial ? (
          <button
            onClick={() => navigate('/planes')}
            className="flex-1 py-3 border border-amber-200 rounded-xl text-sm text-amber-600 font-medium active:bg-amber-50 flex items-center justify-center gap-1"
          >
            🔒 Tema {num + 1} →
          </button>
        ) : (
          <button
            onClick={() => navigate(`/oposiciones/${slug}/temas/${num + 1}`)}
            className="flex-1 py-3 border border-gray-200 rounded-xl text-sm text-brand-500 font-medium active:bg-gray-50"
          >
            Tema {num + 1} →
          </button>
        )}
      </div>
    </div>
  )
}
