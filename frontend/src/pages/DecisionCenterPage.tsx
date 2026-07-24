import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { ConfidenceMeter } from '@/components/common/ConfidenceMeter'
import { DecisionBadge } from '@/components/common/DecisionBadge'
import { ErrorState } from '@/components/common/ErrorState'
import { PageHeader } from '@/components/common/PageHeader'
import { evaluateDecision } from '@/services/decisionApi'
import type { CustomerData, DecisionEvaluationResult } from '@/types/decision'
import { CUSTOMER_PRESETS } from '@/utils/constants'
import { formatDateTime, formatMs } from '@/utils/formatters'

export function DecisionCenterPage() {
  const [result, setResult] = useState<DecisionEvaluationResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const { register, handleSubmit, reset } = useForm<CustomerData>({
    defaultValues: { customer_id: '', customer_segment: 'STANDARD' },
  })

  function applyPreset(preset: keyof typeof CUSTOMER_PRESETS) {
    reset(CUSTOMER_PRESETS[preset])
  }

  async function onEvaluate(data: CustomerData) {
    try {
      setLoading(true)
      setError(null)
      const evaluation = await evaluateDecision({
        domain: 'telecom',
        customer: data,
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
      })
      setResult(evaluation)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Evaluation failed')
    } finally {
      setLoading(false)
    }
  }

  const fields: Array<{ name: keyof CustomerData; label: string; type?: string }> = [
    { name: 'customer_id', label: 'Customer ID' },
    { name: 'customer_tenure_months', label: 'Tenure (months)', type: 'number' },
    { name: 'credit_score', label: 'Credit Score', type: 'number' },
    { name: 'payment_defaults', label: 'Payment Defaults', type: 'number' },
    { name: 'fraud_risk_score', label: 'Fraud Risk Score', type: 'number' },
    { name: 'monthly_bill_amount', label: 'Monthly Bill', type: 'number' },
    { name: 'requested_device_price', label: 'Device Price', type: 'number' },
    { name: 'outstanding_balance', label: 'Outstanding Balance', type: 'number' },
    { name: 'previous_upgrade_months_ago', label: 'Previous Upgrade (months)', type: 'number' },
    { name: 'current_plan', label: 'Current Plan' },
  ]

  return (
    <div>
      <PageHeader
        title="Decision Center"
        subtitle="Submit customer attributes and review the deterministic decision with full explainability."
      />

      <div className="grid gap-6 xl:grid-cols-2">
        <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
          <div className="mb-4 flex flex-wrap gap-2">
            {(['eligible', 'highFraud', 'missingInfo', 'outstandingBalance'] as const).map((preset) => (
              <button
                key={preset}
                type="button"
                onClick={() => applyPreset(preset)}
                className="rounded-md border border-border px-3 py-1 text-xs hover:bg-surface-muted"
              >
                {preset === 'eligible' && 'Eligible customer'}
                {preset === 'highFraud' && 'High fraud risk'}
                {preset === 'missingInfo' && 'Missing info'}
                {preset === 'outstandingBalance' && 'High balance'}
              </button>
            ))}
          </div>

          <form noValidate onSubmit={handleSubmit(onEvaluate)} className="space-y-3" data-testid="evaluation-form">
            {fields.map(({ name, label, type }) => (
              <div key={name}>
                <label className="mb-1 block text-sm font-medium">{label}</label>
                <input
                  {...register(name, type === 'number' ? { valueAsNumber: true } : undefined)}
                  type={type ?? 'text'}
                  className="w-full rounded-lg border border-border px-3 py-2 text-sm"
                />
              </div>
            ))}
            <div>
              <label className="mb-1 block text-sm font-medium">Customer Segment</label>
              <select {...register('customer_segment')} className="w-full rounded-lg border border-border px-3 py-2 text-sm">
                <option value="STANDARD">STANDARD</option>
                <option value="PREMIUM">PREMIUM</option>
                <option value="BUSINESS">BUSINESS</option>
              </select>
            </div>
            <label className="flex items-center gap-2 text-sm">
              <input type="checkbox" {...register('is_existing_customer')} />
              Existing customer
            </label>
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-brand px-4 py-2.5 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-60"
            >
              {loading ? 'Evaluating active policies...' : 'Evaluate Decision'}
            </button>
          </form>
        </div>

        <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
          {error && <ErrorState message={error} />}
          {!result && !loading && (
            <p className="py-20 text-center text-sm text-text-muted">Decision results will appear here after evaluation.</p>
          )}
          {result && (
            <div className="space-y-4">
              <div className="flex flex-wrap items-center gap-3">
                <DecisionBadge decision={result.decision} />
                <ConfidenceMeter score={result.decision_confidence} label="Decision confidence" />
              </div>
              <p className="text-xs text-text-muted">Evaluation ID: {result.evaluation_id} · {formatDateTime(result.evaluated_at)}</p>

              {result.winning_policy ? (
                <div className="rounded-lg border border-border bg-surface-muted p-4">
                  <p className="text-sm font-medium">Winning policy</p>
                  <p className="text-lg font-semibold">{result.winning_policy.name}</p>
                  <p className="text-sm text-text-secondary">Priority {result.winning_policy.priority} · v{result.winning_policy.version}</p>
                  {result.resolution && <p className="mt-2 text-sm">{result.resolution.reason}</p>}
                </div>
              ) : (
                <p className="text-sm text-text-secondary">No winning policy — manual review fallback applied.</p>
              )}

              <div>
                <h3 className="mb-2 font-medium">Explanation</h3>
                <p className="text-sm">{result.explanation.summary}</p>
                <p className="mt-1 text-xs text-text-muted">
                  Generated by {result.explanation.generated_by}
                  {result.explanation.fallback_used && ' (deterministic fallback)'}
                </p>
              </div>

              {result.matched_policies.length > 0 && (
                <div>
                  <h3 className="mb-2 font-medium">Matched policies</h3>
                  <div className="space-y-2">
                    {result.matched_policies.map((p) => (
                      <div key={p.policy_id} className="rounded-lg border border-border p-3 text-sm">
                        <div className="flex items-center justify-between">
                          <span className="font-medium">{p.policy_name}</span>
                          <DecisionBadge decision={p.decision} />
                        </div>
                        <p className="text-text-muted">Priority {p.priority}</p>
                        {p.condition_results?.map((cr) => (
                          <p key={cr.field} className="mt-1 text-xs">
                            {cr.field}: expected {String(cr.expected)}, actual {String(cr.actual)} — {cr.matched ? 'Matched' : 'Failed'}
                          </p>
                        ))}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {result.skipped_policies.length > 0 && (
                <div>
                  <h3 className="mb-2 font-medium">Skipped policies</h3>
                  {result.skipped_policies.map((p) => (
                    <p key={p.policy_id} className="text-sm text-text-secondary">
                      {p.policy_name}: {p.reason} {p.missing_fields?.join(', ')}
                    </p>
                  ))}
                </div>
              )}

              <div className="rounded-lg border border-border p-3 text-xs">
                <p>Policies loaded: {result.metrics.policies_loaded}</p>
                <p>Matched: {result.metrics.policies_matched}</p>
                <p>Engine latency: {formatMs(result.metrics.engine_latency_ms)}</p>
                <p>Total latency: {formatMs(result.metrics.total_latency_ms)}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
