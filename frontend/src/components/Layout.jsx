import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useState } from 'react'

export default function Layout({ children, usuario, onLogout }) {
  const [query, setQuery] = useState('')
  const navigate = useNavigate()

  const handleSearch = (e) => {
    e.preventDefault()
    if (query.trim().length >= 2) {
      navigate(`/buscar?q=${encodeURIComponent(query.trim())}`)
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-brand-700 text-white shadow-md sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-3 flex items-center gap-4">
          <Link to="/" className="font-bold text-lg leading-tight shrink-0">
            <span className="text-yellow-300">📜</span> Constitución
          </Link>
          {usuario && (
            <div className="hidden sm:flex items-center gap-2 shrink-0 ml-auto mr-2">
              <span className="text-xs text-white/60 truncate max-w-[140px]">{usuario.nombre || usuario.email}</span>
              <button onClick={onLogout} className="text-xs text-white/40 hover:text-white/80 transition-colors">salir</button>
            </div>
          )}

          <form onSubmit={handleSearch} className="flex-1 flex gap-2">
            <input
              type="search"
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Buscar artículo, palabra..."
              className="flex-1 rounded-lg px-3 py-1.5 text-gray-900 text-sm focus:outline-none focus:ring-2 focus:ring-yellow-300"
            />
            <button type="submit" className="bg-yellow-400 hover:bg-yellow-300 text-brand-900 font-semibold px-3 py-1.5 rounded-lg text-sm transition-colors">
              Buscar
            </button>
          </form>
        </div>

        {/* Nav */}
        <nav className="bg-brand-900/40 border-t border-white/10">
          <div className="max-w-4xl mx-auto px-4 flex gap-1 overflow-x-auto">
            {[
              { to: '/', label: 'Índice' },
              { to: '/quiz', label: '🧠 Test' },
              { to: '/stats', label: '📊 Stats' },
              { to: '/cambios', label: '🔔 Cambios' },
            ].map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                end
                className={({ isActive }) =>
                  `px-3 py-2 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${
                    isActive
                      ? 'border-yellow-300 text-white'
                      : 'border-transparent text-white/70 hover:text-white'
                  }`
                }
              >
                {label}
              </NavLink>
            ))}
          </div>
        </nav>
      </header>

      {/* Content */}
      <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-6">
        {children}
      </main>

      <footer className="text-center text-xs text-gray-400 py-4 border-t border-gray-100">
        Texto oficial BOE · Actualizado diariamente
      </footer>
    </div>
  )
}
