import { useEffect, useState, useRef } from 'react'
import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import { apiFetch } from './utils/api'
import LoginModal from './components/LoginModal'
import InstallPrompt from './components/InstallPrompt'
import Home from './pages/Home'
import Constitucion from './pages/Constitucion'
import Articulo from './pages/Articulo'
import Buscar from './pages/Buscar'
import Cambios from './pages/Cambios'
import Quiz from './pages/Quiz'
import Stats from './pages/Stats'
import Ranking from './pages/Ranking'
import Admin from './pages/Admin'
import Oposiciones from './pages/Oposiciones'
import OposicionTemas from './pages/OposicionTemas'
import TemaDetalle from './pages/TemaDetalle'
import Flashcards from './pages/Flashcards'

function useTiempoGlobal(usuario) {
  const inicio = useRef(Date.now())
  useEffect(() => {
    if (!usuario) return
    const enviar = (seg) => {
      if (seg > 5) apiFetch('/api/tiempo', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ segundos: seg }) }).catch(() => {})
    }
    const onUnload = () => enviar(Math.floor((Date.now() - inicio.current) / 1000))
    window.addEventListener('beforeunload', onUnload)
    const id = setInterval(() => {
      enviar(60)
      inicio.current = Date.now()
    }, 60000)
    return () => { window.removeEventListener('beforeunload', onUnload); clearInterval(id) }
  }, [usuario])
}

export default function App() {
  const [usuario, setUsuario] = useState(null)
  const [cargando, setCargando] = useState(true)

  useEffect(() => {
    const guardado = localStorage.getItem('usuario')
    if (guardado) {
      try { setUsuario(JSON.parse(guardado)) }
      catch { localStorage.removeItem('usuario') }
    }
    setCargando(false)
  }, [])

  useTiempoGlobal(usuario)

  const handleLogin = (u) => {
    setUsuario(u)
  }

  if (cargando) return null

  return (
    <>
      {!usuario && <LoginModal onLogin={handleLogin} />}
      <Layout usuario={usuario} onLogout={() => { localStorage.removeItem('usuario'); setUsuario(null) }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/constitucion" element={<Constitucion />} />
          <Route path="/articulo/:numero" element={<Articulo usuario={usuario} />} />
          <Route path="/buscar" element={<Buscar />} />
          <Route path="/cambios" element={<Cambios />} />
          <Route path="/quiz" element={<Quiz />} />
          <Route path="/stats" element={<Stats />} />
          <Route path="/ranking" element={<Ranking />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/oposiciones" element={<Oposiciones />} />
          <Route path="/oposiciones/:slug" element={<OposicionTemas />} />
          <Route path="/oposiciones/:slug/temas/:numero" element={<TemaDetalle />} />
          <Route path="/flashcards" element={<Flashcards />} />
        </Routes>
      </Layout>
      <InstallPrompt />
    </>
  )
}
