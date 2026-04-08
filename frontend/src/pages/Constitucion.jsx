import { apiFetch } from '../utils/api'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

export default function Home() {
  const [estructura, setEstructura] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(null)
  const [abiertos, setAbiertos] = useState({})

  useEffect(() => {
    apiFetch('/api/estructura')
      .then(r => r.json())
      .then(data => { setEstructura(data); setCargando(false) })
      .catch(() => { setError('No se pudo conectar con el servidor'); setCargando(false) })
  }, [])

  const toggle = (key) => setAbiertos(prev => ({ ...prev, [key]: !prev[key] }))

  const getEstudiados = () => {
    try { return JSON.parse(localStorage.getItem('estudiados') || '{}') } catch { return {} }
  }
  const estudiados = getEstudiados()

  if (cargando) return (
    <div className="flex flex-col items-center justify-center mt-24 gap-3">
      <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
      <p className="text-gray-400 text-sm">Cargando Constitución...</p>
    </div>
  )

  if (error) return (
    <div className="card text-center mt-16">
      <p className="text-red-500 font-medium">{error}</p>
      <p className="text-sm text-gray-400 mt-2">Asegúrate de que el servidor está en marcha.</p>
    </div>
  )

  const titulos = Object.entries(estructura)
  const totalArticulos = titulos.reduce((acc, [, bloques]) =>
    acc + Object.values(bloques).reduce((a, arts) => a + arts.length, 0), 0)
  const totalEstudiados = Object.keys(estudiados).filter(k => estudiados[k]).length
  const porcentaje = totalArticulos ? Math.round((totalEstudiados / totalArticulos) * 100) : 0

  return (
    <div>
      {/* Header visual */}
      <div className="relative rounded-2xl overflow-hidden mb-5 shadow-lg" style={{ height: '140px' }}>
        <div className="absolute inset-0 bg-gradient-to-br from-[#1e3a5f] via-[#2d5a8e] to-[#1a237e]" />
        <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'repeating-linear-gradient(45deg, white 0, white 1px, transparent 0, transparent 50%)', backgroundSize: '20px 20px' }} />
        <div className="absolute inset-0 flex flex-col justify-center px-5">
          <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-white/50 mb-1">Texto oficial · BOE</p>
          <h1 className="text-2xl font-black text-white leading-tight">Constitución<br/>Española</h1>
          <p className="text-xs text-white/60 mt-1">Aprobada el 6 de diciembre de 1978</p>
        </div>
        <div className="absolute right-4 top-1/2 -translate-y-1/2 text-6xl opacity-20">📜</div>
      </div>

      {/* Progreso */}
      <div className="card mb-5">
        <div className="flex justify-between items-center mb-2">
          <h2 className="font-semibold text-brand-700 text-sm">Tu progreso</h2>
          <span className="text-xs text-gray-400">{totalEstudiados}/{totalArticulos} arts.</span>
        </div>
        <div className="w-full bg-gray-100 rounded-full h-3 mb-1">
          <div
            className="bg-brand-500 h-3 rounded-full transition-all"
            style={{ width: `${porcentaje}%` }}
          />
        </div>
        <p className="text-xs text-gray-400 text-right">{porcentaje}% completado</p>
      </div>

      <div className="space-y-2">
        {titulos.map(([titulo, bloques]) => {
          const arts = Object.values(bloques).flat()
          const estudiodosEnTitulo = arts.filter(a => estudiados[a.numero]).length
          const abierto = abiertos[titulo] ?? false
          const pct = Math.round((estudiodosEnTitulo / arts.length) * 100)

          return (
            <div key={titulo} className="card p-0 overflow-hidden">
              {/* Cabecera del título */}
              <button
                onClick={() => toggle(titulo)}
                className="w-full flex items-center gap-3 px-4 py-3.5 text-left active:bg-gray-50 transition-colors"
              >
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-brand-700 text-sm leading-snug truncate">{titulo}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <div className="flex-1 bg-gray-100 rounded-full h-1.5">
                      <div
                        className={`h-1.5 rounded-full ${pct === 100 ? 'bg-green-400' : 'bg-brand-400'}`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                    <span className="text-[10px] text-gray-400 shrink-0">{estudiodosEnTitulo}/{arts.length}</span>
                  </div>
                </div>
                <span className="text-gray-400 text-sm shrink-0">{abierto ? '▲' : '▼'}</span>
              </button>

              {abierto && (
                <div className="border-t border-gray-100">
                  {Object.entries(bloques).map(([bloque, articulos]) => (
                    <div key={bloque}>
                      {bloque !== '_' && (
                        <p className="px-4 py-2 text-xs font-semibold text-gray-400 bg-gray-50 border-b border-gray-100">
                          {bloque}
                        </p>
                      )}
                      {articulos.map(a => (
                        <Link
                          key={a.numero}
                          to={`/articulo/${a.numero}`}
                          className="flex items-center gap-3 px-4 py-3 active:bg-blue-50 transition-colors border-b border-gray-50 last:border-0"
                        >
                          <span className={`w-2.5 h-2.5 rounded-full shrink-0 ${
                            estudiados[a.numero] ? 'bg-green-400' : 'bg-gray-200'
                          }`} />
                          <span className="text-sm min-w-0">
                            <span className="font-semibold text-brand-500 mr-1">Art. {a.numero}.</span>
                            <span className="text-gray-600">{a.titulo || ''}</span>
                          </span>
                          <span className="text-gray-300 ml-auto shrink-0">›</span>
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
