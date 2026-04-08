import { apiFetch } from '../utils/api'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

export default function Oposiciones() {
  const [lista, setLista] = useState([])
  const [cargando, setCargando] = useState(true)

  useEffect(() => {
    apiFetch('/api/oposiciones')
      .then(r => r.json())
      .then(data => { setLista(data); setCargando(false) })
      .catch(() => setCargando(false))
  }, [])

  if (cargando) return (
    <div className="flex justify-center mt-24">
      <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  return (
    <div>
      <h1 className="text-xl font-bold text-brand-700 mb-1">Oposiciones</h1>
      <p className="text-sm text-gray-400 mb-5">Selecciona tu categoría para estudiar el temario</p>

      {lista.length === 0 ? (
        <div className="card text-center mt-16">
          <p className="text-4xl mb-3">🚧</p>
          <p className="font-semibold text-gray-700">Próximamente</p>
          <p className="text-sm text-gray-400 mt-1">
            Estamos cargando los temarios. Vuelve en breve.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {lista.map(op => (
            <Link
              key={op.slug}
              to={`/oposiciones/${op.slug}`}
              className="card flex items-center gap-4 active:bg-gray-50 transition-colors"
            >
              <span className="text-4xl shrink-0">{op.icono || '📚'}</span>
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-brand-700">{op.nombre}</p>
                {op.descripcion && (
                  <p className="text-xs text-gray-400 mt-0.5 truncate">{op.descripcion}</p>
                )}
                <p className="text-xs text-gray-300 mt-1">
                  {op.total_temas ?? 0} tema{op.total_temas !== 1 ? 's' : ''}
                </p>
              </div>
              <span className="text-gray-300 shrink-0">›</span>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
