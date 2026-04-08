import { useEffect, useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import LoginModal from './components/LoginModal'
import InstallPrompt from './components/InstallPrompt'
import Home from './pages/Home'
import Constitucion from './pages/Constitucion'
import Articulo from './pages/Articulo'
import Buscar from './pages/Buscar'
import Cambios from './pages/Cambios'
import Quiz from './pages/Quiz'
import Stats from './pages/Stats'
import Oposiciones from './pages/Oposiciones'
import OposicionTemas from './pages/OposicionTemas'
import TemaDetalle from './pages/TemaDetalle'

export default function App() {
  const [usuario, setUsuario] = useState(null)
  const [cargando, setCargando] = useState(true)

  useEffect(() => {
    // Comprobar si ya hay sesión guardada
    const guardado = localStorage.getItem('usuario')
    if (guardado) {
      try {
        setUsuario(JSON.parse(guardado))
      } catch {
        localStorage.removeItem('usuario')
      }
    }
    setCargando(false)
  }, [])

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
          <Route path="/oposiciones" element={<Oposiciones />} />
          <Route path="/oposiciones/:slug" element={<OposicionTemas />} />
          <Route path="/oposiciones/:slug/temas/:numero" element={<TemaDetalle />} />
        </Routes>
      </Layout>
      <InstallPrompt />
    </>
  )
}
