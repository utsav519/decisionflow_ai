export interface ApiSuccess<T, M = Record<string, unknown>> {
  success: true
  data: T
  meta: M
  correlation_id: string
}

export interface ApiErrorDetail {
  path?: string
  issue: string
  received?: unknown
  allowed_values?: unknown[]
  suggestion?: string
}

export interface ApiErrorBody {
  code: string
  message: string
  details: ApiErrorDetail[]
}

export interface ApiFailure {
  success: false
  error: ApiErrorBody
  correlation_id: string
}

export interface PaginationMeta {
  page: number
  page_size: number
  total_items: number
  total_pages: number
}

export interface FrontendApiError {
  code: string
  message: string
  details: ApiErrorDetail[]
  correlationId?: string
  status?: number
}
