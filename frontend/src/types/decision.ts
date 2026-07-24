import type { DecisionOutcome } from '@/types/policy'

export interface CustomerData {
  customer_id: string
  customer_tenure_months?: number
  credit_score?: number
  payment_defaults?: number
  fraud_risk_score?: number
  monthly_bill_amount?: number
  requested_device_price?: number
  customer_segment?: 'STANDARD' | 'PREMIUM' | 'BUSINESS'
  current_plan?: string
  outstanding_balance?: number
  is_existing_customer?: boolean
  previous_upgrade_months_ago?: number
}

export interface DecisionEvaluationRequest {
  request_id?: string
  domain: 'telecom'
  customer: CustomerData
  context: {
    channel: string
    currency: string
    requested_action: string
  }
  options: {
    include_explanation: boolean
    include_unmatched_rules: boolean
    include_condition_trace: boolean
  }
}

export interface ConditionResult {
  field: string
  operator: string
  expected?: unknown
  actual?: unknown
  matched: boolean
  status?: string
  reason?: string
}

export interface EvaluatedPolicy {
  policy_id: string
  policy_name: string
  priority: number
  decision: DecisionOutcome
  matched: boolean
  condition_results?: ConditionResult[]
  missing_fields?: string[]
  reason?: string
}

export interface DecisionEvaluationResult {
  evaluation_id: string
  request_id?: string
  decision: DecisionOutcome
  decision_confidence: number
  winning_policy: {
    id: string
    name: string
    priority: number
    decision: DecisionOutcome
    version: number
  } | null
  matched_policies: EvaluatedPolicy[]
  unmatched_policies: EvaluatedPolicy[]
  skipped_policies: EvaluatedPolicy[]
  resolution?: {
    strategy: string
    reason: string
    tie_breaker_used?: boolean
  }
  explanation: {
    summary: string
    generated_by: 'AI' | 'DETERMINISTIC_FALLBACK'
    fallback_used: boolean
  }
  metrics: {
    policies_loaded: number
    policies_evaluated: number
    policies_matched: number
    policies_skipped: number
    condition_count: number
    conflicts_detected: number
    engine_latency_ms: number
    explanation_latency_ms?: number
    total_latency_ms: number
  }
  warnings: Array<Record<string, unknown>>
  evaluated_at: string
}
