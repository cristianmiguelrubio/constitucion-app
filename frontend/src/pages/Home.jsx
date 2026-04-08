import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

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

function ProgresoCard() {
  const [stats, setStats] = useState({ artEstudiados: 0, artTotal: 169, temasOk: 0 })

  useEffect(() => {
    try {
      const est = JSON.parse(localStorage.getItem('estudiados') || '{}')
      const artEstudiados = Object.values(est).filter(Boolean).length
      // contar temas de policia completados
      const temasOk = Object.keys(localStorage)
        .filter(k => k.startsWith('quiz_ok_policia-local_')).length
      setStats({ artEstudiados, artTotal: 169, temasOk })
    } catch {}
  }, [])

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 mb-5">
      <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">Tu progreso</p>
      <div className="grid grid-cols-2 gap-3">
        <Link to="/constitucion" className="bg-brand-50 rounded-xl p-3 text-center active:bg-brand-100">
          <p className="text-2xl font-bold text-brand-700">{stats.artEstudiados}</p>
          <p className="text-xs text-brand-500 mt-0.5">arts. Constitución</p>
          <div className="mt-2 bg-brand-100 rounded-full h-1.5">
            <div
              className="bg-brand-500 h-1.5 rounded-full transition-all"
              style={{ width: `${Math.round(stats.artEstudiados / stats.artTotal * 100)}%` }}
            />
          </div>
        </Link>
        <Link to="/quiz" className="bg-indigo-50 rounded-xl p-3 text-center active:bg-indigo-100">
          <p className="text-2xl font-bold text-indigo-700">{stats.temasOk}</p>
          <p className="text-xs text-indigo-500 mt-0.5">tests superados</p>
          <div className="mt-2 bg-indigo-100 rounded-full h-1.5">
            <div
              className="bg-indigo-500 h-1.5 rounded-full transition-all"
              style={{ width: `${Math.round(stats.temasOk / 40 * 100)}%` }}
            />
          </div>
        </Link>
      </div>
    </div>
  )
}

export default function Home() {
  const navigate = useNavigate()

  return (
    <div>
      {/* Hero */}
      <div className="bg-gradient-to-br from-brand-800 to-brand-600 rounded-2xl p-5 mb-5 text-white shadow-lg">
        <p className="text-xs font-semibold uppercase tracking-widest text-white/60 mb-1">Plataforma de estudio</p>
        <h1 className="text-2xl font-bold leading-tight mb-1">Oposiciones del Estado</h1>
        <p className="text-sm text-white/70">Prepara tu oposición con temarios actualizados, resúmenes y tests</p>
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

      {/* Acceso rápido al test */}
      <div className="mt-5 grid grid-cols-2 gap-3">
        <Link to="/quiz" className="card flex items-center gap-3 active:bg-gray-50">
          <span className="text-2xl">🧠</span>
          <div>
            <p className="font-semibold text-sm text-gray-700">Test rápido</p>
            <p className="text-xs text-gray-400">Constitución + Policía</p>
          </div>
        </Link>
        <Link to="/cambios" className="card flex items-center gap-3 active:bg-gray-50">
          <span className="text-2xl">🔔</span>
          <div>
            <p className="font-semibold text-sm text-gray-700">Cambios BOE</p>
            <p className="text-xs text-gray-400">Actualizaciones</p>
          </div>
        </Link>
      </div>
    </div>
  )
}
