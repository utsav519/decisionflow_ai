import type {
  PolicyCreateInput,
  PolicyDecision,
} from '@/types/policy'

export interface AiProviderMetadata {
  provider?: string
  model?: string
  processing_time_ms?: number
  fallback_used?: boolean
  retry_count?: number
  request_tokens?: number | null
  response_tokens?: number | null
  estimated_cost?: number | null
  [key: string]: unknown
}

export interface GeneratedCondition {
  field: string
  operator: string
  value: unknown
}

export interface GeneratedConditionGroup {
  logical_operator: 'AND' | 'OR'
  conditions: GeneratedCondition[]
}

export interface GeneratedPolicy {
  policy_name: string
  priority: number
  decision: string
  condition_group: GeneratedConditionGroup
}

export interface AiAmbiguityItem {
  field: string
  reason: string
  suggested_clarification: string
}

export interface AiAssumptionItem {
  description: string
}

export interface AiWarning {
  message: string
}

export interface GeneratedTestCase {
  name: string
  category:
    | 'POSITIVE'
    | 'NEGATIVE'
    | 'BOUNDARY'
    | 'MISSING_FIELD'
    | 'CONFLICT'
  input: Record<string, unknown>
  expected_match: boolean
  expected_decision: string
  rationale: string
}

export interface GeneratePolicyRequest {
  policy_text: string
  domain: string
  preferred_decision?: PolicyDecision
  preferred_priority?: number
  generate_test_cases: boolean
  active_policies?: Array<Record<string, unknown>>
}

export interface GeneratePolicyResult {
  generated_policy: GeneratedPolicy
  ai_confidence: number
  validation_status:
    | 'VALID'
    | 'WARNING'
    | 'FAILED'
  warnings: AiWarning[]
  ambiguities: AiAmbiguityItem[]
  assumptions: AiAssumptionItem[]
  suggested_test_cases: GeneratedTestCase[]
  provider_metadata: AiProviderMetadata
}

export interface ClarificationQuestion {
  question: string
  reason: string
}

export interface AmbiguityFinding {
  field: string
  severity: 'LOW' | 'MEDIUM' | 'HIGH'
  explanation: string
  clarification: ClarificationQuestion
}

export interface AmbiguityDetectionResult {
  has_ambiguity: boolean
  findings: AmbiguityFinding[]
  provider_metadata?: AiProviderMetadata | null
}

export interface ConflictingPolicy {
  policy_id: string
  policy_name: string
  priority: number
  decision: string
}

export interface ConflictReason {
  description: string
  severity: 'LOW' | 'MEDIUM' | 'HIGH'
}

export interface ConflictAnalysisResult {
  has_conflict: boolean
  conflicting_policies: ConflictingPolicy[]
  reasons: ConflictReason[]
  recommended_winner?: string | null
  explanation: string
  provider_metadata?: AiProviderMetadata | null
}

export interface TestCaseGenerationResult {
  generated_test_cases: GeneratedTestCase[]
  provider_metadata: AiProviderMetadata
}

function normalizeDecision(
  decision: string,
): PolicyDecision {
  if (
    decision === 'APPROVE' ||
    decision === 'REJECT' ||
    decision === 'MANUAL_REVIEW'
  ) {
    return decision
  }

  return 'MANUAL_REVIEW'
}

export function buildPolicyCreateInput(
  result: GeneratePolicyResult,
  domain: string,
  originalPolicyText: string,
): PolicyCreateInput {
  const generated =
    result.generated_policy

  const conditions =
    generated.condition_group.conditions.map(
      (condition) => ({
        field: condition.field,
        operator: condition.operator,
        value: condition.value,
      }),
    )

  const conditionGroup =
    generated.condition_group
      .logical_operator === 'OR'
      ? { any: conditions }
      : { all: conditions }

  return {
    name: generated.policy_name,
    description:
      `AI-generated policy based on: ` +
      originalPolicyText.trim(),
    domain,
    priority: generated.priority,
    decision: normalizeDecision(
      generated.decision,
    ),
    conditions: conditionGroup,
    reason:
      'Generated from a natural-language business requirement.',
    source: 'AI_GENERATED',
    ai_metadata: {
      generated: true,
      ai_confidence: Math.round(
        result.ai_confidence * 100,
      ),
      warnings: result.warnings.map(
        (warning) => warning.message,
      ),
      ambiguities: result.ambiguities.map(
        (ambiguity) =>
          ambiguity.suggested_clarification,
      ),
      model:
        typeof result.provider_metadata.model ===
        'string'
          ? result.provider_metadata.model
          : undefined,
    },
  }
}
