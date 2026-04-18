import { useEffect, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { apiFetch } from '../utils/api'
import { usePlan } from '../hooks/usePlan'

export default function OposicionTemas() {
  const { slug } = useParams()
  const navigate = useNavigate()
  const [oposicion, setOposicion] = useState(null)
  const [temas, setTemas] = useState([])
  const [cargando, setCargando] = useState(true)
  const plan = usePlan()

  const esTrial = plan?.es_trial === true

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
          <div className="flex-1 min-w-0">
            <h1 className="text-xl font-bold text-brand-700">{oposicion.nombre}</h1>
            {oposicion.descripcion && (
              <p className="text-sm text-gray-400 mt-0.5">{oposicion.descripcion}</p>
            )}
            <p className="text-xs text-gray-300 mt-1">{temas.length} temas disponibles</p>
          </div>
          {!esTrial && temas.length > 0 && (
            <a
              href={`/api/oposiciones/${slug}/descargar`}
              download
              className="shrink-0 flex items-center gap-1 bg-brand-50 text-brand-700 text-xs font-semibold px-3 py-1.5 rounded-xl hover:bg-brand-100 transition-colors"
            >
              ⬇ Temario
            </a>
          )}
        </div>
      </div>

      {/* Banner trial */}
      {esTrial && (
        <div className="mb-4 bg-amber-50 border border-amber-200 rounded-2xl px-4 py-3 flex items-center gap-3">
          <span className="text-2xl shrink-0">⏱</span>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-amber-700">Periodo de prueba — Tema 1 desbloqueado</p>
            <p className="text-xs text-amber-600 mt-0.5">Suscríbete para acceder a todos los temas</p>
          </div>
          <button
            onClick={() => navigate('/planes')}
            className="shrink-0 bg-amber-500 text-white text-xs font-bold px-3 py-1.5 rounded-xl hover:bg-amber-600 transition-colors"
          >
            Ver planes
          </button>
        </div>
      )}

      {/* Lista de temas */}
      {temas.length === 0 ? (
        <div className="card text-center mt-10">
          <p className="text-4xl mb-3">🚧</p>
          <p className="font-semibold text-gray-700">Cargando temario...</p>
          <p className="text-sm text-gray-400 mt-1">Los temas se están procesando.</p>
        </div>
      ) : (
        <div className="space-y-2">
          {temas.map(tema => {
            const bloqueado = esTrial && tema.numero > 1

            if (bloqueado) {
              return (
                <button
                  key={tema.numero}
                  onClick={() => navigate('/planes')}
                  className="w-full card flex items-center gap-3 py-3.5 opacity-60 active:opacity-50 transition-opacity text-left"
                >
                  <span className="shrink-0 bg-gray-100 text-gray-400 font-bold text-sm w-9 h-9 rounded-xl flex items-center justify-center">
                    {tema.numero}
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-500 leading-snug line-clamp-3">
                      {tema.titulo}
                    </p>
                    {tema.total_preguntas > 0 && (
                      <p className="text-xs text-gray-300 mt-0.5">
                        {tema.total_preguntas} preguntas de test
                      </p>
                    )}
                  </div>
                  <span className="text-gray-300 shrink-0 text-lg">🔒</span>
                </button>
              )
            }

            return (
              <Link
                key={tema.numero}
                to={`/oposiciones/${slug}/temas/${tema.numero}`}
                className="card flex items-center gap-3 active:bg-gray-50 transition-colors py-3.5"
              >
                <span className="shrink-0 bg-brand-100 text-brand-700 font-bold text-sm w-9 h-9 rounded-xl flex items-center justify-center">
                  {tema.numero}
                </span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-800 leading-snug line-clamp-3">
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
            )
          })}
        </div>
      )}
    </div>
  )
}
