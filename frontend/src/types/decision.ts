export type DecisionOutcome =
  | 'APPROVE'
  | 'REJECT'
  | 'MANUAL_REVIEW'
  | 'NO_MATCH'

export interface StandardResponse<T> {
  success: boolean
  data: T
  meta?: Record<string, unknown> | null
  correlation_id: string
}

export interface DecisionCustomer {
  customer_id?: string
  customer_tenure_months?: number
  credit_score?: number
  payment_defaults?: number
  fraud_risk_score?: number

  monthly_bill_amount?: number
  requested_device_price?: number
  outstanding_balance?: number
  account_status?: string

  customer_segment?: string
  current_plan?: string
  is_existing_customer?: boolean
  previous_upgrade_months_ago?: number
}

export interface DecisionContext {
  channel?: string
  currency?: string
  requested_action?: string
}

export interface DecisionOptions {
  include_explanation: boolean
  include_unmatched_rules: boolean
  include_condition_trace: boolean
}

export interface DecisionEvaluationRequest {
  request_id: string
  domain: string
  customer: DecisionCustomer
  context?: DecisionContext
  options?: DecisionOptions
}

export interface ConditionResult {
  field: string
  operator: string
  expected: unknown
  actual: unknown
  matched: boolean
  status?: string | null
  reason?: string | null
}

export interface PolicyEvaluation {
  policy_id: string
  policy_name: string
  policy_version: number
  priority: number
  decision: DecisionOutcome
  matched: boolean
  result_status: string
  condition_results: ConditionResult[]
  missing_fields: string[]
}

export interface WinningPolicy {
  id: string
  name: string
  priority: number
  decision: DecisionOutcome
  version: number
}

export interface DecisionResolution {
  decision: DecisionOutcome
  winning_policy_id?: string | null
  winning_policy_version?: number | null
  strategy: string
  reason: string
  tie_breaker_used: boolean
  competing_policy_ids: string[]
}

export interface ProviderMetadata {
  provider: string
  model: string
  processing_time_ms: number
  fallback_used: boolean
  retry_count: number
  request_tokens?: number | null
  response_tokens?: number | null
  estimated_cost?: number | null
}

export interface DecisionExplanation {
  summary: string
  key_factors: string[]
  winning_policy_reason?: string | null
  competing_policy_note?: string | null
  generated_by: string
  fallback_used: boolean
  provider_metadata?: ProviderMetadata | null
}

export interface DecisionWarning {
  code: string
  message: string
  fields?: string[] | null
}

export interface EvaluationMetrics {
  policies_loaded: number
  policies_evaluated: number
  policies_matched: number
  policies_unmatched: number
  policies_skipped: number
  condition_count: number
  conflicts_detected: number
  engine_latency_ms: number
  explanation_latency_ms: number
  total_latency_ms: number
}

export interface DecisionEvaluationResponse {
  evaluation_id: string
  request_id: string
  decision: DecisionOutcome
  decision_confidence: number
  winning_policy?: WinningPolicy | null
  matched_policies: PolicyEvaluation[]
  unmatched_policies: PolicyEvaluation[]
  skipped_policies: PolicyEvaluation[]
  resolution: DecisionResolution
  explanation?: DecisionExplanation | null
  metrics: EvaluationMetrics
  warnings: DecisionWarning[]
  evaluated_at: string
}

export interface DecisionDetailResponse
  extends DecisionEvaluationResponse {
  domain: string
  customer_id: string
}
