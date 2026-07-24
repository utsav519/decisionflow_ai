import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { ConfidenceMeter } from '@/components/common/ConfidenceMeter'
import { ConfirmDialog } from '@/components/common/ConfirmDialog'
import { DecisionBadge } from '@/components/common/DecisionBadge'
import { ErrorState } from '@/components/common/ErrorState'
import { JsonViewer } from '@/components/common/JsonViewer'
import { LoadingSkeleton } from '@/components/common/LoadingSkeleton'
import { PageHeader } from '@/components/common/PageHeader'
import { StatusBadge } from '@/components/common/StatusBadge'
import { ConditionTree } from '@/components/policy/ConditionTree'
import { useToast } from '@/hooks/useToast'
import { activatePolicy, disablePolicy, getPolicy } from '@/services/policyApi'
import type { Policy } from '@/types/policy'
import { formatDateTime } from '@/utils/formatters'

export function PolicyDetailPage() {
  const { policyId } = useParams()
  const { toast } = useToast()
  const [policy, setPolicy] = useState<Policy | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [confirmAction, setConfirmAction] = useState<'activate' | 'disable' | null>(null)
  const [actionLoading, setActionLoading] = useState(false)

  useEffect(() => {
    if (!policyId) return
    getPolicy(policyId)
      .then(setPolicy)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [policyId])

  async function handleActivate() {
    if (!policy) return
    try {
      setActionLoading(true)
      await activatePolicy(policy.id)
      setPolicy({ ...policy, status: 'ACTIVE', activated_at: new Date().toISOString() })
      toast('Policy activated successfully.', 'success')
    } catch (e) {
      toast(e instanceof Error ? e.message : 'Activation failed', 'error')
    } finally {
      setActionLoading(false)
      setConfirmAction(null)
    }
  }

  async function handleDisable() {
    if (!policy) return
    try {
      setActionLoading(true)
      await disablePolicy(policy.id)
      setPolicy({ ...policy, status: 'DISABLED' })
      toast('Policy disabled.', 'success')
    } catch (e) {
      toast(e instanceof Error ? e.message : 'Disable failed', 'error')
    } finally {
      setActionLoading(false)
      setConfirmAction(null)
    }
  }

  if (loading) return <LoadingSkeleton rows={4} />
  if (error) return <ErrorState message={error} />
  if (!policy) return null

  return (
    <div>
      <PageHeader
        backTo="/policies"
        backLabel="Back to Policies"
        title={policy.name}
        subtitle={policy.description}
        actions={
          <>
            {policy.status === 'DRAFT' && (
              <button
                type="button"
                onClick={() => setConfirmAction('activate')}
                disabled={actionLoading}
                className="rounded-lg bg-green-600 px-4 py-2 text-sm text-white hover:bg-green-700 disabled:opacity-60"
              >
                Activate
              </button>
            )}
            {policy.status === 'ACTIVE' && (
              <button
                type="button"
                onClick={() => setConfirmAction('disable')}
                disabled={actionLoading}
                className="rounded-lg border border-border px-4 py-2 text-sm hover:bg-surface-muted disabled:opacity-60"
              >
                Disable
              </button>
            )}
            <Link to="/decisions" className="rounded-lg bg-brand px-4 py-2 text-sm text-white hover:bg-blue-700">
              Evaluate Customer
            </Link>
          </>
        }
      />

      <div className="mb-4 flex flex-wrap gap-2">
        <StatusBadge status={policy.status} />
        <DecisionBadge decision={policy.decision} />
        <span className="rounded-md bg-slate-100 px-2 py-0.5 text-xs">Priority {policy.priority}</span>
        <span className="rounded-md bg-slate-100 px-2 py-0.5 text-xs">v{policy.version}</span>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
          <h2 className="mb-3 font-semibold">Conditions</h2>
          <ConditionTree conditions={policy.conditions} />
          {policy.reason && <p className="mt-4 text-sm text-text-secondary">{policy.reason}</p>}
        </div>
        <div className="space-y-4">
          <div className="rounded-xl border border-border bg-surface p-5 text-sm shadow-sm">
            <h2 className="mb-3 font-semibold">Metadata</h2>
            <div className="space-y-2">
              <p>Source: {policy.source}</p>
              <p>Created: {formatDateTime(policy.created_at)}</p>
              <p>Updated: {formatDateTime(policy.updated_at)}</p>
              {policy.activated_at && <p>Activated: {formatDateTime(policy.activated_at)}</p>}
            </div>
          </div>
          {policy.ai_metadata?.ai_confidence && (
            <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
              <ConfidenceMeter score={policy.ai_metadata.ai_confidence} />
            </div>
          )}
          <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
            <h2 className="mb-3 font-semibold">Raw JSON</h2>
            <JsonViewer data={policy} />
          </div>
        </div>
      </div>

      <ConfirmDialog
        open={confirmAction === 'activate'}
        title="Activate this policy?"
        description="Once active, it will participate in customer decision evaluations and be recorded in the audit log."
        confirmLabel={actionLoading ? 'Activating...' : 'Activate Policy'}
        onConfirm={handleActivate}
        onCancel={() => setConfirmAction(null)}
      />

      <ConfirmDialog
        open={confirmAction === 'disable'}
        title="Disable this policy?"
        description="The policy will no longer participate in new decision evaluations. Existing audit records remain unchanged."
        confirmLabel={actionLoading ? 'Disabling...' : 'Disable Policy'}
        confirmVariant="danger"
        onConfirm={handleDisable}
        onCancel={() => setConfirmAction(null)}
      />
    </div>
  )
}
