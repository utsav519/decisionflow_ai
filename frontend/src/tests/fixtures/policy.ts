import type { GeneratedPolicyResult } from '@/types/policy'

export const validPolicyText =
  'Approve premium device upgrades for customers with at least 24 months tenure, no payment defaults, credit score at least 750, and fraud risk below 0.6.'

export const ambiguousPolicyText = 'Approve loyal customers for expensive devices.'

export const mockGeneratedPolicyResult: GeneratedPolicyResult = {
  generated_policy: {
    name: 'Premium device upgrade eligibility',
    description: 'Approves low-risk customers for premium device upgrades.',
    domain: 'telecom',
    status: 'DRAFT',
    priority: 100,
    decision: 'APPROVE',
    conditions: {
      all: [
        { field: 'customer_tenure_months', operator: 'greater_than_or_equal', value: 24 },
        { field: 'payment_defaults', operator: 'equals', value: 0 },
        { field: 'credit_score', operator: 'greater_than_or_equal', value: 750 },
        { field: 'fraud_risk_score', operator: 'less_than', value: 0.6 },
      ],
    },
    reason: 'Customer satisfies tenure, payment, credit, and fraud-risk requirements.',
    source: 'AI_GENERATED',
  },
  ai_confidence: 95,
  validation: { status: 'PASSED', errors: [], warnings: [] },
  ambiguities: [],
  assumptions: ["The phrase 'no payment defaults' was mapped to payment_defaults equals 0."],
  conflicts: [],
  suggested_test_cases: [
    {
      name: 'Eligible premium customer',
      category: 'POSITIVE',
      expected_decision: 'APPROVE',
      expected_match: true,
      input: { customer_id: 'CUST-1001', credit_score: 790 },
      rationale: 'All thresholds satisfied.',
    },
  ],
}

export const mockAmbiguousPolicyResult: GeneratedPolicyResult = {
  generated_policy: null,
  ai_confidence: 35,
  validation: {
    status: 'NEEDS_CLARIFICATION',
    errors: [],
    warnings: [{ code: 'AMBIGUOUS_TERM', message: 'Non-measurable terms.', severity: 'BLOCKING' }],
  },
  ambiguities: [
    {
      term: 'loyal customers',
      question: 'How should loyalty be measured?',
      suggested_fields: ['customer_tenure_months'],
    },
  ],
  assumptions: [],
  conflicts: [],
  suggested_test_cases: [],
}
