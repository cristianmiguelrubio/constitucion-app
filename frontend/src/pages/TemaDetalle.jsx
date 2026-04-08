import { useEffect, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import TextoFormateado from '../components/TextoFormateado'
import { apiFetch } from '../utils/api'

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
  const [tema, setTema] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [vista, setVista] = useState('contenido')
  const [quiz, setQuiz] = useState(null)
  const [respuestas, setRespuestas] = useState({})
  const [enviado, setEnviado] = useState(false)
  const [completado, setCompletado] = useState(false)

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
    const token = localStorage.getItem('token')
    apiFetch(`/api/oposiciones/${slug}/temas/${numero}/quiz?limite=20`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })
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
        }
        setEnviado(true)
      }
      return nuevo
    })
  }

  const aciertos = quiz ? quiz.filter(p => respuestas[p.id] === 'correcta').length : 0
  const pct = quiz ? Math.round((aciertos / quiz.length) * 100) : 0

  const enviarQuiz = () => {
    setEnviado(true)
    if (quiz && aciertos / quiz.length >= 0.3) {
      localStorage.setItem(clavePregunta(slug, numero), '1')
      setCompletado(true)
    }
  }

  // Agrupar preguntas del quiz por sección
  const seccionesQuiz = quiz ? quiz.reduce((acc, p) => {
    const sec = p.seccion || 'General'
    if (!acc[sec]) acc[sec] = []
    acc[sec].push(p)
    return acc
  }, {}) : {}

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
            onClick={() => tab.id === 'quiz' ? cargarQuiz() : setVista(tab.id)}
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
          {/* Info test */}
          {!enviado && (
            <div className="bg-brand-50 border border-brand-100 rounded-xl px-4 py-3 mb-4 flex items-center gap-3">
              <span className="text-2xl">🧠</span>
              <div>
                <p className="text-sm font-semibold text-brand-700">{quiz.length} preguntas</p>
                <p className="text-xs text-brand-500">Necesitas un 30% para superar el test</p>
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
                        <p className="font-semibold text-sm text-gray-800 mb-3">
                          {n}. {p.pregunta}
                        </p>
                        <div className="space-y-2">
                          {p.opciones.map(({ key, texto }) => {
                            const elegida = respuestas[p.id] === key
                            const esCorrecta = key === 'correcta'
                            const yaRespondida = !!respuestas[p.id]
                            let cls = 'w-full text-left px-3 py-2.5 rounded-xl border text-[13px] leading-snug transition-colors '
                            if (!yaRespondida) {
                              cls += 'border-gray-200 text-gray-700 active:bg-gray-50'
                            } else {
                              if (esCorrecta) cls += 'border-green-400 bg-green-50 text-green-700 font-medium'
                              else if (elegida) cls += 'border-red-300 bg-red-50 text-red-600'
                              else cls += 'border-gray-100 text-gray-400'
                            }
                            return (
                              <button key={key} onClick={() => elegir(p.id, key)} className={cls}>
                                {yaRespondida && esCorrecta && <span className="mr-1.5">✓</span>}
                                {yaRespondida && elegida && !esCorrecta && <span className="mr-1.5">✗</span>}
                                {texto}
                              </button>
                            )
                          })}
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            )
          })}

          {/* Progreso y resultado */}
          {!enviado && (
            <div className="text-center text-xs text-gray-400 py-2">
              {Object.keys(respuestas).length}/{quiz.length} preguntas respondidas
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
        <button
          onClick={() => navigate(`/oposiciones/${slug}/temas/${num + 1}`)}
          className="flex-1 py-3 border border-gray-200 rounded-xl text-sm text-brand-500 font-medium active:bg-gray-50"
        >
          Tema {num + 1} →
        </button>
      </div>
    </div>
  )
}
