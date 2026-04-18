import { useNavigate } from 'react-router-dom'
import { usePlan } from '../hooks/usePlan'

export default function PremiumGate({ children, mensaje = 'Este contenido requiere suscripción' }) {
  const navigate = useNavigate()
  const plan = usePlan()

  // Si el plan aún no cargó, spinner pequeño (evita exponer contenido premium)
  if (!plan) return (
    <div className="flex justify-center mt-24">
      <div className="w-7 h-7 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  if (plan.premium) return children

  return (
    <div className="min-h-[60vh] flex items-center justify-center p-6">
      <div className="bg-white rounded-2xl shadow-lg p-8 max-w-sm w-full text-center border border-gray-100">
        <div className="w-14 h-14 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4 text-2xl">🔒</div>
        <h2 className="text-lg font-bold text-gray-800 mb-2">Acceso premium</h2>
        <p className="text-gray-500 text-sm mb-6 leading-relaxed">{mensaje}</p>
        <button
          onClick={() => navigate('/planes')}
          className="w-full bg-gray-900 text-white py-3 rounded-xl font-semibold text-sm hover:bg-gray-800 transition-colors">
          Ver planes →
        </button>
        <p className="text-xs text-gray-400 mt-3">Desde 4,99€/mes · Cancela cuando quieras</p>
      </div>
    </div>
  )
}
