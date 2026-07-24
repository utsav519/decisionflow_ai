import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { AxiosError, type AxiosResponse, type InternalAxiosRequestConfig } from 'axios'
import MockAdapter from 'axios-mock-adapter'
import type { ApiFailure, ApiSuccess } from '@/types/api'
import { apiClient, mockDelay, normalizeError, unwrap } from '@/services/apiClient'

function axiosFailure(data: ApiFailure, status = 400): AxiosError<ApiFailure> {
  const error = new AxiosError('Request failed', undefined, undefined, undefined, {
    status,
    data,
    statusText: 'Bad Request',
    headers: {},
    config: {} as InternalAxiosRequestConfig,
  } as AxiosResponse<ApiFailure>)
  return error
}

describe('apiClient', () => {
  let mock: MockAdapter

  beforeEach(() => {
    mock = new MockAdapter(apiClient)
    vi.spyOn(crypto, 'randomUUID').mockReturnValue('00000000-0000-4000-8000-000000000001')
  })

  afterEach(() => {
    mock.restore()
    vi.restoreAllMocks()
  })

  it('uses configured base URL', () => {
    expect(apiClient.defaults.baseURL).toBeTruthy()
  })

  it('adds correlation and user headers on requests', async () => {
    mock.onGet('/health-check').reply((config) => {
      expect(config.headers?.['X-Correlation-ID']).toMatch(/^cor_/)
      expect(config.headers?.['X-User-ID']).toBeTruthy()
      expect(config.headers?.['X-User-Role']).toBeTruthy()
      return [200, { success: true, data: {}, meta: {}, correlation_id: 'cor_test' }]
    })

    await apiClient.get('/health-check')
  })

  it('unwrap returns data from success envelope', async () => {
    const payload = { items: [1, 2, 3] }
    const envelope: ApiSuccess<typeof payload> = {
      success: true,
      data: payload,
      meta: {},
      correlation_id: 'cor_123',
    }

    const result = await unwrap(Promise.resolve({ data: envelope }))
    expect(result).toEqual(payload)
  })

  it('normalizes API failure responses', () => {
    const error = normalizeError(
      axiosFailure({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid payload',
          details: [{ issue: 'Missing field' }],
        },
        correlation_id: 'cor_fail',
      }),
    )

    expect(error.code).toBe('VALIDATION_ERROR')
    expect(error.message).toBe('Invalid payload')
    expect(error.correlationId).toBe('cor_fail')
    expect(error.status).toBe(400)
  })

  it('normalizes network errors', () => {
    const error = normalizeError(new AxiosError('Network Error'))
    expect(error.code).toBe('NETWORK_ERROR')
    expect(error.message).toBe('Network Error')
  })

  it('normalizes unknown errors', () => {
    const error = normalizeError(new Error('boom'))
    expect(error.code).toBe('UNKNOWN_ERROR')
    expect(error.message).toBe('An unexpected error occurred.')
  })

  it('mockDelay resolves after timeout', async () => {
    vi.useFakeTimers()
    const promise = mockDelay({ ok: true }, 500)
    await vi.advanceTimersByTimeAsync(500)
    await expect(promise).resolves.toEqual({ ok: true })
    vi.useRealTimers()
  })
})
