import { useState, useEffect } from 'react'
import { apiFetch } from '../utils/api'
import { useNavigate } from 'react-router-dom'

const PLANES = [
  {
    id: 'free',
    nombre: 'Gratis',
    precio: '0€',
    periodo: '',
    subtitulo: 'Para explorar la app',
    color: 'gray',
    features: [
      { texto: 'Constitución completa', ok: true },
      { texto: 'Búsqueda de artículos', ok: true },
      { texto: 'Tests limitados (5/día)', ok: true },
      { texto: 'Simulacros oficiales', ok: false },
      { texto: 'IA tutora', ok: false },
      { texto: 'Estadísticas avanzadas', ok: false },
      { texto: 'Historial de exámenes', ok: false },
    ],
    cta: 'Plan actual',
    ctaDisabled: true,
  },
  {
    id: 'basico',
    nombre: 'Básico',
    precio: '4,99€',
    periodo: '/mes',
    subtitulo: 'Para preparar tu oposición',
    color: 'blue',
    popular: false,
    features: [
      { texto: 'Constitución completa', ok: true },
      { texto: 'Búsqueda de artículos', ok: true },
      { texto: 'Tests ilimitados', ok: true },
      { texto: 'Simulacros cronometrados', ok: true },
      { texto: 'IA tutora', ok: true },
      { texto: 'Estadísticas avanzadas', ok: true },
      { texto: 'Historial de exámenes', ok: true },
    ],
    cta: 'Empezar con Básico',
  },
  {
    id: 'pro',
    nombre: 'Pro',
    precio: '9,99€',
    periodo: '/mes',
    subtitulo: 'Para aprobar a la primera',
    color: 'purple',
    popular: true,
    features: [
      { texto: 'Todo lo del Básico', ok: true },
      { texto: 'IA tutora con explicaciones', ok: true },
      { texto: 'Simulacros ilimitados', ok: true },
      { texto: 'Análisis de errores con IA', ok: true },
      { texto: 'Estadísticas avanzadas', ok: true },
      { texto: 'Historial de exámenes', ok: true },
      { texto: 'Soporte prioritario', ok: true },
    ],
    cta: 'Empezar con Pro',
  },
  {
    id: 'vitalicio',
    nombre: 'Vitalicio',
    precio: '49,99€',
    periodo: ' único',
    subtitulo: 'Sin pagos recurrentes nunca',
    color: 'amber',
    features: [
      { texto: 'Todo lo del Pro', ok: true },
      { texto: 'Acceso de por vida', ok: true },
      { texto: 'Todas las actualizaciones', ok: true },
      { texto: 'Sin suscripción mensual', ok: true },
      { texto: 'Nuevas oposiciones incluidas', ok: true },
      { texto: 'Estadísticas avanzadas', ok: true },
      { texto: 'Soporte prioritario', ok: true },
    ],
    cta: 'Obtener acceso vitalicio',
  },
]

const COLORS = {
  gray:   { ring: 'ring-gray-200',   btn: 'bg-gray-800 hover:bg-gray-700',   badge: '',                             dot: 'bg-gray-300' },
  blue:   { ring: 'ring-blue-200',   btn: 'bg-blue-600 hover:bg-blue-700',   badge: '',                             dot: 'bg-blue-500' },
  purple: { ring: 'ring-purple-400', btn: 'bg-purple-600 hover:bg-purple-700', badge: 'bg-purple-600',              dot: 'bg-purple-500' },
  amber:  { ring: 'ring-amber-300',  btn: 'bg-amber-500 hover:bg-amber-400', badge: '',                             dot: 'bg-amber-400' },
}

