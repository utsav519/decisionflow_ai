export interface AnalyticsSummary {
  policies: {
    total: number
    active: number
    draft: number
    pending_approval: number
    disabled: number
    ai_generated: number
  }
  decisions: {
    total: number
    approve: number
    reject: number
    manual_review: number
    approval_rate: number
    rejection_rate: number
    manual_review_rate: number
  }
  performance: {
    average_decision_confidence: number
    average_engine_latency_ms: number
    average_total_latency_ms: number
    p95_total_latency_ms: number
  }
  quality: {
    validation_errors: number
    conflicts_detected: number
    ai_fallback_count: number
  }
}

export interface DecisionDistributionItem {
  decision: string
  count: number
}

export interface DecisionTrendItem {
  date: string
  approve: number
  reject: number
  manual_review: number
}

export interface TopPolicyItem {
  policy_id: string
  policy_name: string
  trigger_count: number
}
