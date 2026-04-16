import { useState, useRef, useEffect } from 'react'
import { apiFetch } from '../utils/api'

export default function ChatBot() {
  const [abierto, setAbierto] = useState(false)
  const [mensajes, setMensajes] = useState([
    { rol: 'bot', texto: '¡Hola! Soy tu asistente de oposiciones 👋 Pregúntame cualquier cosa sobre la Constitución, temarios o dudas de tu oposición.' }
  ])
  const [input, setInput] = useState('')
  const [cargando, setCargando] = useState(false)
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    if (abierto) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
      setTimeout(() => inputRef.current?.focus(), 100)
    }
  }, [abierto, mensajes])

  const enviar = async () => {
    const texto = input.trim()
    if (!texto || cargando) return
    setInput('')
    setMensajes(m => [...m, { rol: 'user', texto }])
    setCargando(true)
    try {
      const r = await apiFetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensaje: texto, historial: mensajes.slice(-6) }),
      })
      const data = await r.json()
      if (r.status === 403) {
        setMensajes(m => [...m, { rol: 'bot', texto: '🔒 El chatbot requiere plan Pro o Vitalicio. Ve a Planes para actualizarte.' }])
      } else {
        setMensajes(m => [...m, { rol: 'bot', texto: data.respuesta || 'No pude responder, inténtalo de nuevo.' }])
      }
    } catch {
      setMensajes(m => [...m, { rol: 'bot', texto: 'Error de conexión. Inténtalo de nuevo.' }])
    } finally {
      setCargando(false)
    }
  }

  return (
    <>
      {/* Botón flotante */}
      <button
        onClick={() => setAbierto(v => !v)}
        className="fixed bottom-20 right-4 z-50 w-14 h-14 rounded-full bg-gray-900 text-white shadow-xl flex items-center justify-center text-2xl hover:bg-gray-800 active:scale-95 transition-all"
        aria-label="Abrir chatbot"
      >
        {abierto ? '✕' : '🤖'}
      </button>

      {/* Ventana chat */}
      {abierto && (
        <div className="fixed bottom-36 right-4 z-50 w-[340px] max-w-[calc(100vw-2rem)] bg-white rounded-2xl shadow-2xl border border-gray-100 flex flex-col overflow-hidden"
          style={{ height: '420px' }}>

          {/* Header */}
          <div className="bg-gray-900 text-white px-4 py-3 flex items-center gap-3">
            <span className="text-xl">🤖</span>
            <div>
              <p className="text-sm font-semibold leading-none">Asistente IA</p>
              <p className="text-[11px] text-gray-400 mt-0.5">Oposiciones del Estado</p>
            </div>
          </div>

          {/* Mensajes */}
          <div className="flex-1 overflow-y-auto px-3 py-3 space-y-3">
            {mensajes.map((m, i) => (
              <div key={i} className={`flex ${m.rol === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] rounded-2xl px-3 py-2 text-sm leading-relaxed whitespace-pre-wrap
                  ${m.rol === 'user'
                    ? 'bg-gray-900 text-white rounded-br-sm'
                    : 'bg-gray-100 text-gray-800 rounded-bl-sm'}`}>
                  {m.texto}
                </div>
              </div>
            ))}
            {cargando && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-2xl rounded-bl-sm px-4 py-2.5">
                  <div className="flex gap-1">
                    <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="border-t border-gray-100 px-3 py-2.5 flex gap-2">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && !e.shiftKey && enviar()}
              placeholder="Escribe tu pregunta..."
              className="flex-1 text-sm bg-gray-50 rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-200 text-gray-800"
              disabled={cargando}
            />
            <button
              onClick={enviar}
              disabled={!input.trim() || cargando}
              className="w-9 h-9 rounded-xl bg-gray-900 text-white flex items-center justify-center disabled:opacity-30 hover:bg-gray-800 transition-colors shrink-0"
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </>
  )
}