export default function Planes() {
  const navigate = useNavigate()
  const [planActual, setPlanActual] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    apiFetch('/api/plan').then(r => r.json()).then(setPlanActual).catch(() => {})
  }, [])

  const horasRestantes = () => {
    if (!planActual?.trial_expira) return null
    const diff = new Date(planActual.trial_expira) - new Date()
    if (diff <= 0) return 0
    return Math.ceil(diff / 3600000)
  }

  const suscribirse = async (id) => {
    if (id === 'free') return
    setCargando(true); setError('')
    try {
      const r = await apiFetch('/api/stripe/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan: id }),
      })
      const data = await r.json()
      if (!r.ok) { setError(data.detail || 'Error'); return }
      window.location.href = data.url
    } catch { setError('Error de conexión') }
    finally { setCargando(false) }
  }

  const horas = horasRestantes()
  const esPlanActual = (id) => planActual?.plan === id

  return (
    <div className="min-h-screen bg-white pb-24">
      {/* Hero */}
      <div className="bg-gradient-to-b from-gray-950 to-gray-900 text-white pt-12 pb-16 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <p className="text-xs font-semibold tracking-widest text-gray-400 uppercase mb-3">Oposiciones del Estado</p>
          <h1 className="text-4xl font-black mb-3 leading-tight">
            El plan adecuado<br />para tu oposición
          </h1>
          <p className="text-gray-400 text-base">
            Empieza gratis 24 horas. Sin tarjeta de crédito.
          </p>

          {/* Trial badge */}
          {planActual?.plan === 'trial' && horas !== null && (
            <div className={`inline-flex items-center gap-2 mt-5 px-4 py-2 rounded-full text-sm font-medium
              ${horas > 0 ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-red-500/20 text-red-300 border border-red-500/30'}`}>
              <span className="animate-pulse">●</span>
              {horas > 0 ? `Trial activo — ${horas}h restantes` : 'Trial expirado — elige un plan'}
            </div>
          )}
          {planActual?.plan && planActual.plan !== 'trial' && planActual.plan !== 'free' && (
            <div className="inline-flex items-center gap-2 mt-5 px-4 py-2 rounded-full text-sm font-medium bg-green-500/20 text-green-300 border border-green-500/30">
              ✓ Plan activo: {planActual.plan}
            </div>
          )}
        </div>
      </div>

      {/* Cards */}
      <div className="max-w-5xl mx-auto px-4 -mt-6">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 rounded-xl px-4 py-3 text-sm mb-6">{error}</div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {PLANES.map(plan => {
            const c = COLORS[plan.color]
            const esActual = esPlanActual(plan.id)
            return (
              <div key={plan.id}
                className={`relative bg-white rounded-2xl border ring-2 ${c.ring} p-5 flex flex-col
                  ${plan.popular ? 'shadow-xl scale-[1.02]' : 'shadow-sm'}`}>

                {plan.popular && (
                  <div className={`absolute -top-3 left-1/2 -translate-x-1/2 ${c.badge} text-white text-[11px] font-bold px-3 py-1 rounded-full whitespace-nowrap`}>
                    MÁS POPULAR
                  </div>
                )}

                <div className="mb-4">
                  <div className={`w-2 h-2 rounded-full ${c.dot} mb-3`} />
                  <h2 className="text-lg font-bold text-gray-900">{plan.nombre}</h2>
                  <p className="text-xs text-gray-400 mt-0.5">{plan.subtitulo}</p>
                  <div className="mt-3 flex items-baseline gap-0.5">
                    <span className="text-3xl font-black text-gray-900">{plan.precio}</span>
                    <span className="text-sm text-gray-400">{plan.periodo}</span>
                  </div>
                </div>

                <ul className="space-y-2.5 mb-6 flex-1">
                  {plan.features.map((f, i) => (
                    <li key={i} className={`flex items-start gap-2 text-sm ${f.ok ? 'text-gray-700' : 'text-gray-300'}`}>
                      <span className={`shrink-0 mt-0.5 font-bold ${f.ok ? 'text-green-500' : 'text-gray-200'}`}>
                        {f.ok ? '✓' : '✗'}
                      </span>
                      {f.texto}
                    </li>
                  ))}
                </ul>

                {esActual ? (
                  <div className="w-full py-2.5 rounded-xl bg-gray-100 text-gray-400 text-sm font-medium text-center">
                    Plan actual
                  </div>
                ) : plan.ctaDisabled ? (
                  <div className="w-full py-2.5 rounded-xl bg-gray-100 text-gray-400 text-sm font-medium text-center">
                    {plan.cta}
                  </div>
                ) : (
                  <button
                    onClick={() => suscribirse(plan.id)}
                    disabled={cargando}
                    className={`w-full py-2.5 rounded-xl text-white text-sm font-semibold ${c.btn} disabled:opacity-50 transition-all active:scale-95`}>
                    {cargando ? '...' : plan.cta}
                  </button>
                )}
              </div>
            )
          })}
        </div>

        {/* Comparativa rápida */}
        <div className="mt-12 text-center">
          <p className="text-xs text-gray-400 mb-6 font-medium tracking-wide uppercase">Incluido en todos los planes de pago</p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-2xl mx-auto">
            {[
              { icon: '📜', texto: 'Constitución completa' },
              { icon: '🧠', texto: 'Tests sin límites' },
              { icon: '📊', texto: 'Estadísticas' },
              { icon: '🔒', texto: 'Cancela cuando quieras' },
            ].map((item, i) => (
              <div key={i} className="flex flex-col items-center gap-1.5 bg-gray-50 rounded-xl p-4">
                <span className="text-2xl">{item.icon}</span>
                <span className="text-xs text-gray-500 font-medium text-center leading-tight">{item.texto}</span>
              </div>
            ))}
          </div>
        </div>

        <p className="text-center text-xs text-gray-300 mt-8">
          Pagos seguros con Stripe · Visa, Mastercard, Apple Pay, Google Pay · IVA incluido
        </p>
      </div>
    </div>
  )
}
