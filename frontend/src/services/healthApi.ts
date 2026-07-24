import axios from 'axios'
import { env } from '@/config/env'
import { mockDelay } from '@/services/apiClient'

export type HealthStatus = 'healthy' | 'degraded' | 'unavailable'

export async function getHealth(): Promise<{ status: HealthStatus; message: string }> {
  if (env.useMockApi) {
    return mockDelay({ status: 'healthy', message: 'Mock mode — backend not required.' }, 200)
  }
  try {
    const { data } = await axios.get(`${env.backendBaseUrl}/health`, { timeout: 5000 })
    return { status: 'healthy', message: data?.message ?? 'Backend is healthy.' }
  } catch {
    return { status: 'unavailable', message: 'Backend is unavailable.' }
  }
}
