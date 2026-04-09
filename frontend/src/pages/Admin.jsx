import { useEffect, useState } from 'react'
import { apiFetch } from '../utils/api'

export default function Admin() {
  const [sugerencias, setSugerencias] = useState([])
  const [cargando, setCargando] = useState(true)
  const [acceso, setAcceso] = useState(true)

  useEffect(() => {
    apiFetch('/api/admin/sugerencias')
      .then(r => {
        if (r.status === 403) { setAcceso(false); setCargando(false); return null }
        return r.json()
      })
      .then(data => { if (data) { setSugerencias(data); setCargando(false) } })
      .catch(() => setCargando(false))
  }, [])

  if (!acceso) return (
    <div className="card text-center mt-16">
      <p className="text-3xl mb-2">🔒</p>
      <p className="font-medium text-gray-600">Acceso restringido</p>
    </div>
  )

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex items-center justify-between mb-5">
        <h1 className="text-xl font-bold text-brand-700">Panel Admin</h1>
        <span className="text-xs text-gray-400">{sugerencias.length} sugerencias</span>
      </div>

      {cargando && <div className="flex justify-center mt-12"><div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" /></div>}

      {!cargando && sugerencias.length === 0 && (
        <div className="card text-center py-10">
          <p className="text-3xl mb-2">📭</p>
          <p className="text-gray-400">Sin sugerencias todavía</p>
        </div>
      )}

      <div className="space-y-3">
        {sugerencias.map(s => (
          <div key={s.id} className="card border-l-4 border-brand-300">
            <div className="flex justify-between items-start gap-2 mb-1">
              <span className="text-xs font-semibold text-brand-600">{s.usuario}</span>
              <span className="text-xs text-gray-400 shrink-0">
                {new Date(s.fecha).toLocaleDateString('es-ES', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
            <p className="text-sm text-gray-700 leading-relaxed">{s.texto}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
