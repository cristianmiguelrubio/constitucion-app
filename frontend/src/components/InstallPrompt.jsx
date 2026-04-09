import { useEffect, useState } from 'react'

/**
 * Muestra un banner para instalar la PWA en Android/iOS.
 * - Android: usa el evento beforeinstallprompt
 * - iOS: detecta Safari y muestra instrucciones manuales
 */
export default function InstallPrompt() {
  const [promptEvt, setPromptEvt] = useState(null)
  const [mostrarIOS, setMostrarIOS] = useState(false)
  const [oculto, setOculto] = useState(false)

  useEffect(() => {
    // No mostrar si ya está instalada como PWA (standalone) o descartada
    const esStandalone =
      window.matchMedia('(display-mode: standalone)').matches ||
      window.navigator.standalone === true  // iOS Safari instalada
    if (esStandalone || localStorage.getItem('pwa_descartada')) return

    // Android / Chrome
    const handler = (e) => {
      e.preventDefault()
      setPromptEvt(e)
    }
    window.addEventListener('beforeinstallprompt', handler)

    // iOS Safari — solo mostrar si no está instalada
    const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent)
    const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent)
    if (isIOS && isSafari && !esStandalone) {
      // Esperar 5 segundos antes de mostrar para no interrumpir al entrar
      const t = setTimeout(() => setMostrarIOS(true), 5000)
      return () => { clearTimeout(t); window.removeEventListener('beforeinstallprompt', handler) }
    }

    return () => window.removeEventListener('beforeinstallprompt', handler)
  }, [])

  const instalarAndroid = async () => {
    if (!promptEvt) return
    promptEvt.prompt()
    const { outcome } = await promptEvt.userChoice
    if (outcome === 'accepted') setOculto(true)
    setPromptEvt(null)
  }

  const descartar = () => {
    localStorage.setItem('pwa_descartada', '1')
    setOculto(true)
    setMostrarIOS(false)
    setPromptEvt(null)
  }

  if (oculto || (!promptEvt && !mostrarIOS)) return null

  return (
    <div className="fixed left-4 right-4 z-40 max-w-sm mx-auto" style={{ bottom: 'calc(env(safe-area-inset-bottom, 0px) + 72px)' }}>
      <div className="bg-brand-700 text-white rounded-2xl shadow-2xl p-4">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-3">
            <span className="text-3xl">📱</span>
            <div>
              <p className="font-semibold text-sm">Instala la app</p>
              <p className="text-xs text-white/70 mt-0.5">
                {mostrarIOS
                  ? 'Pulsa el botón compartir ↑ y luego "Añadir a pantalla de inicio"'
                  : 'Accede sin internet, más rápido'}
              </p>
            </div>
          </div>
          <button onClick={descartar} className="text-white/50 hover:text-white text-xl leading-none mt-0.5">×</button>
        </div>

        {promptEvt && (
          <button
            onClick={instalarAndroid}
            className="mt-3 w-full bg-white text-brand-700 font-semibold py-2 rounded-xl text-sm hover:bg-gray-100 transition-colors"
          >
            Instalar ahora
          </button>
        )}
      </div>
    </div>
  )
}
