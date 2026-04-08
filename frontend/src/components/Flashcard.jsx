import { useState } from 'react'

/**
 * Flashcard simple: muestra el número de artículo al frente
 * y el contenido al darle la vuelta. Para modo repaso rápido.
 */
export default function Flashcard({ numero, contenido, titulo }) {
  const [volteada, setVolteada] = useState(false)

  return (
    <div
      onClick={() => setVolteada(!volteada)}
      className="cursor-pointer select-none"
      title="Haz clic para ver el contenido"
    >
      <div className={`card transition-all duration-200 min-h-[120px] flex flex-col justify-center ${
        volteada ? 'bg-brand-50 border-brand-200' : 'hover:border-brand-300'
      }`}>
        {!volteada ? (
          <div className="text-center">
            <p className="text-3xl font-bold text-brand-500 mb-1">Art. {numero}</p>
            {titulo && <p className="text-sm text-gray-400">{titulo}</p>}
            <p className="text-xs text-gray-300 mt-3">Toca para ver</p>
          </div>
        ) : (
          <div>
            <p className="text-xs text-brand-400 font-semibold mb-2">Artículo {numero}</p>
            <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-line">{contenido}</p>
            <p className="text-xs text-gray-300 mt-3 text-right">Toca para ocultar</p>
          </div>
        )}
      </div>
    </div>
  )
}
