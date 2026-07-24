import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, Legend } from 'recharts'
import { StatCard } from '@/components/cards/StatCard'
import { ErrorState } from '@/components/common/ErrorState'
import { LoadingSkeleton } from '@/components/common/LoadingSkeleton'
import { PageHeader } from '@/components/common/PageHeader'
import { getSummary, getDecisionDistribution, getDecisionTrend, getTopPolicies } from '@/services/analyticsApi'
import type { AnalyticsSummary } from '@/types/analytics'
import { formatMs, formatPercent } from '@/utils/formatters'

export function AnalyticsPage() {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null)
  const [distribution, setDistribution] = useState<Array<{ decision: string; count: number }>>([])
  const [trend, setTrend] = useState<Array<Record<string, string | number>>>([])
  const [topPolicies, setTopPolicies] = useState<Array<{ policy_name: string; trigger_count: number }>>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([getSummary(), getDecisionDistribution(), getDecisionTrend(), getTopPolicies()])
      .then(([s, d, t, tp]) => {
        setSummary(s as AnalyticsSummary)
        setDistribution(d as typeof distribution)
        setTrend(t as typeof trend)
        setTopPolicies(tp as typeof topPolicies)
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSkeleton rows={6} />
  if (error) return <ErrorState message={error} />
  if (!summary) return null

  return (
    <div>
      <PageHeader title="Analytics" subtitle="Decision volume, outcome distribution, and platform performance." />

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Total Decisions" value={summary.decisions.total} />
        <StatCard label="Approval Rate" value={formatPercent(summary.decisions.approval_rate)} />
        <StatCard label="Rejection Rate" value={formatPercent(summary.decisions.rejection_rate)} />
        <StatCard label="Manual Review Rate" value={formatPercent(summary.decisions.manual_review_rate)} />
        <StatCard label="Avg Confidence" value={`${summary.performance.average_decision_confidence}%`} />
        <StatCard label="Avg Total Latency" value={formatMs(summary.performance.average_total_latency_ms)} />
        <StatCard label="P95 Latency" value={formatMs(summary.performance.p95_total_latency_ms)} />
        <StatCard label="Conflicts Detected" value={summary.quality.conflicts_detected} />
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
          <h2 className="mb-4 font-semibold">Decision Distribution</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={distribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="decision" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#2563eb" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
          <h2 className="mb-4 font-semibold">Decision Trend</h2>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={trend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" tick={{ fontSize: 11 }} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="approve" stroke="#16a34a" />
              <Line type="monotone" dataKey="reject" stroke="#dc2626" />
              <Line type="monotone" dataKey="manual_review" stroke="#d97706" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="rounded-xl border border-border bg-surface p-5 shadow-sm lg:col-span-2">
          <h2 className="mb-4 font-semibold">Top Triggered Policies</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={topPolicies} layout="vertical" margin={{ left: 30 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis type="category" dataKey="policy_name" width={160} tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="trigger_count" fill="#2563eb" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
