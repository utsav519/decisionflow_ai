export interface AnalyticsSummary {
  total_policies: number
  active_policies: number
  total_evaluations: number
  avg_confidence: number
  policy_status_breakdown?: Record<string, number>
}

export interface DecisionDistribution {
  approve: number
  reject: number
  manual_review: number
}

export interface TrendPoint {
  date: string
  count: number
}

export interface AnalyticsTrends {
  evaluations?: TrendPoint[]
  APPROVE?: TrendPoint[]
  REJECT?: TrendPoint[]
  MANUAL_REVIEW?: TrendPoint[]
  [key: string]: TrendPoint[] | undefined
}

export interface TopPolicy {
  policy_id: string
  name: string
  match_count: number
  decision: string
}

export interface AnalyticsDashboard {
  summary: AnalyticsSummary
  distribution: DecisionDistribution
  trends: AnalyticsTrends
  top_policies: TopPolicy[]
}
