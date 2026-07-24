import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { ConfidenceMeter } from '@/components/common/ConfidenceMeter'
import { ConfirmDialog } from '@/components/common/ConfirmDialog'
import { DecisionBadge } from '@/components/common/DecisionBadge'
import { ErrorState } from '@/components/common/ErrorState'
import { JsonViewer } from '@/components/common/JsonViewer'
import { LoadingSkeleton } from '@/components/common/LoadingSkeleton'
import { PageHeader } from '@/components/common/PageHeader'
import { ConditionTree } from '@/components/policy/ConditionTree'
import { useToast } from '@/hooks/useToast'
import { generatePolicy } from '@/services/aiApi'
import { activatePolicy, createPolicy } from '@/services/policyApi'
import type { GeneratedPolicyResult } from '@/types/policy'
import { TELECOM_FIELDS } from '@/utils/constants'

const schema = z.object({
  policy_text: z.string().min(10, 'Enter a more detailed policy.').max(5000),
  domain: z.literal('telecom'),
  preferred_decision: z
    .union([z.enum(['APPROVE', 'REJECT', 'MANUAL_REVIEW']), z.literal('')])
    .transform((value) => (value === '' ? undefined : value))
    .optional(),
  preferred_priority: z.preprocess(
    (value) => (value === '' || Number.isNaN(Number(value)) ? undefined : Number(value)),
    z.number().int().min(1).max(1000).optional(),
  ),
  generate_test_cases: z.boolean(),
})

type FormValues = z.infer<typeof schema>

