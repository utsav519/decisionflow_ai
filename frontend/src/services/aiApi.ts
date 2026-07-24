import { env } from '@/config/env'
import { apiClient, mockDelay, unwrap } from '@/services/apiClient'
import { mockPolicyGeneration } from '@/mocks/aiPolicy'
import type { GeneratedPolicyResult } from '@/types/policy'

export interface GeneratePolicyPayload {
  policy_text: string
  domain?: string
  preferred_decision?: string
  preferred_priority?: number
  generate_test_cases?: boolean
}

export async function generatePolicy(payload: GeneratePolicyPayload) {
  if (env.useMockApi) {
    return mockDelay(mockPolicyGeneration(payload.policy_text))
  }
  return unwrap<GeneratedPolicyResult>(apiClient.post('/ai/policies/generate', payload))
}

export async function getFields() {
  if (env.useMockApi) {
    const { TELECOM_FIELDS } = await import('@/utils/constants')
    return mockDelay(TELECOM_FIELDS)
  }
  return unwrap(apiClient.get('/config/fields'))
}

export async function getOperators() {
  if (env.useMockApi) {
    return mockDelay([
      'equals',
      'not_equals',
      'greater_than',
      'greater_than_or_equal',
      'less_than',
      'less_than_or_equal',
      'contains',
      'in',
      'not_in',
      'is_empty',
      'is_not_empty',
    ])
  }
  return unwrap(apiClient.get('/config/operators'))
}
