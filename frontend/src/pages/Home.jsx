import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

export default function Home() {
  const [estructura, setEstructura] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(null)
  const [abiertos, setAbiertos] = useState({})

  useEffect(() => {
    fetch('/api/estructura')
      .then(r => r.json())
      .then(data => { setEstructura(data); setCargando(false) })
      .catch(() => { setError('No se pudo conectar con el servidor'); setCargando(false) })
  }, [])

  const toggle = (key) => setAbiertos(prev => ({ ...prev, [key]: !prev[key] }))

  // Progreso guardado en localStorage
  const getEstudiados = () => {
    try { return JSON.parse(localStorage.getItem('estudiados') || '{}') } catch { return {} }
  }
  const estudiados = getEstudiados()

  if (cargando) return <p className="text-center text-gray-400 mt-16">Cargando Constitución...</p>
  if (error) return (
    <div className="card text-center mt-16">
      <p className="text-red-500 font-medium">{error}</p>
      <p className="text-sm text-gray-400 mt-2">Asegúrate de que el servidor backend está en marcha.</p>
    </div>
  )

  const titulos = Object.entries(estructura)
  const totalArticulos = titulos.reduce((acc, [, bloques]) =>
    acc + Object.values(bloques).reduce((a, arts) => a + arts.length, 0), 0)
  const totalEstudiados = Object.keys(estudiados).filter(k => estudiados[k]).length

  return (
    <div>
      {/* Progreso general */}
      <div className="card mb-6">
        <div className="flex justify-between items-center mb-2">
          <h2 className="font-semibold text-brand-700">Tu progreso</h2>
          <span className="text-sm text-gray-500">{totalEstudiados} / {totalArticulos} artículos</span>
        </div>
        <div className="w-full bg-gray-100 rounded-full h-2.5">
          <div
            className="bg-brand-500 h-2.5 rounded-full transition-all"
            style={{ width: `${totalArticulos ? (totalEstudiados / totalArticulos) * 100 : 0}%` }}
          />
        </div>
      </div>

      {/* Índice por Títulos */}
      <h1 className="text-xl font-bold text-brand-700 mb-4">Constitución Española</h1>

      <div className="space-y-3">
        {titulos.map(([titulo, bloques]) => {
          const arts = Object.values(bloques).flat()
          const estudiodosEnTitulo = arts.filter(a => estudiados[a.numero]).length
          const abierto = abiertos[titulo] ?? false

          return (
            <div key={titulo} className="card p-0 overflow-hidden">
              <button
                onClick={() => toggle(titulo)}
                className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-gray-50 transition-colors"
              >
                <span className="font-semibold text-brand-700 text-sm">{titulo}</span>
                <div className="flex items-center gap-2 text-xs text-gray-400">
                  <span>{estudiodosEnTitulo}/{arts.length}</span>
                  <span>{abierto ? '▲' : '▼'}</span>
                </div>
              </button>

              {abierto && (
                <div className="border-t border-gray-100 divide-y divide-gray-50">
                  {Object.entries(bloques).map(([bloque, articulos]) => (
                    <div key={bloque}>
                      {bloque !== '_' && (
                        <p className="px-4 py-1.5 text-xs font-medium text-gray-400 bg-gray-50">
                          {bloque}
                        </p>
                      )}
                      {articulos.map(a => (
                        <Link
                          key={a.numero}
                          to={`/articulo/${a.numero}`}
                          className="flex items-center gap-3 px-4 py-2.5 hover:bg-blue-50 transition-colors"
                        >
                          <span className={`w-2 h-2 rounded-full shrink-0 ${
                            estudiados[a.numero] ? 'bg-green-400' : 'bg-gray-200'
                          }`} />
                          <span className="text-sm">
                            <span className="font-medium text-brand-500 mr-1">Art. {a.numero}.</span>
                            <span className="text-gray-600">{a.titulo || ''}</span>
                          </span>
                        </Link>
                      ))}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
