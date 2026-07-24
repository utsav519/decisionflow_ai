import { env } from '@/config/env'
import { apiClient, mockDelay, unwrap } from '@/services/apiClient'
import { mockDecisionEvaluation } from '@/mocks/decisions'
import type { DecisionEvaluationRequest, DecisionEvaluationResult } from '@/types/decision'

export async function evaluateDecision(payload: DecisionEvaluationRequest) {
  if (env.useMockApi) {
    return mockDelay(mockDecisionEvaluation(payload), 800)
  }
  return unwrap<DecisionEvaluationResult>(apiClient.post('/decisions/evaluate', payload))
}

export async function getDecision(evaluationId: string) {
  if (env.useMockApi) {
    return mockDelay({
      evaluation_id: evaluationId,
      decision: 'APPROVE',
      decision_confidence: 96,
    } as DecisionEvaluationResult)
  }
  return unwrap<DecisionEvaluationResult>(apiClient.get(`/decisions/${evaluationId}`))
}
