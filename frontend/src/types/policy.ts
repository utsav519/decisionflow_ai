export type PolicyStatus =
  | 'DRAFT'
  | 'PENDING_APPROVAL'
  | 'ACTIVE'
  | 'DISABLED'
  | 'ARCHIVED'

export type DecisionOutcome = 'APPROVE' | 'REJECT' | 'MANUAL_REVIEW' | 'NO_MATCH'

export type PolicySource = 'AI_GENERATED' | 'MANUAL' | 'IMPORTED' | 'SEEDED'

export interface Condition {
  field: string
  operator: string
  value?: unknown
}

export interface ConditionGroup {
  all?: ConditionNode[]
  any?: ConditionNode[]
}

export type ConditionNode = Condition | ConditionGroup

export interface AIMetadata {
  generated: boolean
  ai_confidence?: number
  warnings?: unknown[]
  ambiguities?: unknown[]
  model?: string
}

export interface Policy {
  id: string
  name: string
  description?: string
  domain: string
  status: PolicyStatus
  priority: number
  decision: Exclude<DecisionOutcome, 'NO_MATCH'>
  conditions: ConditionGroup
  reason?: string
  source: PolicySource
  version: number
  ai_metadata?: AIMetadata
  created_by?: string
  approved_by?: string
  created_at: string
  updated_at: string
  activated_at?: string
}

export interface PolicyConflict {
  severity: 'INFO' | 'WARNING' | 'BLOCKING'
  existing_policy_id: string
  existing_policy_name: string
  conflict_type: string
  fields: string[]
  overlap?: { minimum?: number; maximum?: number }
  deterministic_reason: string
  ai_explanation?: string
  suggestions?: string[]
}

export interface AmbiguityItem {
  term: string
  question: string
  suggested_fields: string[]
}

export interface AIWarning {
  code: string
  message: string
  severity?: 'INFO' | 'WARNING' | 'BLOCKING'
}

export interface SuggestedTestCase {
  name: string
  category?: string
  expected_decision: DecisionOutcome
  expected_match?: boolean
  input: Record<string, unknown>
  rationale?: string
}

export interface GeneratedPolicyResult {
  generated_policy: Omit<
    Policy,
    'id' | 'version' | 'created_at' | 'updated_at' | 'approved_by' | 'activated_at'
  > | null
  ai_confidence: number
  validation: {
    status: 'PASSED' | 'PASSED_WITH_WARNINGS' | 'NEEDS_CLARIFICATION' | 'FAILED'
    errors: unknown[]
    warnings: AIWarning[]
  }
  ambiguities: AmbiguityItem[]
  assumptions: string[]
  conflicts: PolicyConflict[]
  suggested_test_cases: SuggestedTestCase[]
}
