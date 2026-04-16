import { useState, useEffect, createContext, useContext } from 'react'
import { apiFetch } from '../utils/api'

export const PlanContext = createContext(null)

export function usePlan() {
  return useContext(PlanContext)
}

export function usePlanData() {
  const [plan, setPlan] = useState(null)
  const [cargando, setCargando] = useState(true)

  const recargar = () => {
    setCargando(true)
    apiFetch('/api/plan')
      .then(r => r.json())
      .then(data => { setPlan(data); setCargando(false) })
      .catch(() => setCargando(false))
  }

  useEffect(() => { recargar() }, [])

  return { plan, cargando, recargar }
}
