import { useEffect, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import Flashcard from '../components/Flashcard'

export default function Articulo() {
  const { numero } = useParams()
  const navigate = useNavigate()
  const [art, setArt] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [estudiado, setEstudiado] = useState(false)
  const [nota, setNota] = useState('')
  const [modoFlashcard, setModoFlashcard] = useState(false)

  useEffect(() => {
    setCargando(true)
    fetch(`/api/articulos/${numero}`)
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(data => {
        setArt(data)
        setCargando(false)
        // Cargar estado local
        const est = JSON.parse(localStorage.getItem('estudiados') || '{}')
        const notas = JSON.parse(localStorage.getItem('notas') || '{}')
        setEstudiado(!!est[numero])
        setNota(notas[numero] || '')
      })
      .catch(() => { setCargando(false) })
  }, [numero])

  const toggleEstudiado = () => {
    const est = JSON.parse(localStorage.getItem('estudiados') || '{}')
    est[numero] = !estudiado
    localStorage.setItem('estudiados', JSON.stringify(est))
    setEstudiado(!estudiado)
  }

  const guardarNota = (val) => {
    setNota(val)
    const notas = JSON.parse(localStorage.getItem('notas') || '{}')
    notas[numero] = val
    localStorage.setItem('notas', JSON.stringify(notas))
  }

  if (cargando) return <p className="text-center text-gray-400 mt-16">Cargando...</p>
  if (!art) return (
    <div className="card text-center mt-16">
      <p className="text-red-500">Artículo no encontrado</p>
      <Link to="/" className="text-brand-500 text-sm mt-2 inline-block">← Volver al índice</Link>
    </div>
  )

  const numInt = parseInt(numero)

  return (
    <div className="max-w-2xl mx-auto">
      {/* Breadcrumb */}
      <div className="text-xs text-gray-400 mb-4 flex flex-wrap gap-1">
        <Link to="/" className="hover:text-brand-500">Índice</Link>
        {art.titulo_titulo && <><span>/</span><span>{art.titulo_titulo}</span></>}
        {art.titulo_capitulo && <><span>/</span><span>{art.titulo_capitulo}</span></>}
      </div>

      {/* Artículo */}
      <div className="card mb-4">
        <div className="flex items-start justify-between mb-3">
          <h1 className="text-xl font-bold text-brand-700">
            Artículo {art.numero}
            {art.titulo && <span className="font-normal text-base ml-1">– {art.titulo}</span>}
          </h1>
          <div className="flex gap-2 shrink-0 ml-3">
            <button
              onClick={() => setModoFlashcard(f => !f)}
              className="px-3 py-1.5 rounded-full text-xs font-semibold bg-purple-100 text-purple-700 hover:bg-purple-200 transition-colors"
              title="Modo flashcard"
            >
              🃏 Flashcard
            </button>
            <button
              onClick={toggleEstudiado}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold transition-colors ${
                estudiado
                  ? 'bg-green-100 text-green-700 hover:bg-green-200'
                  : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
              }`}
            >
              {estudiado ? '✓ Estudiado' : 'Marcar'}
            </button>
          </div>
        </div>

        {modoFlashcard ? (
          <Flashcard numero={art.numero} contenido={art.contenido} titulo={art.titulo} />
        ) : (
          <div className="prose prose-sm max-w-none text-gray-700 leading-relaxed whitespace-pre-line">
            {art.contenido}
          </div>
        )}

        <p className="text-xs text-gray-300 mt-4">
          Actualizado: {new Date(art.actualizado_en).toLocaleDateString('es-ES')}
        </p>
      </div>

      {/* Notas personales */}
      <div className="card mb-4">
        <label className="block text-sm font-medium text-gray-600 mb-2">
          Mis notas
        </label>
        <textarea
          value={nota}
          onChange={e => guardarNota(e.target.value)}
          placeholder="Escribe tus apuntes aquí..."
          rows={4}
          className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 resize-none"
        />
      </div>

      {/* Historial de cambios */}
      {art.cambios?.length > 0 && (
        <div className="card mb-4">
          <h2 className="font-semibold text-sm text-gray-600 mb-3">Historial de cambios</h2>
          <ul className="space-y-2">
            {art.cambios.map(c => (
              <li key={c.id} className="text-xs text-gray-500 border-l-2 border-amber-300 pl-3">
                <span className="badge-nuevo mr-1">BOE</span>
                {c.descripcion} — {new Date(c.fecha).toLocaleDateString('es-ES')}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Navegación prev/next */}
      <div className="flex justify-between text-sm mt-2">
        {numInt > 1 ? (
          <button onClick={() => navigate(`/articulo/${numInt - 1}`)} className="text-brand-500 hover:underline">
            ← Art. {numInt - 1}
          </button>
        ) : <span />}
        <button onClick={() => navigate(`/articulo/${numInt + 1}`)} className="text-brand-500 hover:underline">
          Art. {numInt + 1} →
        </button>
      </div>
    </div>
  )
}
