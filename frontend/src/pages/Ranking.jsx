import { useEffect, useState } from 'react'
import { apiFetch } from '../utils/api'

const MEDALLAS = ['🥇', '🥈', '🥉']

function formatTiempo(segundos) {
  if (segundos < 60) return `${segundos}s`
  if (segundos < 3600) return `${Math.floor(segundos / 60)}min`
  const h = Math.floor(segundos / 3600)
  const m = Math.floor((segundos % 3600) / 60)
  return m > 0 ? `${h}h ${m}min` : `${h}h`
}

export default function Ranking() {
  const [ranking, setRanking] = useState([])
  const [cargando, setCargando] = useState(true)
  const [miNombre, setMiNombre] = useState('')

  useEffect(() => {
    try {
      const u = JSON.parse(localStorage.getItem('usuario') || '{}')
      setMiNombre(u.nombre || u.email?.split('@')[0] || '')
    } catch {}

    apiFetch('/api/ranking')
      .then(r => r.json())
      .then(data => { setRanking(data); setCargando(false) })
      .catch(() => setCargando(false))
  }, [])

  const top3 = ranking.slice(0, 3)
  const resto = ranking.slice(3)

  return (
    <div className="max-w-xl mx-auto">
      {/* Header */}
      <div className="relative rounded-2xl overflow-hidden mb-5 shadow-lg" style={{ height: '120px' }}>
        <div className="absolute inset-0 bg-gradient-to-br from-amber-500 to-orange-600" />
        <div className="absolute inset-0 flex flex-col justify-center px-5">
          <h1 className="text-2xl font-black text-white leading-tight">Ranking</h1>
          <p className="text-xs text-white/70 mt-1">Alumnos con más horas de estudio</p>
        </div>
        <div className="absolute right-4 top-1/2 -translate-y-1/2 text-5xl opacity-20">🏆</div>
      </div>

      {cargando && (
        <div className="flex justify-center mt-12">
          <div className="w-8 h-8 border-4 border-amber-500 border-t-transparent rounded-full animate-spin" />
        </div>
      )}

      {!cargando && ranking.length === 0 && (
        <div className="card text-center py-10">
          <p className="text-3xl mb-2">📊</p>
          <p className="font-medium text-gray-600">Todavía no hay datos</p>
          <p className="text-sm text-gray-400 mt-1">Sé el primero en aparecer estudiando</p>
        </div>
      )}

      {!cargando && ranking.length > 0 && (
        <>
          {/* Top 3 podio */}
          <div className="flex items-end justify-center gap-3 mb-5">
            {[top3[1], top3[0], top3[2]].filter(Boolean).map((r, idx) => {
              const real = idx === 0 ? top3[1] : idx === 1 ? top3[0] : top3[2]
              const altura = idx === 1 ? 'h-28' : 'h-20'
              const pos = idx === 1 ? 1 : idx === 0 ? 2 : 3
              const esYo = real?.nombre === miNombre
              return (
                <div key={pos} className="flex-1 flex flex-col items-center gap-1">
                  <span className="text-2xl">{MEDALLAS[pos - 1]}</span>
                  <p className={`text-xs font-bold text-center truncate w-full px-1 ${esYo ? 'text-amber-600' : 'text-gray-700'}`}>
                    {real?.nombre}{esYo ? ' (tú)' : ''}
                  </p>
                  <p className="text-[10px] text-gray-400">{formatTiempo(real?.segundos)}</p>
                  <div className={`w-full ${altura} rounded-t-xl flex items-end justify-center pb-2 ${
                    pos === 1 ? 'bg-amber-400' : pos === 2 ? 'bg-gray-300' : 'bg-orange-300'
                  }`}>
                    <span className="text-white font-black text-lg">{pos}</span>
                  </div>
                </div>
              )
            })}
          </div>

          {/* Resto */}
          {resto.length > 0 && (
            <div className="space-y-2">
              {resto.map(r => {
                const esYo = r.nombre === miNombre
                return (
                  <div key={r.posicion} className={`flex items-center gap-3 px-4 py-3 rounded-xl ${esYo ? 'bg-amber-50 border border-amber-200' : 'bg-white border border-gray-100'}`}>
                    <span className="text-sm font-bold text-gray-400 w-6 text-center">{r.posicion}</span>
                    <p className={`flex-1 text-sm font-medium ${esYo ? 'text-amber-700' : 'text-gray-700'}`}>
                      {r.nombre}{esYo ? ' (tú)' : ''}
                    </p>
                    <span className="text-xs text-gray-400">{formatTiempo(r.segundos)}</span>
                  </div>
                )
              })}
            </div>
          )}
        </>
      )}
    </div>
  )
}
