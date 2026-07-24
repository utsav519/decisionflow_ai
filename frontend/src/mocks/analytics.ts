import type {
  AnalyticsSummary,
  DecisionDistributionItem,
  DecisionTrendItem,
  TopPolicyItem,
} from '@/types/analytics'

export const mockAnalyticsSummary: AnalyticsSummary = {
  policies: {
    total: 6,
    active: 5,
    draft: 1,
    pending_approval: 0,
    disabled: 0,
    ai_generated: 1,
  },
  decisions: {
    total: 47,
    approve: 28,
    reject: 12,
    manual_review: 7,
    approval_rate: 0.596,
    rejection_rate: 0.255,
    manual_review_rate: 0.149,
  },
  performance: {
    average_decision_confidence: 87,
    average_engine_latency_ms: 42,
    average_total_latency_ms: 315,
    p95_total_latency_ms: 480,
  },
  quality: {
    validation_errors: 2,
    conflicts_detected: 1,
    ai_fallback_count: 3,
  },
}

export const mockDecisionDistribution: DecisionDistributionItem[] = [
  { decision: 'APPROVE', count: 28 },
  { decision: 'REJECT', count: 12 },
  { decision: 'MANUAL_REVIEW', count: 7 },
]

export const mockDecisionTrend: DecisionTrendItem[] = [
  { date: '2026-07-18', approve: 4, reject: 2, manual_review: 1 },
  { date: '2026-07-19', approve: 5, reject: 1, manual_review: 2 },
  { date: '2026-07-20', approve: 6, reject: 3, manual_review: 0 },
  { date: '2026-07-21', approve: 3, reject: 2, manual_review: 1 },
  { date: '2026-07-22', approve: 4, reject: 2, manual_review: 1 },
  { date: '2026-07-23', approve: 3, reject: 2, manual_review: 1 },
  { date: '2026-07-24', approve: 3, reject: 0, manual_review: 1 },
]

export const mockTopPolicies: TopPolicyItem[] = [
  { policy_id: 'pol_std_001', policy_name: 'Standard upgrade approval', trigger_count: 22 },
  { policy_id: 'pol_fraud_001', policy_name: 'Fraud rejection', trigger_count: 8 },
  { policy_id: 'pol_fraud_002', policy_name: 'Fraud manual review', trigger_count: 6 },
  { policy_id: 'pol_balance_001', policy_name: 'Outstanding balance rejection', trigger_count: 4 },
]
