import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export default function PagoOk() {
  const navigate = useNavigate()

  useEffect(() => {
    // Forzar reload del plan en el próximo fetch
    setTimeout(() => navigate('/'), 5000)
  }, [])

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-b from-green-50 to-white">
      <div className="bg-white rounded-2xl shadow-lg p-10 max-w-sm w-full text-center">
        <div className="text-6xl mb-4">🎉</div>
        <h1 className="text-2xl font-black text-gray-800 mb-2">¡Pago completado!</h1>
        <p className="text-gray-500 mb-6">Tu plan ya está activo. Ahora tienes acceso completo a todos los contenidos.</p>
        <button onClick={() => navigate('/')} className="w-full bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700">
          Empezar a estudiar
        </button>
        <p className="text-xs text-gray-400 mt-4">Redirigiendo automáticamente en 5 segundos...</p>
      </div>
    </div>
  )
}
