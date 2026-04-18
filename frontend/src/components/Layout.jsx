import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useState, useEffect } from 'react'
import MenuLateral from './MenuLateral'

export default function Layout({ children, usuario, onLogout }) {
  const [query, setQuery] = useState('')
  const [buscarAbierto, setBuscarAbierto] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    setBuscarAbierto(false)
    setQuery('')
  }, [location.pathname])

  const handleSearch = (e) => {
    e.preventDefault()
    if (query.trim().length >= 2) {
      navigate(`/buscar?q=${encodeURIComponent(query.trim())}`)
      setBuscarAbierto(false)
      setQuery('')
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">

      {/* Header */}
      <header className="bg-brand-700 text-white shadow-md sticky top-0 z-50 safe-area-top">
        <div className="max-w-4xl mx-auto px-4 h-14 flex items-center gap-3">

          <Link to="/" className="font-bold text-base leading-tight shrink-0 flex items-center gap-1.5">
            <span className="text-xl">📜</span>
            <span className="text-sm">Oposiciones del Estado</span>
          </Link>

          {/* Buscador escritorio */}
          <form onSubmit={handleSearch} className="hidden sm:flex flex-1 gap-2">
            <input
              type="search"
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Buscar artículo o palabra..."
              className="flex-1 rounded-xl px-4 py-2 text-gray-900 text-sm focus:outline-none focus:ring-2 focus:ring-yellow-300"
            />
            <button type="submit" className="bg-yellow-400 hover:bg-yellow-300 text-brand-900 font-semibold px-4 py-2 rounded-xl text-sm transition-colors">
              Buscar
            </button>
          </form>

          {/* Iconos móvil */}
          <div className="sm:hidden ml-auto flex items-center gap-1">
            <button onClick={() => setBuscarAbierto(v => !v)} className="p-2 rounded-xl hover:bg-white/10 transition-colors" aria-label="Buscar">
              🔍
            </button>
          </div>

          {/* Hamburguesa siempre visible */}
          <div className="ml-auto sm:ml-0 shrink-0">
            {usuario
              ? <MenuLateral usuario={usuario} onLogout={onLogout} />
              : <Link to="/planes" className="text-xs bg-yellow-400 text-brand-900 font-semibold px-3 py-1.5 rounded-lg hover:bg-yellow-300 transition-colors">Planes</Link>
            }
          </div>
        </div>

        {/* Buscador móvil desplegable */}
        {buscarAbierto && (
          <div className="sm:hidden px-4 pb-3">
            <form onSubmit={handleSearch} className="flex gap-2">
              <input
                type="search"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Buscar artículo o palabra..."
                autoFocus
                className="flex-1 rounded-xl px-4 py-2.5 text-gray-900 text-sm focus:outline-none focus:ring-2 focus:ring-yellow-300"
              />
              <button type="submit" className="bg-yellow-400 text-brand-900 font-semibold px-4 py-2.5 rounded-xl text-sm">Ir</button>
            </form>
          </div>
        )}
      </header>

      {/* Contenido */}
      <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-5 pb-24">
        {children}
      </main>

      {/* Footer */}
      <footer className="text-center text-xs text-gray-400 py-3 border-t border-gray-100">
        Texto oficial BOE · Actualizado diariamente
      </footer>

    </div>
  )
}
