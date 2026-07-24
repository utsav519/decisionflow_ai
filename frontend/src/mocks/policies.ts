import type { Policy } from '@/types/policy'

const now = new Date().toISOString()

export const mockPolicies: Policy[] = [
  {
    id: 'pol_std_001',
    name: 'Standard upgrade approval',
    description: 'Approves low-risk customers for device upgrades.',
    domain: 'telecom',
    status: 'ACTIVE',
    priority: 100,
    decision: 'APPROVE',
    conditions: {
      all: [
        { field: 'customer_tenure_months', operator: 'greater_than_or_equal', value: 24 },
        { field: 'credit_score', operator: 'greater_than_or_equal', value: 750 },
        { field: 'payment_defaults', operator: 'equals', value: 0 },
        { field: 'fraud_risk_score', operator: 'less_than', value: 0.6 },
      ],
    },
    reason: 'Customer satisfies tenure, payment, credit, and risk requirements.',
    source: 'SEEDED',
    version: 1,
    created_by: 'system',
    approved_by: 'demo_user',
    created_at: now,
    updated_at: now,
    activated_at: now,
  },
  {
    id: 'pol_fraud_001',
    name: 'Fraud rejection',
    description: 'Rejects customers with very high fraud risk.',
    domain: 'telecom',
    status: 'ACTIVE',
    priority: 300,
    decision: 'REJECT',
    conditions: {
      all: [{ field: 'fraud_risk_score', operator: 'greater_than_or_equal', value: 0.85 }],
    },
    reason: 'Fraud risk exceeds permitted threshold.',
    source: 'SEEDED',
    version: 1,
    created_by: 'system',
    approved_by: 'demo_user',
    created_at: now,
    updated_at: now,
    activated_at: now,
  },
  {
    id: 'pol_fraud_002',
    name: 'Fraud manual review',
    description: 'Routes borderline fraud cases for manual review.',
    domain: 'telecom',
    status: 'ACTIVE',
    priority: 250,
    decision: 'MANUAL_REVIEW',
    conditions: {
      all: [
        { field: 'fraud_risk_score', operator: 'greater_than_or_equal', value: 0.6 },
        { field: 'fraud_risk_score', operator: 'less_than', value: 0.85 },
      ],
    },
    reason: 'Fraud risk in review band.',
    source: 'SEEDED',
    version: 1,
    created_by: 'system',
    approved_by: 'demo_user',
    created_at: now,
    updated_at: now,
    activated_at: now,
  },
  {
    id: 'pol_balance_001',
    name: 'Outstanding balance rejection',
    domain: 'telecom',
    status: 'ACTIVE',
    priority: 220,
    decision: 'REJECT',
    conditions: {
      all: [{ field: 'outstanding_balance', operator: 'greater_than', value: 10000 }],
    },
    reason: 'Outstanding balance too high.',
    source: 'SEEDED',
    version: 1,
    created_by: 'system',
    approved_by: 'demo_user',
    created_at: now,
    updated_at: now,
    activated_at: now,
  },
  {
    id: 'pol_premium_001',
    name: 'Premium override approval',
    domain: 'telecom',
    status: 'ACTIVE',
    priority: 120,
    decision: 'APPROVE',
    conditions: {
      all: [
        { field: 'customer_segment', operator: 'equals', value: 'PREMIUM' },
        { field: 'customer_tenure_months', operator: 'greater_than_or_equal', value: 18 },
        { field: 'credit_score', operator: 'greater_than_or_equal', value: 780 },
        { field: 'fraud_risk_score', operator: 'less_than', value: 0.4 },
      ],
    },
    reason: 'Premium segment override.',
    source: 'SEEDED',
    version: 1,
    created_by: 'system',
    approved_by: 'demo_user',
    created_at: now,
    updated_at: now,
    activated_at: now,
  },
  {
    id: 'pol_draft_001',
    name: 'New device promo draft',
    domain: 'telecom',
    status: 'DRAFT',
    priority: 90,
    decision: 'APPROVE',
    conditions: {
      all: [{ field: 'customer_tenure_months', operator: 'greater_than_or_equal', value: 12 }],
    },
    reason: 'Promotional eligibility draft.',
    source: 'AI_GENERATED',
    version: 1,
    ai_metadata: { generated: true, ai_confidence: 88 },
    created_by: 'demo_user',
    created_at: now,
    updated_at: now,
  },
]

let policyStore = [...mockPolicies]

export function getPolicyStore() {
  return policyStore
}

export function setPolicyStore(policies: Policy[]) {
  policyStore = policies
}

export function resetPolicyStore() {
  policyStore = [...mockPolicies]
}
