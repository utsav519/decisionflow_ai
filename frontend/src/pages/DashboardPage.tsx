import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts'
import { StatCard } from '@/components/cards/StatCard'
import { EmptyState } from '@/components/common/EmptyState'
import { ErrorState } from '@/components/common/ErrorState'
import { PageSkeleton } from '@/components/common/LoadingSkeleton'
import { PageHeader } from '@/components/common/PageHeader'
import { getSummary, getDecisionDistribution, getTopPolicies } from '@/services/analyticsApi'
import { listAudit } from '@/services/auditApi'
import type { AnalyticsSummary } from '@/types/analytics'
import type { AuditListItem } from '@/types/audit'
import { formatDateTime, formatMs, formatPercent } from '@/utils/formatters'

const COLORS = ['#16a34a', '#dc2626', '#d97706']

export function DashboardPage() {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null)
  const [distribution, setDistribution] = useState<Array<{ decision: string; count: number }>>([])
  const [topPolicies, setTopPolicies] = useState<Array<{ policy_name: string; trigger_count: number }>>([])
  const [audit, setAudit] = useState<AuditListItem[]>([])
  const [auditError, setAuditError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function load() {
      setLoading(true)
      const [summaryResult, distributionResult, topResult, auditResult] = await Promise.allSettled([
        getSummary(),
        getDecisionDistribution(),
        getTopPolicies(),
        listAudit(),
      ])

      if (summaryResult.status === 'fulfilled') {
        setSummary(summaryResult.value as AnalyticsSummary)
        setError(null)
      } else {
        setError(
          summaryResult.reason instanceof Error
            ? summaryResult.reason.message
            : 'Failed to load dashboard',
        )
      }

      if (distributionResult.status === 'fulfilled') {
        setDistribution(distributionResult.value as typeof distribution)
      }
      if (topResult.status === 'fulfilled') {
        setTopPolicies(topResult.value as typeof topPolicies)
      }
      if (auditResult.status === 'fulfilled') {
        setAudit((auditResult.value as { items: AuditListItem[] }).items)
        setAuditError(null)
      } else {
        setAudit([])
        setAuditError(
          auditResult.reason instanceof Error ? auditResult.reason.message : 'Audit unavailable',
        )
      }

      setLoading(false)
    }
    load()
  }, [])

  if (loading) return <PageSkeleton />
  if (error) return <ErrorState message={error} onRetry={() => window.location.reload()} />
  if (!summary) return null

  return (
    <div>
      <PageHeader
        title="Decision Automation Overview"
        subtitle="Monitor policy activity, decision outcomes, performance, and governance."
        actions={
          <>
            <Link to="/policies/new" className="rounded-lg bg-brand px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">
              Create Policy
            </Link>
            <Link to="/decisions" className="rounded-lg border border-border bg-surface px-4 py-2 text-sm font-medium hover:bg-surface-muted">
              Evaluate Customer
            </Link>
          </>
        }
      />

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <StatCard label="Total Policies" value={summary.policies.total} />
        <StatCard label="Active Policies" value={summary.policies.active} />
        <StatCard label="Total Decisions" value={summary.decisions.total} />
        <StatCard label="Approval Rate" value={formatPercent(summary.decisions.approval_rate)} />
        <StatCard label="Avg Confidence" value={`${summary.performance.average_decision_confidence}%`} />
        <StatCard label="Avg Latency" value={formatMs(summary.performance.average_total_latency_ms)} />
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
          <h2 className="mb-4 font-semibold">Decision Distribution</h2>
          {distribution.length === 0 ? (
            <EmptyState title="No decision data yet" />
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie data={distribution} dataKey="count" nameKey="decision" cx="50%" cy="50%" outerRadius={80} label>
                  {distribution.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
          <h2 className="mb-4 font-semibold">Top Triggered Policies</h2>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={topPolicies} layout="vertical" margin={{ left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis type="category" dataKey="policy_name" width={120} tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="trigger_count" fill="#2563eb" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-3">
        <div className="rounded-xl border border-border bg-surface p-5 shadow-sm lg:col-span-2">
          <h2 className="mb-4 font-semibold">Recent Activity</h2>
          {auditError ? (
            <ErrorState message={auditError} onRetry={() => window.location.reload()} />
          ) : (
            <div className="space-y-3">
              {audit.map((item) => (
              <div key={item.audit_id} className="flex items-start justify-between border-b border-border pb-3 last:border-0">
                <div>
                  <p className="text-sm font-medium">{item.summary}</p>
                  <p className="text-xs text-text-muted">{item.action} · {item.entity_type}</p>
                </div>
                <span className="text-xs text-text-muted">{formatDateTime(item.created_at)}</span>
              </div>
            ))}
            </div>
          )}
        </div>
        <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
          <h2 className="mb-4 font-semibold">Quality Indicators</h2>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between"><span>Validation errors</span><span className="font-medium">{summary.quality.validation_errors}</span></div>
            <div className="flex justify-between"><span>Conflicts detected</span><span className="font-medium">{summary.quality.conflicts_detected}</span></div>
            <div className="flex justify-between"><span>AI fallback count</span><span className="font-medium">{summary.quality.ai_fallback_count}</span></div>
          </div>
        </div>
      </div>
    </div>
  )
}
