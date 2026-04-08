import { apiFetch } from '../utils/api'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

export default function Stats() {
  const [articulos, setArticulos] = useState([])
  const [cargando, setCargando] = useState(true)

  useEffect(() => {
    apiFetch('/api/articulos')
      .then(r => r.json())
      .then(data => { setArticulos(data); setCargando(false) })
      .catch(() => setCargando(false))
  }, [])

  const estudiados = JSON.parse(localStorage.getItem('estudiados') || '{}')
  const notas = JSON.parse(localStorage.getItem('notas') || '{}')

  const totalArticulos = articulos.length
  const totalEstudiados = articulos.filter(a => estudiados[a.numero]).length
  const totalConNotas = articulos.filter(a => notas[a.numero]?.trim()).length
  const porcentaje = totalArticulos ? Math.round((totalEstudiados / totalArticulos) * 100) : 0

  // Agrupados por título
  const porTitulo = articulos.reduce((acc, art) => {
    const t = art.titulo_titulo || 'Sin título'
    if (!acc[t]) acc[t] = { total: 0, estudiados: 0 }
    acc[t].total++
    if (estudiados[art.numero]) acc[t].estudiados++
    return acc
  }, {})

  const resetearProgreso = () => {
    if (window.confirm('¿Seguro que quieres borrar todo tu progreso?')) {
      localStorage.removeItem('estudiados')
      localStorage.removeItem('notas')
      window.location.reload()
    }
  }

  if (cargando) return <p className="text-center text-gray-400 mt-16">Cargando...</p>

  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-xl font-bold text-brand-700 mb-5">Mis estadísticas</h1>

      {/* Resumen */}
      <div className="grid grid-cols-3 gap-3 mb-6">
        <div className="card text-center">
          <p className="text-3xl font-bold text-brand-500">{porcentaje}%</p>
          <p className="text-xs text-gray-400 mt-1">Completado</p>
        </div>
        <div className="card text-center">
          <p className="text-3xl font-bold text-green-500">{totalEstudiados}</p>
          <p className="text-xs text-gray-400 mt-1">Estudiados</p>
        </div>
        <div className="card text-center">
          <p className="text-3xl font-bold text-amber-500">{totalConNotas}</p>
          <p className="text-xs text-gray-400 mt-1">Con notas</p>
        </div>
      </div>

      {/* Barra general */}
      <div className="card mb-6">
        <div className="flex justify-between text-sm mb-2">
          <span className="font-medium text-gray-700">Progreso total</span>
          <span className="text-gray-400">{totalEstudiados} / {totalArticulos}</span>
        </div>
        <div className="w-full bg-gray-100 rounded-full h-4">
          <div
            className="bg-brand-500 h-4 rounded-full transition-all"
            style={{ width: `${porcentaje}%` }}
          />
        </div>
      </div>

      {/* Por título */}
      <h2 className="font-semibold text-gray-600 mb-3">Por título</h2>
      <div className="space-y-2 mb-6">
        {Object.entries(porTitulo).map(([titulo, datos]) => {
          const pct = Math.round((datos.estudiados / datos.total) * 100)
          return (
            <div key={titulo} className="card py-3">
              <div className="flex justify-between items-center mb-1.5">
                <span className="text-xs font-medium text-gray-600 truncate max-w-[75%]">{titulo}</span>
                <span className="text-xs text-gray-400">{datos.estudiados}/{datos.total}</span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-1.5">
                <div
                  className={`h-1.5 rounded-full ${pct === 100 ? 'bg-green-400' : 'bg-brand-500'}`}
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          )
        })}
      </div>

      {/* Artículos pendientes */}
      {totalEstudiados < totalArticulos && (
        <>
          <h2 className="font-semibold text-gray-600 mb-3">Pendientes de estudiar</h2>
          <div className="card mb-6">
            <div className="flex flex-wrap gap-2">
              {articulos
                .filter(a => !estudiados[a.numero])
                .slice(0, 20)
                .map(a => (
                  <Link
                    key={a.numero}
                    to={`/articulo/${a.numero}`}
                    className="text-xs bg-gray-100 hover:bg-brand-100 text-gray-600 hover:text-brand-700 px-2 py-1 rounded-lg transition-colors"
                  >
                    Art. {a.numero}
                  </Link>
                ))
              }
              {articulos.filter(a => !estudiados[a.numero]).length > 20 && (
                <span className="text-xs text-gray-400 self-center">
                  +{articulos.filter(a => !estudiados[a.numero]).length - 20} más
                </span>
              )}
            </div>
          </div>
        </>
      )}

      {/* Acciones */}
      <div className="flex gap-3">
        <Link to="/quiz" className="btn-primary flex-1 text-center">
          Hacer test
        </Link>
        <button
          onClick={resetearProgreso}
          className="flex-1 border border-red-200 text-red-400 hover:bg-red-50 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          Resetear progreso
        </button>
      </div>
    </div>
  )
}
