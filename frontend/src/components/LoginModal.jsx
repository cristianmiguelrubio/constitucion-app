import { useState } from 'react'
import { apiFetch } from '../utils/api'

export default function LoginModal({ onLogin }) {
  const [modo, setModo] = useState('login') // 'login' | 'registro' | 'recuperar' | 'codigo'
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [nombre, setNombre] = useState('')
  const [codigo, setCodigo] = useState('')
  const [nuevaPass, setNuevaPass] = useState('')
  const [error, setError] = useState('')
  const [cargando, setCargando] = useState(false)
  const [devCodigo, setDevCodigo] = useState(null)

  const limpiarError = () => setError('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    const emailLimpio = email.trim().toLowerCase()
    if (!emailLimpio.includes('@')) { setError('Introduce un email válido'); return }
    if (password.length < 6) { setError('La contraseña debe tener al menos 6 caracteres'); return }

    setCargando(true); setError('')
    const endpoint = modo === 'registro' ? '/api/auth/registro' : '/api/auth/login'
    const body = modo === 'registro'
      ? { email: emailLimpio, password, nombre: nombre.trim() || null }
      : { email: emailLimpio, password }

    try {
      const resp = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      let data
      try { data = await resp.json() } catch { setError(`Error del servidor (${resp.status})`); return }
      if (!resp.ok) { setError(data.detail || 'Error al iniciar sesión'); return }

      localStorage.setItem('token', data.token)
      localStorage.setItem('usuario', JSON.stringify({ email: data.email, nombre: data.nombre }))
      try {
        const pr = await apiFetch('/api/progreso')
        const progreso = await pr.json()
        if (Object.keys(progreso.estudiados || {}).length > 0) localStorage.setItem('estudiados', JSON.stringify(progreso.estudiados))
        if (Object.keys(progreso.notas || {}).length > 0) localStorage.setItem('notas', JSON.stringify(progreso.notas))
        // Cargar temas completados
        const tc = await apiFetch('/api/temas-completados')
        const temas = await tc.json()
        temas.forEach(({ slug, numero }) => {
          localStorage.setItem(`quiz_ok_${slug}_${numero}`, '1')
        })
      } catch {}
      onLogin({ email: data.email, nombre: data.nombre })
    } catch { setError('Error de conexión. Inténtalo de nuevo.') }
    finally { setCargando(false) }
  }

  const handleRecuperar = async (e) => {
    e.preventDefault()
    const emailLimpio = email.trim().toLowerCase()
    if (!emailLimpio.includes('@')) { setError('Introduce un email válido'); return }
    setCargando(true); setError('')
    try {
      const resp = await fetch('/api/auth/recuperar', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: emailLimpio }) })
      let data = {}
      try { data = await resp.json() } catch {}
      if (data.dev_codigo) setDevCodigo(data.dev_codigo)
      setModo('codigo') // avanzar siempre — no revelar si el email existe
    } catch { setError('Error de conexión') }
    finally { setCargando(false) }
  }

  const handleReset = async (e) => {
    e.preventDefault()
    if (nuevaPass.length < 6) { setError('Mínimo 6 caracteres'); return }
    if (codigo.length !== 6) { setError('El código tiene 6 dígitos'); return }
    setCargando(true); setError('')
    try {
      const resp = await fetch('/api/auth/reset', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: email.trim().toLowerCase(), codigo, nueva_password: nuevaPass }) })
      const data = await resp.json()
      if (!resp.ok) { setError(data.detail || 'Código incorrecto'); return }
      localStorage.setItem('token', data.token)
      localStorage.setItem('usuario', JSON.stringify({ email: data.email, nombre: data.nombre }))
      try {
        const tc = await apiFetch('/api/temas-completados')
        const temas = await tc.json()
        temas.forEach(({ slug, numero }) => localStorage.setItem(`quiz_ok_${slug}_${numero}`, '1'))
      } catch {}
      onLogin({ email: data.email, nombre: data.nombre })
    } catch { setError('Error de conexión') }
    finally { setCargando(false) }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-brand-900/80 backdrop-blur-sm">
      <div className="bg-white w-full sm:max-w-sm sm:mx-4 rounded-t-3xl sm:rounded-2xl shadow-2xl p-6 pb-6" style={{ marginBottom: '56px' }}>

        <div className="w-10 h-1 bg-gray-200 rounded-full mx-auto mb-5 sm:hidden" />

        {/* Logo */}
        <div className="text-center mb-5">
          <div className="text-4xl mb-2">📜</div>
          <h1 className="text-xl font-bold text-brand-700">Oposiciones del Estado</h1>
          <p className="text-xs text-gray-400 mt-1">Estudio para oposiciones</p>
        </div>

        {/* ── Recuperar: paso 1 (email) ── */}
        {modo === 'recuperar' && (
          <form onSubmit={handleRecuperar} className="space-y-3">
            <button type="button" onClick={() => { setModo('login'); limpiarError() }} className="text-xs text-gray-400 mb-1">← Volver</button>
            <p className="text-sm text-gray-600 mb-3">Introduce tu email y te enviaremos un código de 6 dígitos.</p>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Email</label>
              <input type="email" value={email} onChange={e => { setEmail(e.target.value); limpiarError() }}
                placeholder="tu@email.com" required autoComplete="email"
                className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
            </div>
            {error && <div className="bg-red-50 border border-red-200 text-red-600 text-sm px-3 py-2.5 rounded-xl">{error}</div>}
            <button type="submit" disabled={cargando} className="w-full bg-brand-700 text-white font-semibold py-3.5 rounded-xl disabled:opacity-60">
              {cargando ? 'Enviando...' : 'Enviar código →'}
            </button>
          </form>
        )}

        {/* ── Recuperar: paso 2 (código + nueva contraseña) ── */}
        {modo === 'codigo' && (
          <form onSubmit={handleReset} className="space-y-3">
            <p className="text-sm text-gray-600 mb-1">Introduce el código que te enviamos y tu nueva contraseña.</p>
            {devCodigo && (
              <div className="bg-amber-50 border border-amber-200 rounded-xl px-3 py-2.5 text-sm">
                <p className="text-amber-700 font-medium">Email no disponible — usa este código:</p>
                <p className="text-amber-600 text-xl font-bold tracking-widest text-center py-1">{devCodigo}</p>
              </div>
            )}
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Código (6 dígitos)</label>
              <input type="text" value={codigo} onChange={e => { setCodigo(e.target.value.replace(/\D/g, '').slice(0, 6)); limpiarError() }}
                placeholder="123456" inputMode="numeric" maxLength={6}
                className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm text-center tracking-[0.3em] font-bold focus:outline-none focus:ring-2 focus:ring-brand-500" />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Nueva contraseña</label>
              <input type="password" value={nuevaPass} onChange={e => { setNuevaPass(e.target.value); limpiarError() }}
                placeholder="Mínimo 6 caracteres" autoComplete="new-password"
                className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
            </div>
            {error && <div className="bg-red-50 border border-red-200 text-red-600 text-sm px-3 py-2.5 rounded-xl">{error}</div>}
            <button type="submit" disabled={cargando} className="w-full bg-brand-700 text-white font-semibold py-3.5 rounded-xl disabled:opacity-60">
              {cargando ? 'Verificando...' : 'Cambiar contraseña →'}
            </button>
            <button type="button" onClick={() => setModo('recuperar')} className="w-full text-xs text-gray-400 pt-1">Reenviar código</button>
          </form>
        )}

        {/* ── Login / Registro ── */}
        {(modo === 'login' || modo === 'registro') && (
          <>
            <div className="flex rounded-xl overflow-hidden border border-gray-200 mb-4">
              {['login', 'registro'].map(m => (
                <button key={m} onClick={() => { setModo(m); limpiarError() }}
                  className={`flex-1 py-2.5 text-sm font-semibold transition-colors ${modo === m ? 'bg-brand-700 text-white' : 'text-gray-500 active:bg-gray-50'}`}>
                  {m === 'login' ? 'Entrar' : 'Crear cuenta'}
                </button>
              ))}
            </div>

            <form onSubmit={handleSubmit} className="space-y-3">
              {modo === 'registro' && (
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Nombre (opcional)</label>
                  <input type="text" value={nombre} onChange={e => setNombre(e.target.value)} placeholder="María García"
                    className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
                </div>
              )}
              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">Email</label>
                <input type="email" value={email} onChange={e => { setEmail(e.target.value); limpiarError() }}
                  placeholder="tu@email.com" required autoComplete="email" inputMode="email"
                  className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">Contraseña</label>
                <input type="password" value={password} onChange={e => { setPassword(e.target.value); limpiarError() }}
                  placeholder={modo === 'registro' ? 'Mínimo 6 caracteres' : '••••••••'} required
                  autoComplete={modo === 'login' ? 'current-password' : 'new-password'}
                  className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
              </div>
              {error && <div className="bg-red-50 border border-red-200 text-red-600 text-sm px-3 py-2.5 rounded-xl">{error}</div>}
              <button type="submit" disabled={cargando}
                className="w-full bg-brand-700 active:bg-brand-900 text-white font-semibold py-3.5 rounded-xl disabled:opacity-60 text-base mt-1">
                {cargando ? 'Un momento...' : modo === 'login' ? 'Entrar →' : 'Crear cuenta →'}
              </button>
              {modo === 'login' && (
                <button type="button" onClick={() => { setModo('recuperar'); limpiarError() }}
                  className="w-full text-xs text-gray-400 pt-1 hover:text-brand-500 transition-colors">
                  ¿Olvidaste tu contraseña?
                </button>
              )}
            </form>
          </>
        )}

        <p className="text-xs text-gray-300 text-center mt-4">Sin publicidad · 100% gratis · Actualizado desde el BOE</p>
      </div>
    </div>
  )
}
