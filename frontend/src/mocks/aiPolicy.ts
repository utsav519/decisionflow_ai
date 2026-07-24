import type { GeneratedPolicyResult } from '@/types/policy'

export function mockPolicyGeneration(policyText: string): GeneratedPolicyResult {
  const lower = policyText.toLowerCase()

  if (lower.includes('loyal') || lower.includes('expensive')) {
    return {
      generated_policy: null,
      ai_confidence: 35,
      validation: {
        status: 'NEEDS_CLARIFICATION',
        errors: [],
        warnings: [
          {
            code: 'AMBIGUOUS_TERM',
            message: 'The policy contains non-measurable terms.',
            severity: 'BLOCKING',
          },
        ],
      },
      ambiguities: [
        ...(lower.includes('loyal')
          ? [
              {
                term: 'loyal customers',
                question: 'How should loyalty be measured?',
                suggested_fields: ['customer_tenure_months', 'monthly_bill_amount', 'customer_segment'],
              },
            ]
          : []),
        ...(lower.includes('expensive')
          ? [
              {
                term: 'expensive devices',
                question: 'What device-price threshold should be used?',
                suggested_fields: ['requested_device_price'],
              },
            ]
          : []),
      ],
      assumptions: [],
      conflicts: [],
      suggested_test_cases: [],
    }
  }

  return {
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
        input: {
          customer_id: 'CUST-1001',
          customer_tenure_months: 36,
          credit_score: 790,
          payment_defaults: 0,
          fraud_risk_score: 0.12,
        },
        rationale: 'All thresholds satisfied.',
      },
      {
        name: 'Low credit score',
        category: 'NEGATIVE',
        expected_decision: 'MANUAL_REVIEW',
        expected_match: false,
        input: { customer_id: 'CUST-2001', credit_score: 680, fraud_risk_score: 0.2 },
        rationale: 'Credit score below threshold.',
      },
    ],
  }
}
