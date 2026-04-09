import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { apiFetch } from '../utils/api'

const CATEGORIAS = [
  {
    slug: 'constitucion',
    nombre: 'Constitución Española',
    descripcion: 'Texto oficial actualizado desde el BOE',
    link: '/constitucion',
    gradient: 'from-[#1e3a5f] to-[#2d5a8e]',
    icono: '📜',
    badge: null,
  },
  {
    slug: 'policia-local',
    nombre: 'Policía Local',
    descripcion: '40 temas · Test por sección · Resúmenes',
    link: '/oposiciones/policia-local',
    gradient: 'from-[#1a237e] to-[#283593]',
    icono: '👮',
    badge: 'Disponible',
  },
  {
    slug: 'policia-nacional',
    nombre: 'Policía Nacional',
    descripcion: 'Temario completo en preparación',
    link: null,
    gradient: 'from-[#4a148c] to-[#6a1b9a]',
    icono: '🛡️',
    badge: 'Próximamente',
  },
  {
    slug: 'guardia-civil',
    nombre: 'Guardia Civil',
    descripcion: 'Temario completo en preparación',
    link: null,
    gradient: 'from-[#1b5e20] to-[#2e7d32]',
    icono: '⭐',
    badge: 'Próximamente',
  },
  {
    slug: 'bomberos',
    nombre: 'Bomberos',
    descripcion: 'Temario completo en preparación',
    link: null,
    gradient: 'from-[#b71c1c] to-[#c62828]',
    icono: '🚒',
    badge: 'Próximamente',
  },
]

const CURSOS = [
  {
    slug: 'constitucion',
    nombre: 'Constitución Española',
    icono: '📜',
    link: '/constitucion',
    color: { bar: 'bg-brand-500', bg: 'bg-brand-50', text: 'text-brand-700', sub: 'text-brand-400' },
    getProgreso: () => {
      try {
        const est = JSON.parse(localStorage.getItem('estudiados') || '{}')
        const hecho = Object.values(est).filter(Boolean).length
        return { hecho, total: 169, label: 'artículos leídos' }
      } catch { return { hecho: 0, total: 169, label: 'artículos leídos' } }
    },
  },
  {
    slug: 'policia-local',
    nombre: 'Policía Local',
    icono: '👮',
    link: '/oposiciones/policia-local',
    color: { bar: 'bg-indigo-500', bg: 'bg-indigo-50', text: 'text-indigo-700', sub: 'text-indigo-400' },
    getProgreso: () => {
      const hecho = Object.keys(localStorage).filter(k => k.startsWith('quiz_ok_policia-local_')).length
      return { hecho, total: 40, label: 'temas superados' }
    },
  },
]

function ProgresoCard() {
  const [progresos, setProgresos] = useState([])
  const [racha, setRacha] = useState(null)

  useEffect(() => {
    setProgresos(CURSOS.map(c => ({ ...c, progreso: c.getProgreso() })))
    apiFetch('/api/racha', { method: 'POST' })
      .then(r => r.json())
      .then(setRacha)
      .catch(() => {})
  }, [])

  // Solo mostrar cursos con algún progreso, o todos si ninguno tiene
  const activos = progresos.filter(c => c.progreso?.hecho > 0)
  const mostrar = activos.length > 0 ? activos : progresos

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 mb-5">
      <div className="flex items-center justify-between mb-3">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">Mi progreso</p>
        {racha && racha.racha > 0 && (
          <div className="flex items-center gap-1 bg-orange-50 border border-orange-200 rounded-full px-2.5 py-1">
            <span className="text-sm">🔥</span>
            <span className="text-xs font-bold text-orange-600">{racha.racha} {racha.racha === 1 ? 'día' : 'días'}</span>
          </div>
        )}
      </div>
      <div className="space-y-3">
        {mostrar.map(c => {
          const { hecho, total, label } = c.progreso || { hecho: 0, total: 1, label: '' }
          const pct = Math.round(hecho / total * 100)
          return (
            <Link key={c.slug} to={c.link} className={`flex items-center gap-3 ${c.color.bg} rounded-xl p-3 active:opacity-80`}>
              <span className="text-2xl shrink-0">{c.icono}</span>
              <div className="flex-1 min-w-0">
                <div className="flex justify-between items-baseline mb-1">
                  <p className={`text-sm font-semibold ${c.color.text} truncate`}>{c.nombre}</p>
                  <span className={`text-xs font-bold ${c.color.text} shrink-0 ml-2`}>{pct}%</span>
                </div>
                <div className="bg-white/60 rounded-full h-1.5">
                  <div className={`${c.color.bar} h-1.5 rounded-full transition-all`} style={{ width: `${pct}%` }} />
                </div>
                <p className={`text-[11px] ${c.color.sub} mt-1`}>{hecho}/{total} {label}</p>
              </div>
              <span className={`${c.color.sub} text-lg shrink-0`}>›</span>
            </Link>
          )
        })}
      </div>
    </div>
  )
}


