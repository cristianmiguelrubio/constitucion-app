import { useEffect, useState } from 'react'

export function useToast() {
  const [toasts, setToasts] = useState([])

  const show = (msg, tipo = 'info', duracion = 5000) => {
    const id = Date.now()
    setToasts(t => [...t, { id, msg, tipo }])
    setTimeout(() => setToasts(t => t.filter(x => x.id !== id)), duracion)
  }

  return { toasts, show }
}

export function ToastContainer({ toasts }) {
  return (
    <div className="fixed top-4 left-0 right-0 z-[100] flex flex-col items-center gap-2 px-4 pointer-events-none">
      {toasts.map(t => (
        <Toast key={t.id} msg={t.msg} tipo={t.tipo} />
      ))}
    </div>
  )
}

function Toast({ msg, tipo }) {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    requestAnimationFrame(() => setVisible(true))
  }, [])

  const colors = {
    success: 'bg-green-600 text-white',
    warning: 'bg-amber-500 text-white',
    info: 'bg-blue-600 text-white',
    error: 'bg-red-600 text-white',
  }

  return (
    <div className={`pointer-events-auto max-w-sm w-full rounded-2xl shadow-xl px-5 py-4 flex items-start gap-3 transition-all duration-500
      ${colors[tipo] || colors.info}
      ${visible ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'}`}>
      <span className="text-xl shrink-0">
        {tipo === 'success' ? '🎉' : tipo === 'warning' ? '⏱' : tipo === 'error' ? '❌' : 'ℹ️'}
      </span>
      <p className="text-sm font-medium leading-snug">{msg}</p>
    </div>
  )
}
