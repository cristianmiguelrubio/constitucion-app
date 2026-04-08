import { useEffect, useState } from 'react'
import { useSearchParams, Link } from 'react-router-dom'

export default function Buscar() {
  const [searchParams] = useSearchParams()
  const q = searchParams.get('q') || ''
  const [resultados, setResultados] = useState([])
  const [cargando, setCargando] = useState(false)
  const [buscado, setBuscado] = useState('')

  useEffect(() => {
    if (q.length < 2) return
    setCargando(true)
    fetch(`/api/buscar?q=${encodeURIComponent(q)}`)
      .then(r => r.json())
      .then(data => { setResultados(data); setBuscado(q); setCargando(false) })
      .catch(() => setCargando(false))
  }, [q])

  const resaltar = (texto, termino) => {
    if (!termino) return texto
    const regex = new RegExp(`(${termino.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
    return texto.replace(regex, '<mark class="bg-yellow-200 rounded px-0.5">$1</mark>')
  }

  return (
    <div>
      <h1 className="text-xl font-bold text-brand-700 mb-1">Resultados de búsqueda</h1>
      {buscado && (
        <p className="text-sm text-gray-500 mb-5">
          {cargando ? 'Buscando...' : `${resultados.length} resultado${resultados.length !== 1 ? 's' : ''} para `}
          {!cargando && <span className="font-medium text-gray-700">"{buscado}"</span>}
        </p>
      )}

      {!q && (
        <div className="card text-center text-gray-400 mt-16">
          Escribe algo en el buscador para empezar
        </div>
      )}

      {resultados.length === 0 && !cargando && q && (
        <div className="card text-center mt-10">
          <p className="text-gray-500">No se encontraron artículos para "{q}"</p>
          <Link to="/" className="text-brand-500 text-sm mt-2 inline-block">← Ver índice completo</Link>
        </div>
      )}

      <div className="space-y-3">
        {resultados.map(art => (
          <Link
            key={art.numero}
            to={`/articulo/${art.numero}`}
            className="card block hover:shadow-md hover:border-brand-100 transition-all"
          >
            <div className="flex items-start gap-3">
              <span className="shrink-0 bg-brand-100 text-brand-700 font-bold text-sm px-2 py-1 rounded-lg">
                Art. {art.numero}
              </span>
              <div className="min-w-0">
                {art.titulo && (
                  <p
                    className="font-medium text-gray-800 text-sm"
                    dangerouslySetInnerHTML={{ __html: resaltar(art.titulo, q) }}
                  />
                )}
                {art.titulo_titulo && (
                  <p className="text-xs text-gray-400 mt-0.5">{art.titulo_titulo}</p>
                )}
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}
