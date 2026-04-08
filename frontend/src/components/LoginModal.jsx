import { useState } from 'react'

export default function LoginModal({ onLogin }) {
  const [modo, setModo] = useState('login') // 'login' | 'registro'
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [nombre, setNombre] = useState('')
  const [error, setError] = useState('')
  const [cargando, setCargando] = useState(false)

  const limpiarError = () => setError('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    const emailLimpio = email.trim().toLowerCase()
    if (!emailLimpio.includes('@')) { setError('Introduce un email válido'); return }
    if (password.length < 6) { setError('La contraseña debe tener al menos 6 caracteres'); return }

    setCargando(true)
    setError('')

    const endpoint = modo === 'registro' ? '/api/auth/registro' : '/api/auth/login'
    const body = modo === 'registro'
      ? { email: emailLimpio, password, nombre: nombre.trim() || null }
      : { email: emailLimpio, password }

    try {
      const resp = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      const data = await resp.json()

      if (!resp.ok) {
        setError(data.detail || 'Error al iniciar sesión')
        return
      }

      // Guardar token y datos de sesión
      localStorage.setItem('token', data.token)
      localStorage.setItem('usuario', JSON.stringify({ email: data.email, nombre: data.nombre }))

      // Sincronizar progreso del servidor
      try {
        const progresoResp = await fetch('/api/progreso', {
          headers: { Authorization: `Bearer ${data.token}` }
        })
        const progreso = await progresoResp.json()
        if (Object.keys(progreso.estudiados || {}).length > 0)
          localStorage.setItem('estudiados', JSON.stringify(progreso.estudiados))
        if (Object.keys(progreso.notas || {}).length > 0)
          localStorage.setItem('notas', JSON.stringify(progreso.notas))
      } catch { /* sin progreso previo */ }

      onLogin({ email: data.email, nombre: data.nombre })
    } catch {
      setError('Error de conexión. ¿Está el servidor en marcha?')
    } finally {
      setCargando(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-brand-900/80 backdrop-blur-sm px-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-8">

        {/* Logo */}
        <div className="text-center mb-6">
          <div className="text-5xl mb-3">📜</div>
          <h1 className="text-2xl font-bold text-brand-700">Constitución Española</h1>
          <p className="text-sm text-gray-400 mt-1">Estudio para oposiciones</p>
        </div>

        {/* Tabs login / registro */}
        <div className="flex rounded-xl overflow-hidden border border-gray-200 mb-5">
          {['login', 'registro'].map(m => (
            <button
              key={m}
              onClick={() => { setModo(m); limpiarError() }}
              className={`flex-1 py-2 text-sm font-semibold transition-colors ${
                modo === m
                  ? 'bg-brand-700 text-white'
                  : 'text-gray-500 hover:bg-gray-50'
              }`}
            >
              {m === 'login' ? 'Entrar' : 'Crear cuenta'}
            </button>
          ))}
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          {modo === 'registro' && (
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Nombre (opcional)</label>
              <input
                type="text"
                value={nombre}
                onChange={e => setNombre(e.target.value)}
                placeholder="María García"
                className="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
              />
            </div>
          )}

          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={e => { setEmail(e.target.value); limpiarError() }}
              placeholder="tu@email.com"
              required
              autoComplete="email"
              className="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={e => { setPassword(e.target.value); limpiarError() }}
              placeholder={modo === 'registro' ? 'Mínimo 6 caracteres' : '••••••••'}
              required
              autoComplete={modo === 'login' ? 'current-password' : 'new-password'}
              className="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
            />
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 text-sm px-3 py-2 rounded-xl">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={cargando}
            className="w-full bg-brand-700 hover:bg-brand-900 text-white font-semibold py-3 rounded-xl transition-colors disabled:opacity-60 mt-1"
          >
            {cargando
              ? 'Un momento...'
              : modo === 'login' ? 'Entrar →' : 'Crear cuenta →'}
          </button>
        </form>

        <p className="text-xs text-gray-300 text-center mt-4">
          Sin publicidad · 100% gratis · Actualizado desde el BOE
        </p>
      </div>
    </div>
  )
}
