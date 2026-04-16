import { useState, useEffect } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { apiFetch } from '../utils/api'

const NAV_LINKS = [
  { to: '/',             label: 'Inicio',        icon: '🏠' },
  { to: '/constitucion', label: 'Constitución',  icon: '📜' },
  { to: '/oposiciones',  label: 'Oposiciones',   icon: '👮' },
  { to: '/simulacro',    label: 'Simulacro',     icon: '⏱' },
  { to: '/quiz',         label: 'Tests',         icon: '🧠' },
  { to: '/flashcards',   label: 'Flashcards',    icon: '🃏' },
  { to: '/ranking',      label: 'Ranking',       icon: '🏆' },
  { to: '/stats',        label: 'Estadísticas',  icon: '📊' },
  { to: '/planes',       label: 'Planes',        icon: '💳' },
]

export default function MenuLateral({ usuario, onLogout }) {
  const [abierto, setAbierto] = useState(false)
  const [seccion, setSeccion] = useState(null) // null | 'perfil' | 'password' | 'plan'
  const navigate = useNavigate()

  // Perfil
  const [nombre, setNombre] = useState(usuario?.nombre || '')
  const [email, setEmail] = useState(usuario?.email || '')
  const [planInfo, setPlanInfo] = useState(null)

  // Password
  const [passActual, setPassActual] = useState('')
  const [passNueva, setPassNueva] = useState('')

  const [msg, setMsg] = useState('')
  const [error, setError] = useState('')
  const [cargando, setCargando] = useState(false)

  useEffect(() => {
    if (abierto) {
      apiFetch('/api/perfil').then(r => r.json()).then(d => {
        setNombre(d.nombre || '')
        setEmail(d.email || '')
        setPlanInfo(d)
      }).catch(() => {})
    }
  }, [abierto])

  const cerrar = () => { setAbierto(false); setSeccion(null); setMsg(''); setError('') }

  const guardarPerfil = async () => {
    setCargando(true); setMsg(''); setError('')
    try {
      const r = await apiFetch('/api/perfil', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, email }),
      })
      const d = await r.json()
      if (!r.ok) { setError(d.detail || 'Error'); return }
      setMsg('Perfil actualizado')
      const u = JSON.parse(localStorage.getItem('usuario') || '{}')
      localStorage.setItem('usuario', JSON.stringify({ ...u, nombre: d.nombre, email: d.email }))
    } catch { setError('Error de conexión') }
    finally { setCargando(false) }
  }

  const cambiarPassword = async () => {
    if (passNueva.length < 6) { setError('Mínimo 6 caracteres'); return }
    setCargando(true); setMsg(''); setError('')
    try {
      const r = await apiFetch('/api/perfil/password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password_actual: passActual, nueva_password: passNueva }),
      })
      const d = await r.json()
      if (!r.ok) { setError(d.detail || 'Error'); return }
      setMsg('Contraseña cambiada'); setPassActual(''); setPassNueva('')
    } catch { setError('Error de conexión') }
    finally { setCargando(false) }
  }

  const cancelarPlan = async () => {
    if (!confirm('¿Seguro que quieres cancelar tu suscripción?')) return
    setCargando(true)
    try {
      await apiFetch('/api/perfil/cancelar-plan', { method: 'POST' })
      setMsg('Plan cancelado'); setPlanInfo(p => ({ ...p, plan: 'free' }))
    } catch { setError('Error') }
    finally { setCargando(false) }
  }

  const planLabel = () => {
    if (!planInfo) return '...'
    if (planInfo.plan === 'trial') {
      const h = planInfo.trial_expira ? Math.max(0, Math.ceil((new Date(planInfo.trial_expira) - new Date()) / 3600000)) : 0
      return `Trial — ${h}h restantes`
    }
    if (planInfo.plan === 'vitalicio') return 'Vitalicio ✓'
    if (planInfo.plan === 'free') return 'Sin suscripción'
    return planInfo.plan.charAt(0).toUpperCase() + planInfo.plan.slice(1)
  }

  return (
    <>
      {/* Botón hamburguesa */}
      <button
        onClick={() => setAbierto(true)}
        className="flex flex-col justify-center items-center gap-1.5 w-9 h-9 rounded-xl hover:bg-white/10 transition-colors"
        aria-label="Menú"
      >
        <span className="block w-5 h-0.5 bg-white rounded-full" />
        <span className="block w-5 h-0.5 bg-white rounded-full" />
        <span className="block w-5 h-0.5 bg-white rounded-full" />
      </button>

      {/* Overlay */}
      {abierto && (
        <div className="fixed inset-0 z-[60]" onClick={cerrar}>
          <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" />
        </div>
      )}

      {/* Panel lateral */}
      <div className={`fixed top-0 right-0 h-full w-80 max-w-[90vw] z-[70] bg-white shadow-2xl flex flex-col transition-transform duration-300
        ${abierto ? 'translate-x-0' : 'translate-x-full'}`}>

        {/* Header panel */}
        <div className="bg-gray-900 text-white px-5 py-4 flex items-center justify-between shrink-0">
          <div>
            <p className="font-bold text-sm">{usuario?.nombre || usuario?.email?.split('@')[0]}</p>
            <p className="text-xs text-gray-400 mt-0.5">{planLabel()}</p>
          </div>
          <button onClick={cerrar} className="text-gray-400 hover:text-white text-xl w-8 h-8 flex items-center justify-center rounded-lg hover:bg-white/10">✕</button>
        </div>

        <div className="flex-1 overflow-y-auto">

          {/* Sección principal: nav */}
          {!seccion && (
            <div className="py-3">
              {/* Links navegación */}
              <p className="text-[11px] font-semibold text-gray-400 uppercase tracking-wider px-5 py-2">Navegar</p>
              {NAV_LINKS.map(({ to, label, icon }) => (
                <NavLink key={to} to={to} end onClick={cerrar}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-5 py-2.5 text-sm font-medium transition-colors
                    ${isActive ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:bg-gray-50'}`}>
                  <span className="text-lg w-6 text-center">{icon}</span>
                  {label}
                </NavLink>
              ))}

              {/* Divider */}
              <div className="border-t border-gray-100 my-3 mx-5" />

              {/* Cuenta */}
              <p className="text-[11px] font-semibold text-gray-400 uppercase tracking-wider px-5 py-2">Cuenta</p>
              {[
                { label: 'Editar perfil', icon: '👤', action: () => setSeccion('perfil') },
                { label: 'Cambiar contraseña', icon: '🔐', action: () => setSeccion('password') },
                { label: 'Mi suscripción', icon: '💳', action: () => setSeccion('plan') },
              ].map(({ label, icon, action }) => (
                <button key={label} onClick={action}
                  className="w-full flex items-center gap-3 px-5 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50 text-left transition-colors">
                  <span className="text-lg w-6 text-center">{icon}</span>
                  {label}
                </button>
              ))}

              <div className="border-t border-gray-100 my-3 mx-5" />

              <button onClick={() => { onLogout(); cerrar() }}
                className="w-full flex items-center gap-3 px-5 py-2.5 text-sm font-medium text-red-500 hover:bg-red-50 transition-colors">
                <span className="text-lg w-6 text-center">↩️</span>
                Cerrar sesión
              </button>
            </div>
          )}

          {/* Subsección: Perfil */}
          {seccion === 'perfil' && (
            <div className="p-5">
              <button onClick={() => { setSeccion(null); setMsg(''); setError('') }} className="flex items-center gap-1 text-sm text-gray-500 mb-5 hover:text-gray-700">
                ← Volver
              </button>
              <h2 className="font-bold text-gray-800 mb-4">Editar perfil</h2>

              <div className="space-y-4">
                <div>
                  <label className="text-xs font-medium text-gray-500 mb-1 block">Nombre</label>
                  <input value={nombre} onChange={e => setNombre(e.target.value)}
                    className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-gray-200" />
                </div>
                <div>
                  <label className="text-xs font-medium text-gray-500 mb-1 block">Email</label>
                  <input value={email} onChange={e => setEmail(e.target.value)} type="email"
                    className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-gray-200" />
                </div>

                {msg && <p className="text-green-600 text-sm">{msg}</p>}
                {error && <p className="text-red-500 text-sm">{error}</p>}

                <button onClick={guardarPerfil} disabled={cargando}
                  className="w-full bg-gray-900 text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-gray-800 disabled:opacity-50">
                  {cargando ? 'Guardando...' : 'Guardar cambios'}
                </button>
              </div>
            </div>
          )}

          {/* Subsección: Password */}
          {seccion === 'password' && (
            <div className="p-5">
              <button onClick={() => { setSeccion(null); setMsg(''); setError('') }} className="flex items-center gap-1 text-sm text-gray-500 mb-5 hover:text-gray-700">
                ← Volver
              </button>
              <h2 className="font-bold text-gray-800 mb-4">Cambiar contraseña</h2>

              <div className="space-y-4">
                <div>
                  <label className="text-xs font-medium text-gray-500 mb-1 block">Contraseña actual</label>
                  <input value={passActual} onChange={e => setPassActual(e.target.value)} type="password"
                    className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-gray-200" />
                </div>
                <div>
                  <label className="text-xs font-medium text-gray-500 mb-1 block">Nueva contraseña</label>
                  <input value={passNueva} onChange={e => setPassNueva(e.target.value)} type="password"
                    className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-gray-200" />
                </div>

                {msg && <p className="text-green-600 text-sm">{msg}</p>}
                {error && <p className="text-red-500 text-sm">{error}</p>}

                <button onClick={cambiarPassword} disabled={cargando}
                  className="w-full bg-gray-900 text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-gray-800 disabled:opacity-50">
                  {cargando ? 'Guardando...' : 'Cambiar contraseña'}
                </button>
              </div>
            </div>
          )}

          {/* Subsección: Plan */}
          {seccion === 'plan' && (
            <div className="p-5">
              <button onClick={() => { setSeccion(null); setMsg(''); setError('') }} className="flex items-center gap-1 text-sm text-gray-500 mb-5 hover:text-gray-700">
                ← Volver
              </button>
              <h2 className="font-bold text-gray-800 mb-4">Mi suscripción</h2>

              <div className="bg-gray-50 rounded-2xl p-4 mb-5">
                <p className="text-xs text-gray-400 mb-1">Plan actual</p>
                <p className="text-xl font-black text-gray-800">{planLabel()}</p>
                {planInfo?.plan_expira && (
                  <p className="text-xs text-gray-400 mt-1">Renueva: {new Date(planInfo.plan_expira).toLocaleDateString('es-ES')}</p>
                )}
              </div>

              {msg && <p className="text-green-600 text-sm mb-3">{msg}</p>}
              {error && <p className="text-red-500 text-sm mb-3">{error}</p>}

              <button onClick={() => { cerrar(); navigate('/planes') }}
                className="w-full bg-gray-900 text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-gray-800 mb-3">
                Cambiar plan
              </button>

              {planInfo?.plan && !['free', 'trial', 'vitalicio'].includes(planInfo.plan) && (
                <button onClick={cancelarPlan} disabled={cargando}
                  className="w-full border border-red-200 text-red-500 py-2.5 rounded-xl text-sm font-medium hover:bg-red-50 disabled:opacity-50">
                  {cargando ? '...' : 'Cancelar suscripción'}
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  )
}
