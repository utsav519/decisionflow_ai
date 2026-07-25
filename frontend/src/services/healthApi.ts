import axios from 'axios'

import { env } from '@/config/env'

export type HealthStatus =
  | 'healthy'
  | 'degraded'
  | 'unavailable'

export interface HealthResult {
  status: HealthStatus
  message: string
}

interface BackendHealthResponse {
  status?: string
  service?: string
  app?: string
}

export async function getHealth(): Promise<HealthResult> {
  try {
    const response = await axios.get<BackendHealthResponse>(
      `${env.backendBaseUrl}/health`,
      {
        timeout: 5000,
      },
    )

    const isHealthy =
      response.data.status === 'healthy'

    return {
      status: isHealthy ? 'healthy' : 'degraded',
      message: isHealthy
        ? 'DecisionFlow backend is healthy.'
        : 'DecisionFlow backend reported a degraded state.',
    }
  } catch {
    return {
      status: 'unavailable',
      message:
        'DecisionFlow backend is unavailable.',
    }
  }
}
