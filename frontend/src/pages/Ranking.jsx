import { useEffect, useState } from 'react'
import { apiFetch } from '../utils/api'

const MEDALLAS = ['🥇', '🥈', '🥉']
const PERIODOS = [
  { id: 'hoy',    label: 'Hoy',    icono: '📅' },
  { id: 'semana', label: 'Semana', icono: '📆' },
  { id: 'total',  label: 'Total',  icono: '🏆' },
]

function formatTiempo(segundos) {
  if (!segundos || segundos < 60) return segundos ? `${segundos}s` : '—'
  if (segundos < 3600) return `${Math.floor(segundos / 60)}min`
  const h = Math.floor(segundos / 3600)
  const m = Math.floor((segundos % 3600) / 60)
  return m > 0 ? `${h}h ${m}min` : `${h}h`
}

export default function Ranking() {
  const [periodo, setPeriodo] = useState('hoy')
  const [ranking, setRanking] = useState([])
  const [cargando, setCargando] = useState(true)
  const [miNombre, setMiNombre] = useState('')

  useEffect(() => {
    try {
      const u = JSON.parse(localStorage.getItem('usuario') || '{}')
      setMiNombre(u.nombre || u.email?.split('@')[0] || '')
    } catch {}
  }, [])

  useEffect(() => {
    setCargando(true)
    apiFetch(`/api/ranking?periodo=${periodo}`)
      .then(r => r.json())
      .then(data => { setRanking(data); setCargando(false) })
      .catch(() => setCargando(false))
  }, [periodo])

  const top3 = ranking.slice(0, 3)
  const resto = ranking.slice(3)

  const miPosicion = miNombre ? ranking.findIndex(r => r.nombre === miNombre) : -1

  return (
    <div className="max-w-xl mx-auto">
      {/* Header */}
      <div className="relative rounded-2xl overflow-hidden mb-5 shadow-lg" style={{ height: '110px' }}>
        <div className="absolute inset-0 bg-gradient-to-br from-amber-500 to-orange-600" />
        <div className="absolute inset-0 flex flex-col justify-center px-5">
          <h1 className="text-2xl font-black text-white leading-tight">Ranking</h1>
          <p className="text-xs text-white/70 mt-1">¿Quién estudia más?</p>
        </div>
        <div className="absolute right-4 top-1/2 -translate-y-1/2 text-5xl opacity-20">🏆</div>
      </div>

      {/* Tabs periodo */}
      <div className="flex rounded-xl overflow-hidden border border-gray-200 mb-5">
        {PERIODOS.map(p => (
          <button
            key={p.id}
            onClick={() => setPeriodo(p.id)}
            className={`flex-1 py-2.5 text-sm font-semibold transition-colors ${
              periodo === p.id ? 'bg-amber-500 text-white' : 'text-gray-500 active:bg-gray-50'
            }`}
          >
            {p.icono} {p.label}
          </button>
        ))}
      </div>

      {/* Mi posición si no estoy en top visible */}
      {!cargando && miPosicion >= 3 && (
        <div className="bg-amber-50 border border-amber-200 rounded-xl px-4 py-2.5 mb-4 flex items-center gap-2">
          <span className="text-sm font-bold text-amber-700">#{miPosicion + 1}</span>
          <span className="text-sm text-amber-600 flex-1">Tu posición · {formatTiempo(ranking[miPosicion]?.segundos)}</span>
        </div>
      )}

      {cargando && (
        <div className="flex justify-center mt-12">
          <div className="w-8 h-8 border-4 border-amber-500 border-t-transparent rounded-full animate-spin" />
        </div>
      )}

      {!cargando && ranking.length === 0 && (
        <div className="card text-center py-10">
          <p className="text-3xl mb-2">📊</p>
          <p className="font-medium text-gray-600">
            {periodo === 'hoy' ? 'Nadie ha estudiado hoy todavía' :
             periodo === 'semana' ? 'Sin datos esta semana' :
             'Todavía no hay datos'}
          </p>
          <p className="text-sm text-gray-400 mt-1">¡Sé el primero en aparecer!</p>
        </div>
      )}

      {!cargando && ranking.length > 0 && (
        <>
          {/* Podio — orden visual: 2º, 1º, 3º */}
          <div className="flex items-end justify-center gap-3 mb-5">
            {([top3[1], top3[0], top3[2]]).map((r, idx) => {
              if (!r) return <div key={idx} className="flex-1" />
              const pos = idx === 0 ? 2 : idx === 1 ? 1 : 3
              const altura = pos === 1 ? 'h-28' : 'h-20'
              const esYo = r.nombre === miNombre
              return (
                <div key={pos} className="flex-1 flex flex-col items-center gap-1">
                  <span className="text-2xl">{MEDALLAS[pos - 1]}</span>
                  <p className={`text-xs font-bold text-center truncate w-full px-1 ${esYo ? 'text-amber-600' : 'text-gray-700'}`}>
                    {r.nombre}{esYo ? ' (tú)' : ''}
                  </p>
                  <p className="text-[10px] text-gray-400">{formatTiempo(r.segundos)}</p>
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
                  <div key={r.posicion} className={`flex items-center gap-3 px-4 py-3 rounded-xl border ${
                    esYo ? 'bg-amber-50 border-amber-200' : 'bg-white border-gray-100'
                  }`}>
                    <span className="text-sm font-bold text-gray-400 w-6 text-center">{r.posicion}</span>
                    <p className={`flex-1 text-sm font-medium truncate ${esYo ? 'text-amber-700' : 'text-gray-700'}`}>
                      {r.nombre}{esYo ? ' (tú)' : ''}
                    </p>
                    <span className="text-xs font-medium text-gray-500">{formatTiempo(r.segundos)}</span>
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
