import { useEffect } from 'react'
import { apiFetch } from '../utils/api'

export function usePushNotifications(usuario) {
  useEffect(() => {
    if (!usuario) return
    if (!('serviceWorker' in navigator) || !('PushManager' in window)) return
    if (localStorage.getItem('push_subscribed')) return

    const suscribir = async () => {
      try {
        const r = await apiFetch('/api/push/vapid-key')
        const { publicKey } = await r.json()
        if (!publicKey) return

        const perm = await Notification.requestPermission()
        if (perm !== 'granted') return

        const reg = await navigator.serviceWorker.ready
        const sub = await reg.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: urlBase64ToUint8Array(publicKey),
        })

        const subJson = sub.toJSON()
        await apiFetch('/api/push/subscribe', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            endpoint: subJson.endpoint,
            p256dh: subJson.keys.p256dh,
            auth: subJson.keys.auth,
          }),
        })
        localStorage.setItem('push_subscribed', '1')
      } catch (e) {
        console.warn('Push subscribe error:', e)
      }
    }

    // Pedir permiso después de 10 segundos para no interrumpir el onboarding
    const timer = setTimeout(suscribir, 10000)
    return () => clearTimeout(timer)
  }, [usuario])
}

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4)
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/')
  const rawData = window.atob(base64)
  return Uint8Array.from([...rawData].map(c => c.charCodeAt(0)))
}
