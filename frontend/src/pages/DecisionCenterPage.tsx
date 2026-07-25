import {
  useState,
  type FormEvent,
} from 'react'

import {
  evaluateDecision,
} from '@/api/decisions'
import {
  getApiErrorMessage,
} from '@/api/client'
import type {
  DecisionCustomer,
  DecisionEvaluationResponse,
  DecisionOutcome,
} from '@/types/decision'

import '@/App.css'

interface FormState {
  customerId: string
  tenureMonths: string
  creditScore: string
  paymentDefaults: string
  fraudRiskScore: string
  customerSegment: string
  outstandingBalance: string
  accountStatus: string
}

const approvalPreset: FormState = {
  customerId: 'CUST-DEMO-APPROVE',
  tenureMonths: '36',
  creditScore: '790',
  paymentDefaults: '0',
  fraudRiskScore: '0.12',
  customerSegment: 'PREMIUM',
  outstandingBalance: '0',
  accountStatus: 'current',
}

const rejectionPreset: FormState = {
  customerId: 'CUST-DEMO-REJECT',
  tenureMonths: '36',
  creditScore: '790',
  paymentDefaults: '0',
  fraudRiskScore: '0.12',
  customerSegment: 'PREMIUM',
  outstandingBalance: '1000',
  accountStatus: 'past_due',
}

const missingFieldsPreset: FormState = {
  customerId: 'CUST-DEMO-MISSING',
  tenureMonths: '',
  creditScore: '790',
  paymentDefaults: '',
  fraudRiskScore: '',
  customerSegment: '',
  outstandingBalance: '',
  accountStatus: '',
}

function optionalNumber(value: string): number | undefined {
  const trimmed = value.trim()

  if (!trimmed) {
    return undefined
  }

  const parsed = Number(trimmed)

  return Number.isFinite(parsed)
    ? parsed
    : undefined
}

function buildCustomer(
  form: FormState,
): DecisionCustomer {
  return {
    customer_id: form.customerId.trim() || undefined,
    customer_tenure_months: optionalNumber(
      form.tenureMonths,
    ),
    credit_score: optionalNumber(form.creditScore),
    payment_defaults: optionalNumber(
      form.paymentDefaults,
    ),
    fraud_risk_score: optionalNumber(
      form.fraudRiskScore,
    ),
    customer_segment:
      form.customerSegment.trim() || undefined,
    outstanding_balance: optionalNumber(
      form.outstandingBalance,
    ),
    account_status:
      form.accountStatus.trim() || undefined,
  }
}

function getDecisionClass(
  decision: DecisionOutcome,
): string {
  return decision.toLowerCase().replace('_', '-')
}

