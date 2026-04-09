import { useEffect, useState } from 'react'
import { apiFetch } from '../utils/api'

function formatTiempo(s) {
  const m = Math.floor(s / 60), sec = s % 60
  return `${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}`
}

export default function Flashcards() {
  const [articulos, setArticulos] = useState([])
  const [cargando, setCargando] = useState(true)
  const [filtro, setFiltro] = useState('todos') // 'todos' | 'pendientes' | 'estudiados'
  const [indice, setIndice] = useState(0)
  const [volteada, setVolteada] = useState(false)
  const [fase, setFase] = useState('config') // 'config' | 'repaso' | 'fin'
  const [cronometro, setCronometro] = useState(0)
  const [correctas, setCorrectas] = useState(0)

  useEffect(() => {
    apiFetch('/api/articulos')
      .then(r => r.json())
      .then(data => { setArticulos(data); setCargando(false) })
      .catch(() => setCargando(false))
  }, [])

  useEffect(() => {
    if (fase !== 'repaso') return
    const id = setInterval(() => setCronometro(s => s + 1), 1000)
    return () => clearInterval(id)
  }, [fase])

  const estudiados = (() => {
    try { return JSON.parse(localStorage.getItem('estudiados') || '{}') } catch { return {} }
  })()

  const mazo = articulos.filter(a => {
    if (filtro === 'pendientes') return !estudiados[a.numero]
    if (filtro === 'estudiados') return !!estudiados[a.numero]
    return true
  })

  const actual = mazo[indice]
  const progreso = mazo.length ? Math.round((indice / mazo.length) * 100) : 0

  const siguiente = (sabia) => {
    if (sabia) {
      setCorrectas(c => c + 1)
      // Marcar como estudiado en localStorage y sincronizar con servidor
      if (actual?.numero) {
        const est = (() => { try { return JSON.parse(localStorage.getItem('estudiados') || '{}') } catch { return {} } })()
        est[actual.numero] = true
        localStorage.setItem('estudiados', JSON.stringify(est))
        apiFetch('/api/progreso', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ articulo_numero: actual.numero, estudiado: true, nota: '' }),
        }).catch(() => {})
      }
    }
    setVolteada(false)
    if (indice + 1 >= mazo.length) {
      setFase('fin')
    } else {
      setTimeout(() => setIndice(i => i + 1), 150)
    }
  }

  const reiniciar = () => {
    setIndice(0)
    setVolteada(false)
    setCorrectas(0)
    setCronometro(0)
    setFase('config')
  }

  // ── Config ──
  if (fase === 'config') return (
    <div className="max-w-xl mx-auto">
      <div className="relative rounded-2xl overflow-hidden mb-5 shadow-lg" style={{ height: '110px' }}>
        <div className="absolute inset-0 bg-gradient-to-br from-violet-600 to-purple-800" />
        <div className="absolute inset-0 flex flex-col justify-center px-5">
          <h1 className="text-2xl font-black text-white">Flashcards</h1>
          <p className="text-xs text-white/70 mt-1">Repasa los artículos uno a uno</p>
        </div>
        <div className="absolute right-4 top-1/2 -translate-y-1/2 text-5xl opacity-20">🃏</div>
      </div>

      {cargando ? (
        <div className="flex justify-center mt-12"><div className="w-8 h-8 border-4 border-violet-500 border-t-transparent rounded-full animate-spin" /></div>
      ) : (
        <>
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">¿Qué artículos repasar?</p>
          <div className="space-y-2 mb-6">
            {[
              { id: 'todos', label: 'Todos los artículos', sub: `${articulos.length} artículos`, icono: '📜' },
              { id: 'pendientes', label: 'Solo pendientes', sub: `${articulos.filter(a => !estudiados[a.numero]).length} sin estudiar`, icono: '⏳' },
              { id: 'estudiados', label: 'Solo estudiados', sub: `${articulos.filter(a => !!estudiados[a.numero]).length} completados`, icono: '✅' },
            ].map(op => (
              <button key={op.id} onClick={() => setFiltro(op.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl border-2 transition-colors ${filtro === op.id ? 'border-violet-500 bg-violet-50' : 'border-gray-200 bg-white'}`}>
                <span className="text-2xl">{op.icono}</span>
                <div className="text-left">
                  <p className={`text-sm font-semibold ${filtro === op.id ? 'text-violet-700' : 'text-gray-700'}`}>{op.label}</p>
                  <p className="text-xs text-gray-400">{op.sub}</p>
                </div>
                {filtro === op.id && <span className="ml-auto text-violet-500">✓</span>}
              </button>
            ))}
          </div>

          {mazo.length === 0 ? (
            <div className="card text-center py-8 text-gray-400">No hay artículos en este filtro</div>
          ) : (
            <button onClick={() => { setIndice(0); setVolteada(false); setCorrectas(0); setCronometro(0); setFase('repaso') }}
              className="w-full bg-violet-600 text-white font-bold py-4 rounded-2xl text-base shadow-lg active:bg-violet-700">
              Empezar repaso · {mazo.length} tarjetas →
            </button>
          )}
        </>
      )}
    </div>
  )

  // ── Fin ──
  if (fase === 'fin') return (
    <div className="max-w-xl mx-auto">
      <div className="card text-center py-8 mb-4">
        <p className="text-5xl mb-3">{correctas / mazo.length >= 0.8 ? '🏆' : correctas / mazo.length >= 0.5 ? '👍' : '📚'}</p>
        <p className="text-2xl font-black text-violet-700 mb-1">{correctas}/{mazo.length}</p>
        <p className="text-sm text-gray-500">artículos que sabías</p>
        <p className="text-xs text-gray-400 mt-2">⏱ {formatTiempo(cronometro)} de repaso</p>
        <div className="w-full bg-gray-100 rounded-full h-2 my-4">
          <div className="bg-violet-500 h-2 rounded-full" style={{ width: `${Math.round(correctas / mazo.length * 100)}%` }} />
        </div>
      </div>
      <button onClick={reiniciar} className="w-full bg-violet-600 text-white font-bold py-4 rounded-2xl">
        Volver a empezar
      </button>
    </div>
  )

  // ── Repaso ──
  return (
    <div className="max-w-xl mx-auto">
      {/* Cabecera */}
      <div className="flex items-center justify-between mb-3">
        <button onClick={reiniciar} className="text-xs text-gray-400">← Salir</button>
        <span className="text-sm font-medium text-gray-500">
          {indice + 1}/{mazo.length} · <span className="text-green-600 font-bold">{correctas} ✓</span>
        </span>
        <span className="text-xs font-bold text-violet-500 tabular-nums">{formatTiempo(cronometro)}</span>
      </div>

      {/* Barra de progreso */}
      <div className="w-full bg-gray-100 rounded-full h-1.5 mb-5">
        <div className="bg-violet-500 h-1.5 rounded-full transition-all" style={{ width: `${progreso}%` }} />
      </div>

      {/* Tarjeta */}
      <div onClick={() => setVolteada(v => !v)}
        className={`rounded-2xl border-2 shadow-md p-6 cursor-pointer min-h-48 flex flex-col justify-center transition-all ${
          volteada ? 'bg-violet-50 border-violet-300' : 'bg-white border-gray-200 active:border-violet-300'
        }`}>
        {!volteada ? (
          <div className="text-center">
            <p className="text-5xl font-black text-violet-600 mb-2">{actual?.numero}</p>
            {actual?.titulo && <p className="text-base text-gray-600 font-medium">{actual.titulo}</p>}
            {actual?.titulo_titulo && <p className="text-xs text-gray-400 mt-1">{actual.titulo_titulo}</p>}
            <p className="text-xs text-gray-300 mt-6">Toca para ver el contenido</p>
          </div>
        ) : (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <span className="bg-violet-100 text-violet-700 font-bold text-xs px-2 py-1 rounded-lg">Art. {actual?.numero}</span>
              {actual?.titulo && <span className="text-xs text-gray-500">{actual.titulo}</span>}
            </div>
            <p className="text-sm text-gray-700 leading-relaxed">{actual?.contenido?.slice(0, 600)}{actual?.contenido?.length > 600 ? '…' : ''}</p>
            <p className="text-xs text-gray-300 mt-4 text-right">Toca para ocultar</p>
          </div>
        )}
      </div>

      {/* Botones respuesta */}
      {volteada && (
        <div className="flex gap-3 mt-4">
          <button onClick={() => siguiente(false)}
            className="flex-1 py-4 rounded-2xl border-2 border-red-200 bg-red-50 text-red-600 font-bold text-sm active:bg-red-100">
            ✗ No lo sabía
          </button>
          <button onClick={() => siguiente(true)}
            className="flex-1 py-4 rounded-2xl border-2 border-green-200 bg-green-50 text-green-600 font-bold text-sm active:bg-green-100">
            ✓ Lo sabía
          </button>
        </div>
      )}

      {!volteada && (
        <p className="text-center text-xs text-gray-400 mt-4">Toca la tarjeta para ver el artículo</p>
      )}
    </div>
  )
}