function FormSugerencia() {
  const [texto, setTexto] = useState('')
  const [estado, setEstado] = useState(null) // null | 'ok' | 'error'
  const [enviando, setEnviando] = useState(false)

  const enviar = async (e) => {
    e.preventDefault()
    if (texto.trim().length < 5) return
    setEnviando(true)
    try {
      const r = await apiFetch('/api/sugerencias', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ texto }) })
      if (r.status === 401) { setEstado('error'); return }
      setEstado(r.ok ? 'ok' : 'error')
      if (r.ok) setTexto('')
    } catch { setEstado('error') }
    finally { setEnviando(false) }
  }

  if (estado === 'ok') return (
    <div className="text-center py-4">
      <p className="text-2xl mb-1">✅</p>
      <p className="text-sm font-medium text-green-600">¡Sugerencia enviada! Gracias.</p>
      <button onClick={() => setEstado(null)} className="text-xs text-gray-400 mt-2">Enviar otra</button>
    </div>
  )

  return (
    <form onSubmit={enviar} className="mt-4 border-t border-gray-100 pt-4">
      <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Sugerencias para la app</p>
      <textarea
        value={texto}
        onChange={e => setTexto(e.target.value)}
        placeholder="¿Qué mejorarías o añadirías?"
        rows={3}
        className="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm text-gray-700 resize-none focus:outline-none focus:ring-2 focus:ring-brand-300"
      />
      {estado === 'error' && <p className="text-xs text-red-500 mt-1">Error al enviar. Recarga la página e inténtalo de nuevo.</p>}
      <button
        type="submit"
        disabled={texto.trim().length < 5 || enviando}
        className="mt-2 w-full bg-brand-700 text-white text-sm font-semibold py-2.5 rounded-xl disabled:opacity-40"
      >
        {enviando ? 'Enviando...' : 'Enviar sugerencia'}
      </button>
    </form>
  )
}

export default function Home() {
  const navigate = useNavigate()

  return (
    <div>
      {/* Hero imagen */}
      <div className="relative rounded-2xl overflow-hidden mb-5 shadow-xl" style={{ height: '200px' }}>
        <img
          src="/hero.jpg"
          alt="Oposiciones del Estado"
          className="w-full h-full object-cover object-center"
        />
        {/* Overlay degradado */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent" />
        {/* Texto encima */}
        <div className="absolute bottom-0 left-0 right-0 p-4">
          <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-white/60 mb-0.5">Plataforma de estudio</p>
          <h1 className="text-2xl font-black text-white leading-tight drop-shadow-lg">Oposiciones del Estado</h1>
          <p className="text-xs text-white/70 mt-0.5">Temarios actualizados · Tests · Resúmenes</p>
        </div>
      </div>

      {/* Progreso */}
      <ProgresoCard />

      {/* Acceso rápido */}
      <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3 px-1">Categorías</p>
      <div className="space-y-3">
        {CATEGORIAS.map(cat => (
          <div
            key={cat.slug}
            onClick={() => cat.link && navigate(cat.link)}
            className={`bg-gradient-to-r ${cat.gradient} rounded-2xl p-4 flex items-center gap-4 shadow-md ${cat.link ? 'active:opacity-90 cursor-pointer' : 'opacity-70'}`}
          >
            <span className="text-4xl shrink-0">{cat.icono}</span>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <p className="font-bold text-white text-base leading-tight">{cat.nombre}</p>
                {cat.badge && (
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full shrink-0 ${
                    cat.badge === 'Disponible'
                      ? 'bg-green-400 text-green-900'
                      : 'bg-white/20 text-white/80'
                  }`}>
                    {cat.badge}
                  </span>
                )}
              </div>
              <p className="text-white/60 text-xs mt-0.5">{cat.descripcion}</p>
            </div>
            {cat.link && <span className="text-white/40 text-lg shrink-0">›</span>}
          </div>
        ))}
      </div>

      {/* Contacto */}
      <div className="mt-5 bg-white rounded-2xl border border-gray-100 shadow-sm p-4">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">Contacto</p>
        <div className="flex gap-3 mb-1">
          <a href="tel:611945719" className="flex-1 flex items-center justify-center gap-2 bg-brand-50 rounded-xl py-3 active:bg-brand-100">
            <span className="text-xl">📞</span>
            <div className="text-left">
              <p className="text-sm font-semibold text-brand-700">Llamar</p>
              <p className="text-xs text-brand-400">611 945 719</p>
            </div>
          </a>
          <a href="https://wa.me/34611945719" target="_blank" rel="noreferrer" className="flex-1 flex items-center justify-center gap-2 bg-green-50 rounded-xl py-3 active:bg-green-100">
            <span className="text-xl">💬</span>
            <div className="text-left">
              <p className="text-sm font-semibold text-green-700">WhatsApp</p>
              <p className="text-xs text-green-400">611 945 719</p>
            </div>
          </a>
        </div>
        <FormSugerencia />
      </div>
    </div>
  )
}
