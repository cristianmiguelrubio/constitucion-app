import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

export default function Cambios() {
  const [cambios, setCambios] = useState([])
  const [cargando, setCargando] = useState(true)

  useEffect(() => {
    fetch('/api/cambios')
      .then(r => r.json())
      .then(data => { setCambios(data); setCargando(false) })
      .catch(() => setCargando(false))
  }, [])

  if (cargando) return <p className="text-center text-gray-400 mt-16">Cargando...</p>

  return (
    <div>
      <div className="flex items-center justify-between mb-5">
        <h1 className="text-xl font-bold text-brand-700">Historial de cambios</h1>
        <span className="text-xs text-gray-400">Actualizado desde BOE diariamente</span>
      </div>

      {cambios.length === 0 ? (
        <div className="card text-center mt-10">
          <p className="text-4xl mb-3">✅</p>
          <p className="font-semibold text-gray-700">Sin cambios registrados</p>
          <p className="text-sm text-gray-400 mt-1">
            Cuando el BOE publique una reforma constitucional aparecerá aquí.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {cambios.map(c => (
            <div key={c.id} className="card border-l-4 border-amber-400">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="badge-nuevo">BOE</span>
                    <Link
                      to={`/articulo/${c.articulo_numero}`}
                      className="font-semibold text-brand-500 hover:underline text-sm"
                    >
                      Artículo {c.articulo_numero}
                    </Link>
                  </div>
                  <p className="text-sm text-gray-700">{c.descripcion}</p>
                  {c.boe_referencia && (
                    <p className="text-xs text-gray-400 mt-1">Ref: {c.boe_referencia}</p>
                  )}
                </div>
                <span className="text-xs text-gray-400 whitespace-nowrap shrink-0">
                  {new Date(c.fecha).toLocaleDateString('es-ES', {
                    day: '2-digit', month: 'short', year: 'numeric'
                  })}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
