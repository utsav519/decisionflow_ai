import type { DecisionEvaluationRequest, DecisionEvaluationResult } from '@/types/decision'

export function mockDecisionEvaluation(
  payload: DecisionEvaluationRequest,
): DecisionEvaluationResult {
  const c = payload.customer
  const fraud = c.fraud_risk_score ?? 0
  const balance = c.outstanding_balance ?? 0
  const now = new Date().toISOString()

  if (fraud >= 0.85) {
    return {
      evaluation_id: `eval_${Date.now()}`,
      request_id: payload.request_id,
      decision: 'REJECT',
      decision_confidence: 92,
      winning_policy: {
        id: 'pol_fraud_001',
        name: 'Fraud rejection',
        priority: 300,
        decision: 'REJECT',
        version: 1,
      },
      matched_policies: [
        {
          policy_id: 'pol_fraud_001',
          policy_name: 'Fraud rejection',
          priority: 300,
          decision: 'REJECT',
          matched: true,
          condition_results: [
            {
              field: 'fraud_risk_score',
              operator: 'greater_than_or_equal',
              expected: 0.85,
              actual: fraud,
              matched: true,
            },
          ],
        },
        {
          policy_id: 'pol_std_001',
          policy_name: 'Standard upgrade approval',
          priority: 100,
          decision: 'APPROVE',
          matched: true,
        },
      ],
      unmatched_policies: [],
      skipped_policies: [],
      resolution: {
        strategy: 'HIGHEST_PRIORITY',
        reason: 'Fraud rejection had priority 300, which exceeded approval priority 100.',
        tie_breaker_used: false,
      },
      explanation: {
        summary:
          'The request was rejected because the fraud-risk policy had the highest priority. The customer\'s fraud-risk score exceeded the permitted threshold, so the approval policy was overridden.',
        generated_by: 'AI',
        fallback_used: false,
      },
      metrics: {
        policies_loaded: 5,
        policies_evaluated: 5,
        policies_matched: 2,
        policies_skipped: 0,
        condition_count: 12,
        conflicts_detected: 1,
        engine_latency_ms: 45,
        explanation_latency_ms: 320,
        total_latency_ms: 365,
      },
      warnings: [],
      evaluated_at: now,
    }
  }

  if (balance > 10000) {
    return {
      evaluation_id: `eval_${Date.now()}`,
      decision: 'REJECT',
      decision_confidence: 88,
      winning_policy: {
        id: 'pol_balance_001',
        name: 'Outstanding balance rejection',
        priority: 220,
        decision: 'REJECT',
        version: 1,
      },
      matched_policies: [
        {
          policy_id: 'pol_balance_001',
          policy_name: 'Outstanding balance rejection',
          priority: 220,
          decision: 'REJECT',
          matched: true,
          condition_results: [
            {
              field: 'outstanding_balance',
              operator: 'greater_than',
              expected: 10000,
              actual: balance,
              matched: true,
            },
          ],
        },
      ],
      unmatched_policies: [],
      skipped_policies: [],
      resolution: {
        strategy: 'HIGHEST_PRIORITY',
        reason: 'Outstanding balance rejection matched with priority 220.',
      },
      explanation: {
        summary: 'The request was rejected because the outstanding balance exceeded the permitted limit.',
        generated_by: 'AI',
        fallback_used: false,
      },
      metrics: {
        policies_loaded: 5,
        policies_evaluated: 5,
        policies_matched: 1,
        policies_skipped: 0,
        condition_count: 8,
        conflicts_detected: 0,
        engine_latency_ms: 38,
        explanation_latency_ms: 280,
        total_latency_ms: 318,
      },
      warnings: [],
      evaluated_at: now,
    }
  }

  if (!c.credit_score || !c.fraud_risk_score) {
    return {
      evaluation_id: `eval_${Date.now()}`,
      decision: 'MANUAL_REVIEW',
      decision_confidence: 55,
      winning_policy: null,
      matched_policies: [],
      unmatched_policies: [],
      skipped_policies: [
        {
          policy_id: 'pol_std_001',
          policy_name: 'Standard upgrade approval',
          priority: 100,
          decision: 'APPROVE',
          matched: false,
          missing_fields: ['credit_score', 'fraud_risk_score'].filter(
            (f) => !(f in c && c[f as keyof typeof c] !== undefined),
          ),
          reason: 'Required fields missing for evaluation.',
        },
      ],
      explanation: {
        summary:
          'The request requires manual review because required fields were missing and no active policy fully matched the supplied data.',
        generated_by: 'DETERMINISTIC_FALLBACK',
        fallback_used: true,
      },
      metrics: {
        policies_loaded: 5,
        policies_evaluated: 3,
        policies_matched: 0,
        policies_skipped: 2,
        condition_count: 4,
        conflicts_detected: 0,
        engine_latency_ms: 22,
        total_latency_ms: 22,
      },
      warnings: [{ code: 'MISSING_FIELDS', message: 'Some policies were skipped due to missing fields.' }],
      evaluated_at: now,
    }
  }

  return {
    evaluation_id: `eval_${Date.now()}`,
    decision: 'APPROVE',
    decision_confidence: 96,
    winning_policy: {
      id: 'pol_std_001',
      name: 'Standard upgrade approval',
      priority: 100,
      decision: 'APPROVE',
      version: 1,
    },
    matched_policies: [
      {
        policy_id: 'pol_std_001',
        policy_name: 'Standard upgrade approval',
        priority: 100,
        decision: 'APPROVE',
        matched: true,
        condition_results: [
          {
            field: 'customer_tenure_months',
            operator: 'greater_than_or_equal',
            expected: 24,
            actual: c.customer_tenure_months,
            matched: true,
          },
          {
            field: 'credit_score',
            operator: 'greater_than_or_equal',
            expected: 750,
            actual: c.credit_score,
            matched: true,
          },
          {
            field: 'payment_defaults',
            operator: 'equals',
            expected: 0,
            actual: c.payment_defaults ?? 0,
            matched: true,
          },
          {
            field: 'fraud_risk_score',
            operator: 'less_than',
            expected: 0.6,
            actual: fraud,
            matched: true,
          },
        ],
      },
    ],
    unmatched_policies: [],
    skipped_policies: [],
    resolution: {
      strategy: 'HIGHEST_PRIORITY',
      reason: 'Standard upgrade approval matched all conditions.',
    },
    explanation: {
      summary:
        'The request was approved because the customer satisfied tenure, payment, credit, and fraud-risk requirements under the standard upgrade policy.',
      generated_by: 'AI',
      fallback_used: false,
    },
    metrics: {
      policies_loaded: 5,
      policies_evaluated: 5,
      policies_matched: 1,
      policies_skipped: 0,
      condition_count: 10,
      conflicts_detected: 0,
      engine_latency_ms: 41,
      explanation_latency_ms: 290,
      total_latency_ms: 331,
    },
    warnings: [],
    evaluated_at: now,
  }
}
