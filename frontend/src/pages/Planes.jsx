import { useState, useEffect } from 'react'
import { apiFetch } from '../utils/api'
import { useNavigate } from 'react-router-dom'

export default function Planes() {
  const navigate = useNavigate()
  const [plan, setPlan] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    apiFetch('/api/plan').then(r => r.json()).then(setPlan).catch(() => {})
  }, [])

  const suscribirse = async (tipoPlan) => {
    setCargando(true)
    setError('')
    try {
      const r = await apiFetch('/api/stripe/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan: tipoPlan }),
      })
      const data = await r.json()
      if (!r.ok) { setError(data.detail || 'Error al procesar pago'); return }
      window.location.href = data.url
    } catch {
      setError('Error de conexión')
    } finally {
      setCargando(false)
    }
  }

  const trialdHorasRestantes = () => {
    if (!plan?.trial_expira) return null
    const diff = new Date(plan.trial_expira) - new Date()
    if (diff <= 0) return 0
    return Math.ceil(diff / 3600000)
  }

  const horas = trialdHorasRestantes()

  const planes = [
    {
      id: 'basico',
      nombre: 'Básico',
      precio: '4,99€',
      periodo: '/mes',
      descripcion: 'Acceso completo a todo el contenido sin límites',
      features: ['Constitución completa', 'Tests ilimitados', 'Flashcards', 'Estadísticas', 'Oposiciones temario'],
      color: 'blue',
      popular: false,
    },
    {
      id: 'pro',
      nombre: 'Pro',
      precio: '9,99€',
      periodo: '/mes',
      descripcion: 'Todo lo del Básico más IA tutora y simulacros oficiales',
      features: ['Todo lo del Básico', 'Simulacros cronometrados', 'IA tutora explicaciones', 'Historial simulacros', 'Soporte prioritario'],
      color: 'purple',
      popular: true,
    },
    {
      id: 'vitalicio',
      nombre: 'Vitalicio',
      precio: '49,99€',
      periodo: ' único',
      descripcion: 'Acceso de por vida a todo, sin pagos recurrentes',
      features: ['Todo lo del Pro', 'Acceso de por vida', 'Actualizaciones incluidas', 'Sin suscripción'],
      color: 'green',
      popular: false,
    },
  ]

  const colorMap = {
    blue: { btn: 'bg-blue-600 hover:bg-blue-700', badge: 'bg-blue-100 text-blue-700', border: 'border-blue-200', check: 'text-blue-500' },
    purple: { btn: 'bg-purple-600 hover:bg-purple-700', badge: 'bg-purple-100 text-purple-700', border: 'border-purple-400 ring-2 ring-purple-200', check: 'text-purple-500' },
    green: { btn: 'bg-green-600 hover:bg-green-700', badge: 'bg-green-100 text-green-700', border: 'border-green-200', check: 'text-green-500' },
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white pb-20 px-4 pt-6">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-black text-gray-900 mb-2">Elige tu plan</h1>
          <p className="text-gray-500">Prepara tus oposiciones con la mejor plataforma</p>

          {plan && (
            <div className={`mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium
              ${plan.premium ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>
              {plan.premium
                ? `✅ Plan activo: ${plan.plan}`
                : horas !== null
                  ? horas > 0
                    ? `⏱ Trial: ${horas}h restantes`
                    : '⚠️ Trial expirado'
                  : ''}
            </div>
          )}
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 rounded-xl px-4 py-3 text-sm mb-6">{error}</div>
        )}

        <div className="grid gap-4 md:grid-cols-3">
          {planes.map(p => {
            const c = colorMap[p.color]
            const esActual = plan?.plan === p.id
            return (
              <div key={p.id} className={`bg-white rounded-2xl border-2 ${c.border} p-6 flex flex-col relative`}>
                {p.popular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                    <span className="bg-purple-600 text-white text-xs font-bold px-3 py-1 rounded-full">MÁS POPULAR</span>
                  </div>
                )}
                <div className="mb-4">
                  <h2 className="text-xl font-bold text-gray-800">{p.nombre}</h2>
                  <div className="mt-2 flex items-baseline gap-0.5">
                    <span className="text-3xl font-black text-gray-900">{p.precio}</span>
                    <span className="text-gray-400 text-sm">{p.periodo}</span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1.5">{p.descripcion}</p>
                </div>

                <ul className="space-y-2 mb-6 flex-1">
                  {p.features.map((f, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-gray-600">
                      <span className={`${c.check} font-bold mt-0.5`}>✓</span>
                      {f}
                    </li>
                  ))}
                </ul>

                {esActual ? (
                  <div className="w-full py-2.5 rounded-xl bg-gray-100 text-gray-500 text-sm font-medium text-center">
                    Plan actual
                  </div>
                ) : (
                  <button
                    onClick={() => suscribirse(p.id)}
                    disabled={cargando}
                    className={`w-full py-2.5 rounded-xl text-white text-sm font-semibold ${c.btn} disabled:opacity-50 transition-colors`}
                  >
                    {cargando ? 'Procesando...' : `Elegir ${p.nombre}`}
                  </button>
                )}
              </div>
            )
          })}
        </div>

        <p className="text-center text-xs text-gray-400 mt-8">
          Pagos seguros con Stripe · Cancela cuando quieras · IVA incluido
        </p>
      </div>
    </div>
  )
}
