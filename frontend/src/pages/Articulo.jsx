import { apiFetch } from '../utils/api'
import { useEffect, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import Flashcard from '../components/Flashcard'

export default function Articulo({ usuario }) {
  const { numero } = useParams()
  const navigate = useNavigate()
  const [art, setArt] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [estudiado, setEstudiado] = useState(false)
  const [nota, setNota] = useState('')
  const [modoFlashcard, setModoFlashcard] = useState(false)
  const [guardandoNota, setGuardandoNota] = useState(false)

  useEffect(() => {
    setCargando(true)
    apiFetch(`/api/articulos/${numero}`)
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(data => {
        setArt(data)
        setCargando(false)
        const est = JSON.parse(localStorage.getItem('estudiados') || '{}')
        const notas = JSON.parse(localStorage.getItem('notas') || '{}')
        setEstudiado(!!est[numero])
        setNota(notas[numero] || '')
      })
      .catch(() => setCargando(false))
  }, [numero])

  const toggleEstudiado = () => {
    const est = JSON.parse(localStorage.getItem('estudiados') || '{}')
    est[numero] = !estudiado
    localStorage.setItem('estudiados', JSON.stringify(est))
    setEstudiado(!estudiado)

    // Sincronizar con servidor si hay usuario
    apiFetch('/api/progreso', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ articulo_numero: numero, estudiado: !estudiado, nota }),
    }).catch(() => {})
  }

  const guardarNota = (val) => {
    setNota(val)
    const notas = JSON.parse(localStorage.getItem('notas') || '{}')
    notas[numero] = val
    localStorage.setItem('notas', JSON.stringify(notas))
  }

  const guardarNotaServidor = () => {
    setGuardandoNota(true)
    apiFetch('/api/progreso', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ articulo_numero: numero, estudiado, nota }),
    }).finally(() => setGuardandoNota(false))
  }

  const numInt = parseInt(numero)

  if (cargando) return (
    <div className="flex justify-center mt-24">
      <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  if (!art) return (
    <div className="card text-center mt-16">
      <p className="text-red-500">Artículo no encontrado</p>
      <Link to="/" className="text-brand-500 text-sm mt-2 inline-block">← Volver al índice</Link>
    </div>
  )

  return (
    <div className="max-w-2xl mx-auto">
      {/* Breadcrumb */}
      <div className="flex items-center gap-1 text-xs text-gray-400 mb-3 overflow-x-auto whitespace-nowrap pb-1">
        <Link to="/" className="hover:text-brand-500 shrink-0">Índice</Link>
        {art.titulo_titulo && <><span>/</span><span className="truncate max-w-[150px]">{art.titulo_titulo}</span></>}
      </div>

      {/* Artículo */}
      <div className="card mb-4">
        {/* Cabecera */}
        <div className="flex items-start justify-between gap-2 mb-4">
          <div className="min-w-0">
            <h1 className="text-xl font-bold text-brand-700">Artículo {art.numero}</h1>
            {art.titulo && <p className="text-sm text-gray-500 mt-0.5">{art.titulo}</p>}
          </div>
          <button
            onClick={toggleEstudiado}
            className={`shrink-0 px-3 py-2 rounded-xl text-xs font-semibold transition-colors ${
              estudiado
                ? 'bg-green-100 text-green-700 active:bg-green-200'
                : 'bg-gray-100 text-gray-500 active:bg-gray-200'
            }`}
          >
            {estudiado ? '✓ Estudiado' : 'Marcar'}
          </button>
        </div>

        {/* Contenido / Flashcard */}
        {modoFlashcard ? (
          <Flashcard numero={art.numero} contenido={art.contenido} titulo={art.titulo} />
        ) : (
          <div className="text-gray-700 leading-relaxed whitespace-pre-line text-[15px]">
            {art.contenido}
          </div>
        )}

        {/* Botón flashcard */}
        <button
          onClick={() => setModoFlashcard(f => !f)}
          className="mt-4 text-xs text-purple-500 font-medium"
        >
          {modoFlashcard ? '← Ver texto completo' : '🃏 Modo flashcard'}
        </button>

        <p className="text-xs text-gray-300 mt-3">
          Actualizado: {new Date(art.actualizado_en).toLocaleDateString('es-ES')}
        </p>
      </div>

      {/* Notas */}
      <div className="card mb-4">
        <label className="block text-sm font-semibold text-gray-600 mb-2">Mis notas</label>
        <textarea
          value={nota}
          onChange={e => guardarNota(e.target.value)}
          onBlur={guardarNotaServidor}
          placeholder="Escribe tus apuntes aquí..."
          rows={4}
          className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 resize-none"
        />
        {guardandoNota && <p className="text-xs text-gray-400 mt-1">Guardando...</p>}
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

      {/* Navegación anterior/siguiente */}
      <div className="flex justify-between gap-3 mt-2">
        {numInt > 1 ? (
          <button
            onClick={() => navigate(`/articulo/${numInt - 1}`)}
            className="flex-1 py-3 border border-gray-200 rounded-xl text-sm text-brand-500 font-medium active:bg-gray-50"
          >
            ← Art. {numInt - 1}
          </button>
        ) : <div className="flex-1" />}
        <button
          onClick={() => navigate(`/articulo/${numInt + 1}`)}
          className="flex-1 py-3 border border-gray-200 rounded-xl text-sm text-brand-500 font-medium active:bg-gray-50"
        >
          Art. {numInt + 1} →
        </button>
      </div>
    </div>
  )
}
