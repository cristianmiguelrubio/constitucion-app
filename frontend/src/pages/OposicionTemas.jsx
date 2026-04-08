import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { apiFetch } from '../utils/api'

export default function OposicionTemas() {
  const { slug } = useParams()
  const [oposicion, setOposicion] = useState(null)
  const [temas, setTemas] = useState([])
  const [cargando, setCargando] = useState(true)

  useEffect(() => {
    apiFetch(`/api/oposiciones/${slug}/temas`)
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(data => {
        setOposicion(data.oposicion)
        setTemas(data.temas)
        setCargando(false)
      })
      .catch(() => setCargando(false))
  }, [slug])

  if (cargando) return (
    <div className="flex justify-center mt-24">
      <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  if (!oposicion) return (
    <div className="card text-center mt-16">
      <p className="text-red-500">Oposición no encontrada</p>
      <Link to="/oposiciones" className="text-brand-500 text-sm mt-2 inline-block">← Volver</Link>
    </div>
  )

  return (
    <div>
      {/* Breadcrumb */}
      <div className="flex items-center gap-1 text-xs text-gray-400 mb-3">
        <Link to="/oposiciones" className="hover:text-brand-500">Oposiciones</Link>
        <span>/</span>
        <span className="text-gray-600">{oposicion.nombre}</span>
      </div>

      {/* Cabecera */}
      <div className="card mb-5">
        <div className="flex items-center gap-3">
          <span className="text-4xl">{oposicion.icono || '📚'}</span>
          <div>
            <h1 className="text-xl font-bold text-brand-700">{oposicion.nombre}</h1>
            {oposicion.descripcion && (
              <p className="text-sm text-gray-400 mt-0.5">{oposicion.descripcion}</p>
            )}
            <p className="text-xs text-gray-300 mt-1">{temas.length} temas disponibles</p>
          </div>
        </div>
      </div>

      {/* Lista de temas */}
      {temas.length === 0 ? (
        <div className="card text-center mt-10">
          <p className="text-4xl mb-3">🚧</p>
          <p className="font-semibold text-gray-700">Cargando temario...</p>
          <p className="text-sm text-gray-400 mt-1">Los temas se están procesando.</p>
        </div>
      ) : (
        <div className="space-y-2">
          {temas.map(tema => (
            <Link
              key={tema.numero}
              to={`/oposiciones/${slug}/temas/${tema.numero}`}
              className="card flex items-center gap-3 active:bg-gray-50 transition-colors py-3.5"
            >
              <span className="shrink-0 bg-brand-100 text-brand-700 font-bold text-sm w-9 h-9 rounded-xl flex items-center justify-center">
                {tema.numero}
              </span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-800 leading-snug line-clamp-2">
                  {tema.titulo}
                </p>
                {tema.total_preguntas > 0 && (
                  <p className="text-xs text-gray-400 mt-0.5">
                    {tema.total_preguntas} preguntas de test
                  </p>
                )}
              </div>
              <span className="text-gray-300 shrink-0">›</span>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
