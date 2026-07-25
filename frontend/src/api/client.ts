import axios, {
  type AxiosError,
  type AxiosInstance,
  type AxiosResponse,
} from 'axios'

import { env } from '@/config/env'
import type {
  ApiFailure,
  ApiSuccess,
  FrontendApiError,
} from '@/types/api'
import {
  createCorrelationId,
} from '@/utils/correlationId'

interface FastApiValidationDetail {
  msg?: string
  loc?: Array<string | number>
}

interface BackendErrorPayload {
  success?: false
  error?: {
    code?: string
    message?: string
    details?: unknown
  }
  detail?: string | FastApiValidationDetail[]
  message?: string
  correlation_id?: string
}

export const apiClient: AxiosInstance = axios.create({
  baseURL: env.apiBaseUrl,
  timeout: env.timeoutMs,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
})

apiClient.interceptors.request.use((config) => {
  if (!config.headers.has('X-Correlation-ID')) {
    config.headers.set(
      'X-Correlation-ID',
      createCorrelationId(),
    )
  }

  if (!config.headers.has('X-User-ID')) {
    config.headers.set(
      'X-User-ID',
      env.defaultUserId,
    )
  }

  if (!config.headers.has('X-User-Role')) {
    config.headers.set(
      'X-User-Role',
      env.defaultUserRole,
    )
  }

  return config
})

export function normalizeApiError(
  error: unknown,
): FrontendApiError {
  if (!axios.isAxiosError(error)) {
    return {
      code: 'UNKNOWN_ERROR',
      message:
        error instanceof Error
          ? error.message
          : 'An unexpected error occurred.',
    }
  }

  const axiosError =
    error as AxiosError<BackendErrorPayload>

  const responseData = axiosError.response?.data

  if (
    responseData?.success === false &&
    responseData.error?.message
  ) {
    return {
      code:
        responseData.error.code ??
        'API_ERROR',
      message: responseData.error.message,
      details: responseData.error.details,
      correlationId:
        responseData.correlation_id,
      status: axiosError.response?.status,
    }
  }

  if (typeof responseData?.detail === 'string') {
    return {
      code: 'VALIDATION_ERROR',
      message: responseData.detail,
      status: axiosError.response?.status,
    }
  }

  if (Array.isArray(responseData?.detail)) {
    const messages = responseData.detail
      .map((item) => {
        const location = item.loc?.join('.')
        return location
          ? `${location}: ${item.msg ?? 'Invalid value'}`
          : item.msg
      })
      .filter(
        (message): message is string =>
          Boolean(message),
      )

    return {
      code: 'VALIDATION_ERROR',
      message:
        messages.join(' ') ||
        'The request could not be validated.',
      details: responseData.detail,
      status: axiosError.response?.status,
    }
  }

  if (responseData?.message) {
    return {
      code: 'API_ERROR',
      message: responseData.message,
      status: axiosError.response?.status,
    }
  }

  if (axiosError.code === 'ECONNABORTED') {
    return {
      code: 'REQUEST_TIMEOUT',
      message: 'The API request timed out.',
    }
  }

  if (!axiosError.response) {
    return {
      code: 'NETWORK_ERROR',
      message:
        'Unable to reach the DecisionFlow API. ' +
        'Confirm that the backend is running on port 8000.',
    }
  }

  return {
    code: 'API_ERROR',
    message:
      `The API request failed with status ` +
      `${axiosError.response.status}.`,
    status: axiosError.response.status,
  }
}

export function getApiErrorMessage(
  error: unknown,
): string {
  return normalizeApiError(error).message
}

export async function unwrap<
  T,
  M = Record<string, unknown>,
>(
  request: Promise<
    AxiosResponse<ApiSuccess<T, M>>
  >,
): Promise<T> {
  const response = await request
  return response.data.data
}

export function isApiFailure(
  value: unknown,
): value is ApiFailure {
  return (
    typeof value === 'object' &&
    value !== null &&
    'success' in value &&
    value.success === false
  )
}
