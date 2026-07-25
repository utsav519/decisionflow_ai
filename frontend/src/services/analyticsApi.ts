import {
  apiClient,
  unwrap,
} from '@/api/client'
import type {
  AnalyticsDashboard,
  AnalyticsSummary,
  AnalyticsTrends,
  DecisionDistribution,
  TopPolicy,
} from '@/types/analytics'

export function getAnalyticsDashboard(): Promise<AnalyticsDashboard> {
  return unwrap(
    apiClient.get('/analytics/dashboard'),
  )
}

export function getAnalyticsSummary(): Promise<AnalyticsSummary> {
  return unwrap(
    apiClient.get('/analytics/summary'),
  )
}

export function getDecisionDistribution(): Promise<DecisionDistribution> {
  return unwrap(
    apiClient.get('/analytics/decision-distribution'),
  )
}

export function getDecisionTrend(): Promise<AnalyticsTrends> {
  return unwrap(
    apiClient.get('/analytics/decision-trend'),
  )
}

export function getTopPolicies(): Promise<TopPolicy[]> {
  return unwrap(
    apiClient.get('/analytics/top-policies'),
  )
}
