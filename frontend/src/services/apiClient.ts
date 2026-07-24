import axios, { type AxiosError } from 'axios'
import { env } from '@/config/env'
import type { ApiFailure, ApiSuccess, FrontendApiError } from '@/types/api'
import { createCorrelationId } from '@/utils/correlationId'

export const apiClient = axios.create({
  baseURL: env.apiBaseUrl,
  timeout: env.timeoutMs,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
})

apiClient.interceptors.request.use((config) => {
  config.headers['X-Correlation-ID'] = createCorrelationId()
  config.headers['X-User-ID'] = env.defaultUserId
  config.headers['X-User-Role'] = env.defaultUserRole
  return config
})

export function normalizeError(error: unknown): FrontendApiError {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiFailure>
    const data = axiosError.response?.data
    if (data && data.success === false) {
      return {
        code: data.error.code,
        message: data.error.message,
        details: data.error.details,
        correlationId: data.correlation_id,
        status: axiosError.response?.status,
      }
    }
    return {
      code: 'NETWORK_ERROR',
      message: axiosError.message || 'Request failed.',
      details: [],
      status: axiosError.response?.status,
    }
  }
  return {
    code: 'UNKNOWN_ERROR',
    message: 'An unexpected error occurred.',
    details: [],
  }
}

export async function unwrap<T>(promise: Promise<{ data: ApiSuccess<T> }>): Promise<T> {
  const response = await promise
  return response.data.data
}

export function mockDelay<T>(value: T, ms = 600): Promise<T> {
  return new Promise((resolve) => setTimeout(() => resolve(value), ms))
}
