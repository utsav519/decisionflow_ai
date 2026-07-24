import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { DecisionBadge } from '@/components/common/DecisionBadge'
import { EmptyState } from '@/components/common/EmptyState'
import { ErrorState } from '@/components/common/ErrorState'
import { TableSkeleton } from '@/components/common/LoadingSkeleton'
import { PageHeader } from '@/components/common/PageHeader'
import { StatusBadge } from '@/components/common/StatusBadge'
import { listPolicies } from '@/services/policyApi'
import type { Policy } from '@/types/policy'
import { formatDateTime } from '@/utils/formatters'

export function PoliciesPage() {
  const [policies, setPolicies] = useState<Policy[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState('')

  useEffect(() => {
    async function load() {
      try {
        setLoading(true)
        const data = await listPolicies({ search, status: status || undefined })
        setPolicies((data as { items: Policy[] }).items)
        setError(null)
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Failed to load policies')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [search, status])

  return (
    <div>
      <PageHeader
        title="Policies"
        subtitle="Manage eligibility and risk policies."
        actions={
          <Link to="/policies/new" className="rounded-lg bg-brand px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">
            Create Policy
          </Link>
        }
      />

      <div className="mb-4 flex flex-wrap gap-3">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search policies..."
          className="rounded-lg border border-border px-3 py-2 text-sm"
        />
        <select value={status} onChange={(e) => setStatus(e.target.value)} className="rounded-lg border border-border px-3 py-2 text-sm">
          <option value="">All statuses</option>
          <option value="ACTIVE">Active</option>
          <option value="DRAFT">Draft</option>
          <option value="DISABLED">Disabled</option>
        </select>
      </div>

      {loading && <TableSkeleton rows={5} />}
      {error && <ErrorState message={error} onRetry={() => window.location.reload()} />}
      {!loading && !error && policies.length === 0 && (
        <EmptyState title="No policies found" description="Create your first policy in AI Policy Studio." />
      )}

      {!loading && !error && policies.length > 0 && (
        <div className="overflow-x-auto rounded-xl border border-border bg-surface shadow-sm">
          <table className="min-w-full text-sm">
            <thead className="border-b border-border bg-surface-muted text-left text-text-secondary">
              <tr>
                <th className="px-4 py-3">Name</th>
                <th className="px-4 py-3">Decision</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Priority</th>
                <th className="px-4 py-3">Source</th>
                <th className="px-4 py-3">Updated</th>
                <th className="px-4 py-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {policies.map((policy) => (
                <tr key={policy.id} className="border-b border-border last:border-0">
                  <td className="px-4 py-3 font-medium">{policy.name}</td>
                  <td className="px-4 py-3"><DecisionBadge decision={policy.decision} /></td>
                  <td className="px-4 py-3"><StatusBadge status={policy.status} /></td>
                  <td className="px-4 py-3">{policy.priority}</td>
                  <td className="px-4 py-3">{policy.source}</td>
                  <td className="px-4 py-3">{formatDateTime(policy.updated_at)}</td>
                  <td className="px-4 py-3">
                    <Link to={`/policies/${policy.id}`} className="text-brand hover:underline">View</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
