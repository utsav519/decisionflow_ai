import { apiClient } from './client'
import type {
  DecisionDetailResponse,
  DecisionEvaluationRequest,
  DecisionEvaluationResponse,
  StandardResponse,
} from '../types/decision'

export interface DecisionRequestHeaders {
  correlationId?: string
  userId?: string
}

function createHeaders(
  headers?: DecisionRequestHeaders,
): Record<string, string> {
  const result: Record<string, string> = {}

  if (headers?.correlationId) {
    result['X-Correlation-ID'] = headers.correlationId
  }

  if (headers?.userId) {
    result['X-User-ID'] = headers.userId
  }

  return result
}

export async function evaluateDecision(
  request: DecisionEvaluationRequest,
  headers?: DecisionRequestHeaders,
): Promise<StandardResponse<DecisionEvaluationResponse>> {
  const response = await apiClient.post<
    StandardResponse<DecisionEvaluationResponse>
  >(
    '/decisions/evaluate',
    request,
    {
      headers: createHeaders(headers),
    },
  )

  return response.data
}

export async function getDecision(
  evaluationId: string,
  headers?: DecisionRequestHeaders,
): Promise<StandardResponse<DecisionDetailResponse>> {
  const encodedEvaluationId = encodeURIComponent(evaluationId)

  const response = await apiClient.get<
    StandardResponse<DecisionDetailResponse>
  >(
    `/decisions/${encodedEvaluationId}`,
    {
      headers: createHeaders(headers),
    },
  )

  return response.data
}