export function PolicyStudioPage() {
  const navigate = useNavigate()
  const { toast } = useToast()
  const [result, setResult] = useState<GeneratedPolicyResult | null>(null)
  const [savedPolicyId, setSavedPolicyId] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [activating, setActivating] = useState(false)
  const [showActivateConfirm, setShowActivateConfirm] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [tab, setTab] = useState<'visual' | 'json' | 'tests'>('visual')

  const { register, handleSubmit, watch, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      policy_text: '',
      domain: 'telecom',
      generate_test_cases: true,
      preferred_priority: 100,
    },
  })

  const policyText = watch('policy_text')

  async function onGenerate(values: FormValues) {
    try {
      setLoading(true)
      setError(null)
      setSavedPolicyId(null)
      const data = await generatePolicy({
        policy_text: values.policy_text,
        domain: values.domain,
        preferred_decision: values.preferred_decision,
        preferred_priority: values.preferred_priority,
        generate_test_cases: values.generate_test_cases,
      })
      setResult(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Generation failed')
    } finally {
      setLoading(false)
    }
  }

  async function onSaveDraft() {
    if (!result?.generated_policy) return
    try {
      setSaving(true)
      const policy = await createPolicy({
        ...result.generated_policy,
        ai_metadata: { generated: true, ai_confidence: result.ai_confidence },
      })
      setSavedPolicyId(policy.id)
      toast('Policy saved as draft.', 'success')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Save failed')
    } finally {
      setSaving(false)
    }
  }

  async function onActivate() {
    if (!savedPolicyId) return
    try {
      setActivating(true)
      await activatePolicy(savedPolicyId)
      toast('Policy activated successfully.', 'success')
      navigate(`/policies/${savedPolicyId}`)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Activation failed')
      toast(e instanceof Error ? e.message : 'Activation failed', 'error')
    } finally {
      setActivating(false)
      setShowActivateConfirm(false)
    }
  }

  const canSave = result?.generated_policy && result.validation.status !== 'NEEDS_CLARIFICATION'
  const canActivate = !!savedPolicyId && result?.validation.status === 'PASSED'

  return (
    <div>
      <PageHeader
        backTo="/policies"
        backLabel="Back to Policies"
        title="AI Policy Studio"
        subtitle="Describe a business policy in natural language and review the generated structured rule."
      />

      <div className="grid gap-6 xl:grid-cols-2">
        <div className="space-y-4 rounded-xl border border-border bg-surface p-5 shadow-sm">
          <form onSubmit={handleSubmit(onGenerate)} className="space-y-4">
            <div>
              <label htmlFor="policy_text" className="mb-1 block text-sm font-medium">
                Describe your business policy
              </label>
              <textarea
                id="policy_text"
                {...register('policy_text')}
                rows={8}
                placeholder="Example: Approve premium device upgrades for customers with at least 24 months tenure..."
                className="w-full rounded-lg border border-border px-3 py-2 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand"
              />
              <div className="mt-1 flex justify-between text-xs text-text-muted">
                <span>{errors.policy_text?.message}</span>
                <span>{policyText.length}/5000</span>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label className="mb-1 block text-sm font-medium">Domain</label>
                <input disabled value="Telecom" className="w-full rounded-lg border border-border bg-surface-muted px-3 py-2 text-sm" />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Preferred priority</label>
                <input type="number" {...register('preferred_priority', { valueAsNumber: true })} className="w-full rounded-lg border border-border px-3 py-2 text-sm" />
              </div>
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium">Preferred decision</label>
              <select {...register('preferred_decision')} className="w-full rounded-lg border border-border px-3 py-2 text-sm">
                <option value="">Auto detect</option>
                <option value="APPROVE">APPROVE</option>
                <option value="REJECT">REJECT</option>
                <option value="MANUAL_REVIEW">MANUAL REVIEW</option>
              </select>
            </div>

            <label className="flex items-center gap-2 text-sm">
              <input type="checkbox" {...register('generate_test_cases')} />
              Generate test cases
            </label>

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-brand px-4 py-2.5 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-60"
            >
              {loading ? 'Generating and validating policy...' : 'Generate Policy'}
            </button>
          </form>

          <details className="rounded-lg border border-border p-3">
            <summary className="cursor-pointer text-sm font-medium">Supported fields reference</summary>
            <div className="mt-3 max-h-48 space-y-2 overflow-auto text-xs">
              {TELECOM_FIELDS.map((f) => (
                <div key={f.name} className="border-b border-border pb-2">
                  <p className="font-medium">{f.label}</p>
                  <p className="text-text-muted">{f.name} · {f.type}</p>
                </div>
              ))}
            </div>
          </details>
        </div>

        <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
          {error && <ErrorState message={error} />}
          {!result && !loading && (
            <p className="py-20 text-center text-sm text-text-muted">Your generated policy will appear here.</p>
          )}
          {loading && <LoadingSkeleton rows={4} />}
          {result && !loading && (
            <div className="space-y-4">
              <ConfidenceMeter score={result.ai_confidence} />
              <p className="text-sm">
                Validation: <span className="font-medium">{result.validation.status}</span>
              </p>

              {result.ambiguities.length > 0 && (
                <div className="rounded-lg border border-amber-200 bg-amber-50 p-3">
                  <p className="text-sm font-medium text-amber-900">Clarification needed</p>
                  {result.ambiguities.map((a) => (
                    <div key={a.term} className="mt-2 text-sm">
                      <p className="font-medium">{a.term}</p>
                      <p className="text-amber-800">{a.question}</p>
                    </div>
                  ))}
                </div>
              )}

              {result.assumptions.length > 0 && (
                <div className="rounded-lg border border-blue-200 bg-blue-50 p-3 text-sm">
                  <p className="font-medium">Assumptions</p>
                  <ul className="mt-1 list-disc pl-5">
                    {result.assumptions.map((a) => <li key={a}>{a}</li>)}
                  </ul>
                </div>
              )}

              {result.generated_policy && (
                <>
                  <div className="flex items-center gap-2">
                    <h3 className="text-lg font-semibold">{result.generated_policy.name}</h3>
                    <DecisionBadge decision={result.generated_policy.decision} />
                  </div>
                  <p className="text-sm text-text-secondary">{result.generated_policy.description}</p>
                  <p className="text-sm">Priority: {result.generated_policy.priority}</p>

                  <div className="flex gap-2 border-b border-border">
                    {(['visual', 'json', 'tests'] as const).map((t) => (
                      <button key={t} type="button" onClick={() => setTab(t)} className={`px-3 py-2 text-sm capitalize ${tab === t ? 'border-b-2 border-brand font-medium' : 'text-text-muted'}`}>
                        {t === 'tests' ? 'Test Cases' : t}
                      </button>
                    ))}
                  </div>

                  {tab === 'visual' && <ConditionTree conditions={result.generated_policy.conditions} />}
                  {tab === 'json' && <JsonViewer data={result.generated_policy} />}
                  {tab === 'tests' && (
                    <div className="space-y-2">
                      {result.suggested_test_cases.map((tc) => (
                        <div key={tc.name} className="rounded-lg border border-border p-3 text-sm">
                          <p className="font-medium">{tc.name}</p>
                          <p className="text-text-muted">{tc.category} · Expected: {tc.expected_decision}</p>
                          <p className="mt-1">{tc.rationale}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="flex flex-wrap gap-2 pt-2">
                    <button
                      type="button"
                      disabled={!canSave || saving}
                      onClick={onSaveDraft}
                      className="rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-surface-muted disabled:opacity-50"
                    >
                      {saving ? 'Saving...' : savedPolicyId ? 'Saved as Draft' : 'Save as Draft'}
                    </button>
                    <button
                      type="button"
                      disabled={!canActivate || activating}
                      onClick={() => setShowActivateConfirm(true)}
                      className="rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700 disabled:opacity-50"
                    >
                      {activating ? 'Activating...' : 'Activate Policy'}
                    </button>
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>

      <ConfirmDialog
        open={showActivateConfirm}
        title="Activate this policy?"
        description="Once active, it will participate in customer decision evaluations. The policy has passed validation and will be recorded in the audit log."
        confirmLabel={activating ? 'Activating...' : 'Activate Policy'}
        onConfirm={onActivate}
        onCancel={() => setShowActivateConfirm(false)}
      />
    </div>
  )
}
