import { env } from '@/config/env'
import { apiClient, mockDelay, unwrap } from '@/services/apiClient'
import {
  mockAnalyticsSummary,
  mockDecisionDistribution,
  mockDecisionTrend,
  mockTopPolicies,
} from '@/mocks/analytics'

export async function getSummary() {
  if (env.useMockApi) return mockDelay(mockAnalyticsSummary)
  return unwrap(apiClient.get('/analytics/summary'))
}

export async function getDecisionDistribution() {
  if (env.useMockApi) return mockDelay(mockDecisionDistribution)
  return unwrap(apiClient.get('/analytics/decision-distribution'))
}

export async function getDecisionTrend() {
  if (env.useMockApi) return mockDelay(mockDecisionTrend)
  return unwrap(apiClient.get('/analytics/decision-trend'))
}

export async function getTopPolicies() {
  if (env.useMockApi) return mockDelay(mockTopPolicies)
  return unwrap(apiClient.get('/analytics/top-policies'))
}
