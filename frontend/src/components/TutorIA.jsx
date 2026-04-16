import { useState } from 'react'
import { apiFetch } from '../utils/api'

export default function TutorIA({ pregunta, respuestaUsuario, respuestaCorrecta, contexto }) {
  const [explicacion, setExplicacion] = useState('')
  const [cargando, setCargando] = useState(false)
  const [abierto, setAbierto] = useState(false)

  const explicar = async () => {
    if (explicacion) { setAbierto(true); return }
    setCargando(true)
    try {
      const r = await apiFetch('/api/tutor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pregunta, respuesta_usuario: respuestaUsuario, respuesta_correcta: respuestaCorrecta, contexto }),
      })
      if (r.status === 403) {
        setExplicacion('La IA tutora requiere plan Pro o Vitalicio. Ve a Planes para actualizarte.')
      } else {
        const data = await r.json()
        setExplicacion(data.explicacion || 'No se pudo obtener explicación')
      }
      setAbierto(true)
    } catch {
      setExplicacion('Error al conectar con la IA')
      setAbierto(true)
    } finally {
      setCargando(false)
    }
  }

  return (
    <div className="mt-3">
      <button
        onClick={explicar}
        disabled={cargando}
        className="flex items-center gap-2 text-sm text-purple-600 font-medium hover:text-purple-700 disabled:opacity-50"
      >
        <span>{cargando ? '⏳' : '🤖'}</span>
        {cargando ? 'Consultando IA...' : abierto ? 'Ocultar explicación' : 'Explicar con IA'}
      </button>

      {abierto && explicacion && (
        <div className="mt-3 bg-purple-50 border border-purple-100 rounded-xl p-4 text-sm text-gray-700 leading-relaxed whitespace-pre-line">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-purple-600 font-semibold text-xs">🤖 IA Tutora</span>
          </div>
          {explicacion}
        </div>
      )}
    </div>
  )
}
