import { useEffect, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'

export default function TemaDetalle() {
  const { slug, numero } = useParams()
  const navigate = useNavigate()
  const [tema, setTema] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [vista, setVista] = useState('contenido') // 'contenido' | 'resumen' | 'quiz'
  const [quiz, setQuiz] = useState(null)
  const [respuestas, setRespuestas] = useState({})
  const [enviado, setEnviado] = useState(false)

  const num = parseInt(numero)

  useEffect(() => {
    setCargando(true)
    fetch(`/api/oposiciones/${slug}/temas/${numero}`)
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(data => { setTema(data); setCargando(false) })
      .catch(() => setCargando(false))
  }, [slug, numero])

  const cargarQuiz = () => {
    const token = localStorage.getItem('token')
    fetch(`/api/oposiciones/${slug}/temas/${numero}/quiz`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })
      .then(r => r.json())
      .then(data => {
        setQuiz(data)
        setRespuestas({})
        setEnviado(false)
        setVista('quiz')
      })
  }

  const elegir = (pregId, opcion) => {
    if (enviado) return
    setRespuestas(prev => ({ ...prev, [pregId]: opcion }))
  }

  const calcularAciertos = () => {
    if (!quiz) return 0
    return quiz.filter(p => respuestas[p.id] === 'a').length
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

  return (
    <div className="max-w-2xl mx-auto">
      {/* Breadcrumb */}
      <div className="flex items-center gap-1 text-xs text-gray-400 mb-3 overflow-x-auto whitespace-nowrap pb-1">
        <Link to="/oposiciones" className="hover:text-brand-500 shrink-0">Oposiciones</Link>
        <span>/</span>
        <Link to={`/oposiciones/${slug}`} className="hover:text-brand-500 shrink-0">{slug}</Link>
        <span>/</span>
        <span className="text-gray-600">Tema {numero}</span>
      </div>

      {/* Cabecera */}
      <div className="card mb-4">
        <h1 className="text-xl font-bold text-brand-700 mb-0.5">Tema {numero}</h1>
        <p className="text-sm text-gray-600 leading-snug">{tema.titulo}</p>
      </div>

      {/* Tabs */}
      <div className="flex rounded-xl overflow-hidden border border-gray-200 mb-4">
        {[
          { id: 'contenido', label: '📄 Texto' },
          { id: 'resumen',   label: '📝 Resumen' },
          { id: 'quiz',      label: '🧠 Test' },
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
          {tema.contenido ? (
            <div className="text-gray-700 leading-relaxed whitespace-pre-line text-[15px]">
              {tema.contenido}
            </div>
          ) : (
            <div className="text-center py-10 text-gray-400">
              <p className="text-3xl mb-3">🚧</p>
              <p className="font-medium">Texto pendiente de procesamiento OCR</p>
              <p className="text-sm mt-1">Disponible próximamente</p>
            </div>
          )}
        </div>
      )}

      {/* Resumen */}
      {vista === 'resumen' && (
        <div className="card mb-4">
          {tema.resumen ? (
            <div className="text-gray-700 leading-relaxed whitespace-pre-line text-[15px]">
              {tema.resumen}
            </div>
          ) : (
            <div className="text-center py-10 text-gray-400">
              <p className="text-3xl mb-3">✍️</p>
              <p className="font-medium">Resumen no disponible aún</p>
              <p className="text-sm mt-1">Se añadirá próximamente</p>
            </div>
          )}
        </div>
      )}

      {/* Quiz */}
      {vista === 'quiz' && quiz && (
        <div className="space-y-4 mb-4">
          {quiz.map((p, i) => (
            <div key={p.id} className="card">
              <p className="font-semibold text-sm text-gray-800 mb-3">
                {i + 1}. {p.pregunta}
              </p>
              <div className="space-y-2">
                {[
                  { key: 'a', texto: p.respuesta_correcta },
                  { key: 'b', texto: p.opcion_b },
                  { key: 'c', texto: p.opcion_c },
                  { key: 'd', texto: p.opcion_d },
                ].map(({ key, texto }) => {
                  const elegida = respuestas[p.id] === key
                  const esCorrecta = key === 'a'
                  let clases = 'w-full text-left px-4 py-2.5 rounded-xl border text-sm transition-colors '
                  if (!enviado) {
                    clases += elegida
                      ? 'border-brand-500 bg-brand-50 text-brand-700 font-medium'
                      : 'border-gray-200 text-gray-700 active:bg-gray-50'
                  } else {
                    if (esCorrecta) clases += 'border-green-400 bg-green-50 text-green-700 font-medium'
                    else if (elegida) clases += 'border-red-300 bg-red-50 text-red-600'
                    else clases += 'border-gray-200 text-gray-400'
                  }
                  return (
                    <button key={key} onClick={() => elegir(p.id, key)} className={clases}>
                      <span className="font-bold mr-2 uppercase">{key})</span>{texto}
                    </button>
                  )
                })}
              </div>
            </div>
          ))}

          {!enviado ? (
            <button
              onClick={() => setEnviado(true)}
              disabled={Object.keys(respuestas).length < quiz.length}
              className="w-full bg-brand-700 text-white font-semibold py-3.5 rounded-xl disabled:opacity-40 transition-opacity"
            >
              Ver resultados
            </button>
          ) : (
            <div className="card text-center">
              <p className="text-3xl mb-2">
                {calcularAciertos() === quiz.length ? '🎉' : calcularAciertos() >= quiz.length * 0.6 ? '👍' : '📚'}
              </p>
              <p className="text-2xl font-bold text-brand-700">
                {calcularAciertos()}/{quiz.length}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                {Math.round((calcularAciertos() / quiz.length) * 100)}% correcto
              </p>
              <button
                onClick={cargarQuiz}
                className="mt-4 text-sm text-brand-500 font-medium"
              >
                Repetir test →
              </button>
            </div>
          )}
        </div>
      )}

      {/* Navegación entre temas */}
      <div className="flex justify-between gap-3 mt-2">
        {num > 1 ? (
          <button
            onClick={() => navigate(`/oposiciones/${slug}/temas/${num - 1}`)}
            className="flex-1 py-3 border border-gray-200 rounded-xl text-sm text-brand-500 font-medium active:bg-gray-50"
          >
            ← Tema {num - 1}
          </button>
        ) : (
          <Link
            to={`/oposiciones/${slug}`}
            className="flex-1 py-3 border border-gray-200 rounded-xl text-sm text-brand-500 font-medium active:bg-gray-50 text-center"
          >
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
