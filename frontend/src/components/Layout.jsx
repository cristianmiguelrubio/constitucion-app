import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useState } from 'react'

const NAV_ITEMS = [
  { to: '/',            label: 'Inicio',      icon: '🏠' },
  { to: '/constitucion',label: 'Constitución',icon: '📜' },
  { to: '/oposiciones', label: 'Oposiciones', icon: '👮' },
  { to: '/quiz',        label: 'Test',        icon: '🧠' },
  { to: '/cambios',     label: 'Cambios',     icon: '🔔' },
]

export default function Layout({ children, usuario, onLogout }) {
  const [query, setQuery] = useState('')
  const [buscarAbierto, setBuscarAbierto] = useState(false)
  const navigate = useNavigate()

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

      {/* Header top */}
      <header className="bg-brand-700 text-white shadow-md sticky top-0 z-50 safe-area-top">
        <div className="max-w-4xl mx-auto px-4 h-14 flex items-center gap-3">

          <Link to="/" className="font-bold text-base leading-tight shrink-0 flex items-center gap-1.5">
            <span className="text-xl">📜</span>
            <span className="hidden sm:inline">Constitución</span>
          </Link>

          {/* Buscador — escritorio */}
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

          {/* Botón buscar móvil */}
          <button
            onClick={() => setBuscarAbierto(v => !v)}
            className="sm:hidden ml-auto p-2 rounded-xl hover:bg-white/10 transition-colors"
            aria-label="Buscar"
          >
            🔍
          </button>

          {/* Usuario escritorio */}
          {usuario && (
            <div className="hidden sm:flex items-center gap-2 shrink-0">
              <span className="text-xs text-white/60 truncate max-w-[130px]">
                {usuario.nombre || usuario.email}
              </span>
              <button
                onClick={onLogout}
                className="text-xs text-white/40 hover:text-white transition-colors px-2 py-1 rounded-lg hover:bg-white/10"
              >
                Salir
              </button>
            </div>
          )}
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
              <button type="submit" className="bg-yellow-400 text-brand-900 font-semibold px-4 py-2.5 rounded-xl text-sm">
                Ir
              </button>
            </form>
          </div>
        )}

        {/* Nav escritorio */}
        <nav className="hidden sm:block bg-brand-900/40 border-t border-white/10">
          <div className="max-w-4xl mx-auto px-4 flex gap-1">
            {NAV_ITEMS.map(({ to, label, icon }) => (
              <NavLink
                key={to}
                to={to}
                end
                className={({ isActive }) =>
                  `px-4 py-2 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${
                    isActive
                      ? 'border-yellow-300 text-white'
                      : 'border-transparent text-white/70 hover:text-white'
                  }`
                }
              >
                {icon} {label}
              </NavLink>
            ))}
          </div>
        </nav>
      </header>

      {/* Contenido */}
      <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-5 pb-28 sm:pb-6">
        {children}
      </main>

      {/* Footer escritorio */}
      <footer className="hidden sm:block text-center text-xs text-gray-400 py-3 border-t border-gray-100">
        Texto oficial BOE · Actualizado diariamente
      </footer>

      {/* Nav inferior móvil */}
      <nav className="sm:hidden fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200">
        <div className="flex">
          {NAV_ITEMS.map(({ to, label, icon }) => (
            <NavLink
              key={to}
              to={to}
              end
              className={({ isActive }) =>
                `flex-1 flex flex-col items-center justify-center pt-2 gap-0.5 transition-colors ${
                  isActive ? 'text-brand-600' : 'text-gray-400'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <span className="text-xl leading-none">{icon}</span>
                  <span className={`text-[10px] font-medium ${isActive ? 'text-brand-600' : 'text-gray-400'}`}>
                    {label}
                  </span>
                  {/* Relleno debajo de los iconos = home indicator iPhone */}
                  <span className="block" style={{ height: 'env(safe-area-inset-bottom, 8px)' }} />
                </>
              )}
            </NavLink>
          ))}
        </div>
      </nav>

    </div>
  )
}
