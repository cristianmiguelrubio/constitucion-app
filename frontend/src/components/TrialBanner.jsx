import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiFetch } from '../utils/api'

export default function TrialBanner() {
  const navigate = useNavigate()
  const [info, setInfo] = useState(null)

  useEffect(() => {
    apiFetch('/api/plan').then(r => r.json()).then(setInfo).catch(() => {})
  }, [])

  if (!info) return null

  const horasRestantes = () => {
    if (!info.trial_expira) return null
    const diff = new Date(info.trial_expira) - new Date()
    if (diff <= 0) return 0
    return Math.ceil(diff / 3600000)
  }

  const horas = horasRestantes()

  // No mostrar si tiene plan de pago
  if (info.plan !== 'trial' && info.plan !== 'free') return null
  // Trial activo con más de 12h: no molestar
  if (info.plan === 'trial' && horas !== null && horas > 12) return null

  const expirado = info.plan === 'free' || horas === 0

  return (
    <div className="fixed bottom-4 left-0 right-0 z-40 px-4">
      <div className={`max-w-lg mx-auto rounded-2xl shadow-lg px-4 py-3 flex items-center justify-between gap-3
        ${expirado ? 'bg-red-600 text-white' : 'bg-amber-500 text-white'}`}>
        <div className="flex-1 min-w-0">
          {expirado
            ? <p className="text-sm font-semibold">Tu periodo de prueba ha expirado</p>
            : <p className="text-sm font-semibold">⏱ Trial: {horas}h restantes</p>
          }
          <p className="text-xs opacity-80 mt-0.5">Suscríbete para no perder el acceso</p>
        </div>
        <button
          onClick={() => navigate('/planes')}
          className="bg-white text-gray-800 px-3 py-1.5 rounded-xl text-xs font-bold shrink-0 hover:bg-gray-100">
          Ver planes
        </button>
      </div>
    </div>
  )
}
