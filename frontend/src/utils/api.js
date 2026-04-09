/**
 * Wrapper de fetch que añade automáticamente el token JWT de localStorage.
 * Si la respuesta es 401, limpia la sesión y recarga para forzar login.
 */
export function apiFetch(url, options = {}) {
  const token = localStorage.getItem('token')
  const headers = {
    ...(options.headers || {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }
  return fetch(url, { ...options, headers }).then(res => {
    if (res.status === 401 && token) {
      // Solo limpiar y recargar si había token (sesión expirada)
      localStorage.removeItem('token')
      localStorage.removeItem('usuario')
      window.location.reload()
    }
    return res
  })
}
