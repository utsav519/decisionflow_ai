import axios, {
  type AxiosError,
  type AxiosInstance,
} from 'axios'

interface BackendErrorPayload {
  error?: {
    code?: string
    message?: string
    details?: unknown
  }
  detail?: string | Array<{
    msg?: string
    loc?: Array<string | number>
  }>
  message?: string
}

const configuredTimeout = Number(
  import.meta.env.VITE_API_TIMEOUT_MS ?? 20000,
)

const timeout = Number.isFinite(configuredTimeout)
  ? configuredTimeout
  : 20000

export const apiClient: AxiosInstance = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL ??
    'http://localhost:8000/api/v1',
  timeout,
  headers: {
    'Content-Type': 'application/json',
  },
})

export function getApiErrorMessage(error: unknown): string {
  if (!axios.isAxiosError(error)) {
    return error instanceof Error
      ? error.message
      : 'An unexpected error occurred.'
  }

  const axiosError = error as AxiosError<BackendErrorPayload>
  const responseData = axiosError.response?.data

  if (responseData?.error?.message) {
    return responseData.error.message
  }

  if (typeof responseData?.detail === 'string') {
    return responseData.detail
  }

  if (Array.isArray(responseData?.detail)) {
    const messages = responseData.detail
      .map((item) => item.msg)
      .filter((message): message is string => Boolean(message))

    if (messages.length > 0) {
      return messages.join(' ')
    }
  }

  if (responseData?.message) {
    return responseData.message
  }

  if (axiosError.code === 'ECONNABORTED') {
    return 'The Decision API request timed out.'
  }

  if (!axiosError.response) {
    return (
      'Unable to reach the Decision API. Confirm that the backend ' +
      'is running on port 8000.'
    )
  }

  return `Decision API request failed with status ${axiosError.response.status}.`
}