export function DecisionCenterPage() {
  const [form, setForm] = useState<FormState>(
    approvalPreset,
  )
  const [result, setResult] =
    useState<DecisionEvaluationResponse | null>(null)
  const [correlationId, setCorrelationId] =
    useState<string | null>(null)
  const [error, setError] =
    useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  function updateField(
    field: keyof FormState,
    value: string,
  ): void {
    setForm((current) => ({
      ...current,
      [field]: value,
    }))
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault()

    setLoading(true)
    setError(null)
    setResult(null)

    const uniqueId = crypto.randomUUID()
    const requestId = `req_ui_${uniqueId}`
    const nextCorrelationId = `cor_ui_${uniqueId}`

    try {
      const response = await evaluateDecision(
        {
          request_id: requestId,
          domain: 'telecom',
          customer: buildCustomer(form),
          context: {
            channel: 'ADMIN_PORTAL',
            currency: 'INR',
            requested_action: 'DEVICE_UPGRADE',
          },
          options: {
            include_explanation: true,
            include_unmatched_rules: true,
            include_condition_trace: true,
          },
        },
        {
          correlationId: nextCorrelationId,
          userId: 'frontend_demo_user',
        },
      )

      setResult(response.data)
      setCorrelationId(response.correlation_id)
    } catch (requestError) {
      setError(getApiErrorMessage(requestError))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">DecisionFlow AI</p>
          <h1>Decision Center</h1>
        </div>

        <div className="environment-pill">
          <span className="status-dot" />
          MySQL · Deterministic Engine
        </div>
      </header>

      <main className="dashboard">
        <section className="panel input-panel">
          <div className="panel-heading">
            <div>
              <p className="section-label">
                Evaluation input
              </p>
              <h2>Customer decision request</h2>
            </div>

            <div className="preset-buttons">
              <button
                type="button"
                className="secondary-button"
                onClick={() => setForm(approvalPreset)}
              >
                Approval
              </button>

              <button
                type="button"
                className="secondary-button"
                onClick={() => setForm(rejectionPreset)}
              >
                Rejection
              </button>

              <button
                type="button"
                className="secondary-button"
                onClick={() =>
                  setForm(missingFieldsPreset)
                }
              >
                Missing fields
              </button>
            </div>
          </div>

          <form
            className="decision-form"
            onSubmit={handleSubmit}
          >
            <label>
              Customer ID
              <input
                value={form.customerId}
                onChange={(event) =>
                  updateField(
                    'customerId',
                    event.target.value,
                  )
                }
                placeholder="CUST-001"
              />
            </label>

            <label>
              Credit score
              <input
                type="number"
                min="300"
                max="900"
                value={form.creditScore}
                onChange={(event) =>
                  updateField(
                    'creditScore',
                    event.target.value,
                  )
                }
                placeholder="790"
              />
            </label>

            <label>
              Customer tenure (months)
              <input
                type="number"
                min="0"
                value={form.tenureMonths}
                onChange={(event) =>
                  updateField(
                    'tenureMonths',
                    event.target.value,
                  )
                }
                placeholder="Leave blank"
              />
            </label>

            <label>
              Payment defaults
              <input
                type="number"
                min="0"
                value={form.paymentDefaults}
                onChange={(event) =>
                  updateField(
                    'paymentDefaults',
                    event.target.value,
                  )
                }
                placeholder="Leave blank"
              />
            </label>

            <label>
              Fraud-risk score
              <input
                type="number"
                min="0"
                max="1"
                step="0.01"
                value={form.fraudRiskScore}
                onChange={(event) =>
                  updateField(
                    'fraudRiskScore',
                    event.target.value,
                  )
                }
                placeholder="Leave blank"
              />
            </label>

            <label>
              Customer segment
              <select
                value={form.customerSegment}
                onChange={(event) =>
                  updateField(
                    'customerSegment',
                    event.target.value,
                  )
                }
              >
                <option value="">
                  Not supplied
                </option>
                <option value="PREMIUM">
                  Premium
                </option>
                <option value="ENTERPRISE">
                  Enterprise
                </option>
                <option value="STANDARD">
                  Standard
                </option>
              </select>
            </label>

            <label>
              Outstanding balance
              <input
                type="number"
                min="0"
                value={form.outstandingBalance}
                onChange={(event) =>
                  updateField(
                    'outstandingBalance',
                    event.target.value,
                  )
                }
                placeholder="Leave blank"
              />
            </label>

            <label>
              Account status
              <select
                value={form.accountStatus}
                onChange={(event) =>
                  updateField(
                    'accountStatus',
                    event.target.value,
                  )
                }
              >
                <option value="">
                  Not supplied
                </option>
                <option value="current">
                  Current
                </option>
                <option value="past_due">
                  Past due
                </option>
                <option value="suspended">
                  Suspended
                </option>
              </select>
            </label>

            <button
              className="primary-button"
              type="submit"
              disabled={loading}
            >
              {loading
                ? 'Evaluating policies…'
                : 'Run decision evaluation'}
            </button>
          </form>

          {error && (
            <div className="error-message">
              <strong>Evaluation failed</strong>
              <span>{error}</span>
            </div>
          )}
        </section>

        <section className="panel result-panel">
          {!result && !loading && (
            <div className="empty-state">
              <div className="empty-icon">DF</div>
              <h2>No evaluation yet</h2>
              <p>
                Select a preset or enter customer data,
                then run the deterministic decision engine.
              </p>
            </div>
          )}

          {loading && (
            <div className="empty-state">
              <div className="spinner" />
              <h2>Evaluating active policies</h2>
              <p>
                Loading policy catalogue, resolving
                conflicts and generating the explanation.
              </p>
            </div>
          )}

          {result && (
            <div className="result-content">
              <div className="result-header">
                <div>
                  <p className="section-label">
                    Final deterministic outcome
                  </p>

                  <div
                    className={`decision-badge ${getDecisionClass(
                      result.decision,
                    )}`}
                  >
                    {result.decision.replace('_', ' ')}
                  </div>
                </div>

                <div className="confidence-box">
                  <span>Confidence</span>
                  <strong>
                    {result.decision_confidence}%
                  </strong>
                </div>
              </div>

              <div className="summary-grid">
                <article className="summary-card">
                  <span>Winning policy</span>
                  <strong>
                    {result.winning_policy?.name ??
                      'No winning policy'}
                  </strong>
                  <small>
                    {result.winning_policy
                      ? `Priority ${result.winning_policy.priority}`
                      : result.resolution.strategy}
                  </small>
                </article>

                <article className="summary-card">
                  <span>Policies matched</span>
                  <strong>
                    {result.metrics.policies_matched}
                  </strong>
                  <small>
                    {result.metrics.policies_evaluated}{' '}
                    evaluated
                  </small>
                </article>

                <article className="summary-card">
                  <span>Total latency</span>
                  <strong>
                    {result.metrics.total_latency_ms.toFixed(
                      2,
                    )}{' '}
                    ms
                  </strong>
                  <small>
                    Engine{' '}
                    {result.metrics.engine_latency_ms.toFixed(
                      2,
                    )}{' '}
                    ms
                  </small>
                </article>
              </div>

              <article className="explanation-card">
                <div className="card-title-row">
                  <h3>Decision explanation</h3>

                  <span className="source-pill">
                    {result.explanation?.generated_by ??
                      'NOT GENERATED'}
                  </span>
                </div>

                <p>
                  {result.explanation?.summary ??
                    result.resolution.reason}
                </p>

                {result.explanation?.key_factors &&
                  result.explanation.key_factors.length >
                    0 && (
                    <ul>
                      {result.explanation.key_factors.map(
                        (factor) => (
                          <li key={factor}>
                            {factor}
                          </li>
                        ),
                      )}
                    </ul>
                  )}
              </article>

              <article className="trace-card">
                <div className="card-title-row">
                  <h3>Policy trace</h3>

                  <span>
                    {result.metrics.condition_count}{' '}
                    conditions
                  </span>
                </div>

                <div className="policy-list">
                  {[
                    ...result.matched_policies,
                    ...result.unmatched_policies,
                    ...result.skipped_policies,
                  ].map((policy) => (
                    <details
                      key={policy.policy_id}
                      className="policy-item"
                      open={policy.matched}
                    >
                      <summary>
                        <div>
                          <strong>
                            {policy.policy_name}
                          </strong>
                          <span>
                            Priority {policy.priority}
                          </span>
                        </div>

                        <span
                          className={`policy-status ${
                            policy.matched
                              ? 'matched'
                              : policy.result_status.startsWith(
                                    'SKIPPED',
                                  )
                                ? 'skipped'
                                : 'unmatched'
                          }`}
                        >
                          {policy.result_status}
                        </span>
                      </summary>

                      <div className="condition-list">
                        {policy.condition_results.map(
                          (condition, index) => (
                            <div
                              className="condition-row"
                              key={`${condition.field}-${index}`}
                            >
                              <div>
                                <strong>
                                  {condition.field}
                                </strong>
                                <span>
                                  {condition.operator}
                                </span>
                              </div>

                              <div>
                                <span>
                                  Expected:{' '}
                                  {JSON.stringify(
                                    condition.expected,
                                  )}
                                </span>
                                <span>
                                  Actual:{' '}
                                  {JSON.stringify(
                                    condition.actual,
                                  )}
                                </span>
                              </div>

                              <span
                                className={
                                  condition.matched
                                    ? 'condition-pass'
                                    : 'condition-fail'
                                }
                              >
                                {condition.status ??
                                  (condition.matched
                                    ? 'MATCHED'
                                    : 'UNMATCHED')}
                              </span>
                            </div>
                          ),
                        )}
                      </div>
                    </details>
                  ))}
                </div>
              </article>

              {result.warnings.length > 0 && (
                <article className="warnings-card">
                  <h3>Warnings</h3>

                  {result.warnings.map((warning) => (
                    <div
                      className="warning-row"
                      key={`${warning.code}-${warning.message}`}
                    >
                      <strong>{warning.code}</strong>
                      <span>{warning.message}</span>
                    </div>
                  ))}
                </article>
              )}

              <footer className="result-footer">
                <span>
                  Evaluation: {result.evaluation_id}
                </span>
                <span>
                  Correlation: {correlationId}
                </span>
              </footer>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}
