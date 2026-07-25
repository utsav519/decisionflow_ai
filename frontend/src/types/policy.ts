import type {
  PaginationMeta,
} from '@/types/api'

export type PolicyStatus =
  | 'DRAFT'
  | 'PENDING_APPROVAL'
  | 'ACTIVE'
  | 'DISABLED'
  | 'ARCHIVED'

export type PolicyDecision =
  | 'APPROVE'
  | 'REJECT'
  | 'MANUAL_REVIEW'

export type PolicySource =
  | 'AI_GENERATED'
  | 'MANUAL'
  | 'IMPORTED'
  | 'SEEDED'

export interface PolicyCondition {
  field: string
  operator: string
  value?: unknown
}

export interface PolicyConditionGroup {
  all?: PolicyConditionNode[] | null
  any?: PolicyConditionNode[] | null
}

export type PolicyConditionNode =
  | PolicyCondition
  | PolicyConditionGroup

export interface PolicyAiMetadata {
  generated: boolean
  ai_confidence?: number | null
  warnings?: string[] | null
  ambiguities?: string[] | null
  model?: string | null
}

export interface PolicyListItem {
  id: string
  version: number
  name: string
  domain: string
  status: PolicyStatus
  priority: number
  decision: PolicyDecision
  created_by?: string | null
  updated_at: string
}

export interface Policy extends PolicyListItem {
  description?: string | null
  conditions: PolicyConditionGroup
  reason?: string | null
  source: PolicySource
  ai_metadata?: PolicyAiMetadata | null
  approved_by?: string | null
  created_at: string
  activated_at?: string | null
  disabled_at?: string | null
}

export interface PolicyListResult {
  items: PolicyListItem[]
  pagination: PaginationMeta
}

export interface PolicyCreateInput {
  name: string
  description?: string | null
  domain: string
  priority: number
  decision: PolicyDecision
  conditions: PolicyConditionGroup
  reason?: string | null
  source?: PolicySource
  ai_metadata?: PolicyAiMetadata | null
}
