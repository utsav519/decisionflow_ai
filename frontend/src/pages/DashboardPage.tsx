import {
  useCallback,
  useEffect,
  useMemo,
  useState,
} from 'react'
import {
  Activity,
  FileCheck2,
  Gauge,
  RefreshCw,
  Scale,
} from 'lucide-react'
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { Link } from 'react-router-dom'

import { getApiErrorMessage } from '@/api/client'
import { StatCard } from '@/components/cards/StatCard'
import { getAnalyticsDashboard } from '@/services/analyticsApi'
import type {
  AnalyticsDashboard,
} from '@/types/analytics'

const decisionColors = [
  '#16a34a',
  '#dc2626',
  '#d97706',
]

function formatConfidence(value: number): string {
  if (!Number.isFinite(value)) {
    return '0%'
  }

  return `${Math.round(value)}%`
}

function formatTrendDate(value: string): string {
  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return value
  }

  return new Intl.DateTimeFormat('en-IN', {
    day: '2-digit',
    month: 'short',
  }).format(date)
}

export function DashboardPage() {
  const [dashboard, setDashboard] =
    useState<AnalyticsDashboard | null>(null)

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState<string | null>(null)

  const loadDashboard = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)

      const result =
        await getAnalyticsDashboard()

      setDashboard(result)
    } catch (requestError) {
      setError(
        getApiErrorMessage(requestError),
      )
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    let active = true

    void getAnalyticsDashboard()
      .then((result) => {
        if (!active) {
          return
        }

        setDashboard(result)
        setError(null)
      })
      .catch((requestError: unknown) => {
        if (!active) {
          return
        }

        setError(
          getApiErrorMessage(requestError),
        )
      })
      .finally(() => {
        if (active) {
          setLoading(false)
        }
      })

    return () => {
      active = false
    }
  }, [])

  const distribution = useMemo(() => {
    if (!dashboard) {
      return []
    }

    return [
      {
        name: 'Approve',
        value: dashboard.distribution.approve,
      },
      {
        name: 'Reject',
        value: dashboard.distribution.reject,
      },
      {
        name: 'Manual Review',
        value:
          dashboard.distribution.manual_review,
      },
    ]
  }, [dashboard])

  const distributionTotal = useMemo(
    () =>
      distribution.reduce(
        (total, item) =>
          total + item.value,
        0,
      ),
    [distribution],
  )

  const evaluationTrend =
    dashboard?.trends.evaluations ?? []

  return (
    <section className="p-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="mb-2 text-xs font-bold uppercase tracking-[0.16em] text-brand">
              DecisionFlow AI
            </p>

            <h1 className="m-0 text-3xl font-bold tracking-tight text-text-primary">
              Decision Dashboard
            </h1>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-text-secondary">
              Live operational metrics from the
              deterministic decision engine and
              policy repository.
            </p>
          </div>

          <div className="flex gap-3">
            <Link
              to="/decisions"
              className="inline-flex items-center gap-2 rounded-lg bg-brand px-4 py-2.5 text-sm font-semibold text-white no-underline hover:bg-blue-700"
            >
              <Scale className="h-4 w-4" />
              Evaluate decision
            </Link>

            <button
              type="button"
              onClick={() => {
                void loadDashboard()
              }}
              disabled={loading}
              className="inline-flex items-center gap-2 rounded-lg border border-border bg-surface px-4 py-2.5 text-sm font-semibold text-text-primary hover:bg-surface-muted disabled:opacity-60"
            >
              <RefreshCw
                className={
                  loading
                    ? 'h-4 w-4 animate-spin'
                    : 'h-4 w-4'
                }
              />
              Refresh
            </button>
          </div>
        </header>

        {loading && !dashboard && (
          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
            {[1, 2, 3, 4].map((item) => (
              <div
                key={item}
                className="h-36 animate-pulse rounded-xl border border-border bg-surface"
              />
            ))}
          </div>
        )}

        {error && (
          <div className="mb-6 rounded-xl border border-red-200 bg-red-50 p-5">
            <p className="m-0 font-semibold text-red-800">
              Dashboard could not be loaded
            </p>

            <p className="mb-0 mt-2 text-sm text-red-700">
              {error}
            </p>
          </div>
        )}

        {dashboard && (
          <>
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
              <StatCard
                title="Total Policies"
                value={dashboard.summary.total_policies}
                description={`${dashboard.summary.active_policies} policies currently active`}
                icon={FileCheck2}
              />

              <StatCard
                title="Active Policies"
                value={dashboard.summary.active_policies}
                description="Policies available to the decision engine"
                icon={Activity}
              />

              <StatCard
                title="Total Evaluations"
                value={dashboard.summary.total_evaluations}
                description="Persisted decision evaluations"
                icon={Scale}
              />

              <StatCard
                title="Average Confidence"
                value={formatConfidence(
                  dashboard.summary.avg_confidence,
                )}
                description="Average confidence across evaluations"
                icon={Gauge}
              />
            </div>

            <div className="mt-6 grid gap-6 xl:grid-cols-[0.85fr_1.15fr]">
              <article className="rounded-xl border border-border bg-surface p-5 shadow-sm">
                <div>
                  <h2 className="m-0 text-lg font-bold text-text-primary">
                    Decision Distribution
                  </h2>

                  <p className="mt-1 text-sm text-text-muted">
                    Outcome distribution across all
                    persisted evaluations.
                  </p>
                </div>

                {distributionTotal === 0 ? (
                  <div className="flex h-72 items-center justify-center rounded-lg bg-surface-muted">
                    <p className="text-sm text-text-muted">
                      No decision evaluations recorded yet.
                    </p>
                  </div>
                ) : (
                  <div className="h-72">
                    <ResponsiveContainer
                      width="100%"
                      height="100%"
                    >
                      <PieChart>
                        <Pie
                          data={distribution}
                          dataKey="value"
                          nameKey="name"
                          innerRadius={62}
                          outerRadius={94}
                          paddingAngle={3}
                        >
                          {distribution.map(
                            (item, index) => (
                              <Cell
                                key={item.name}
                                fill={
                                  decisionColors[
                                    index %
                                      decisionColors.length
                                  ]
                                }
                              />
                            ),
                          )}
                        </Pie>

                        <Tooltip />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </article>

              <article className="rounded-xl border border-border bg-surface p-5 shadow-sm">
                <div>
                  <h2 className="m-0 text-lg font-bold text-text-primary">
                    Evaluation Trend
                  </h2>

                  <p className="mt-1 text-sm text-text-muted">
                    Total evaluations generated during
                    the previous 30 days.
                  </p>
                </div>

                {evaluationTrend.length === 0 ? (
                  <div className="flex h-72 items-center justify-center rounded-lg bg-surface-muted">
                    <p className="text-sm text-text-muted">
                      Trend data will appear after
                      evaluations are recorded.
                    </p>
                  </div>
                ) : (
                  <div className="h-72">
                    <ResponsiveContainer
                      width="100%"
                      height="100%"
                    >
                      <AreaChart
                        data={evaluationTrend}
                        margin={{
                          top: 16,
                          right: 12,
                          left: -20,
                          bottom: 0,
                        }}
                      >
                        <CartesianGrid
                          strokeDasharray="3 3"
                          vertical={false}
                        />

                        <XAxis
                          dataKey="date"
                          tickFormatter={formatTrendDate}
                          fontSize={11}
                        />

                        <YAxis
                          allowDecimals={false}
                          fontSize={11}
                        />

                        <Tooltip
                          labelFormatter={(label) =>
                            formatTrendDate(
                              String(label ?? ''),
                            )
                          }
                        />

                        <Area
                          type="monotone"
                          dataKey="count"
                          name="Evaluations"
                          stroke="#2563eb"
                          fill="#dbeafe"
                          strokeWidth={2}
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </article>
            </div>

            <div className="mt-6 grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
              <article className="rounded-xl border border-border bg-surface p-5 shadow-sm">
                <div>
                  <h2 className="m-0 text-lg font-bold text-text-primary">
                    Top Matching Policies
                  </h2>

                  <p className="mt-1 text-sm text-text-muted">
                    Policies responsible for the most
                    matched evaluations.
                  </p>
                </div>

                {dashboard.top_policies.length === 0 ? (
                  <div className="mt-5 rounded-lg bg-surface-muted p-10 text-center">
                    <p className="m-0 text-sm text-text-muted">
                      No policy matches recorded yet.
                    </p>
                  </div>
                ) : (
                  <div className="mt-4 h-72">
                    <ResponsiveContainer
                      width="100%"
                      height="100%"
                    >
                      <BarChart
                        data={dashboard.top_policies}
                        layout="vertical"
                        margin={{
                          top: 8,
                          right: 20,
                          left: 18,
                          bottom: 8,
                        }}
                      >
                        <CartesianGrid
                          strokeDasharray="3 3"
                          horizontal={false}
                        />

                        <XAxis
                          type="number"
                          allowDecimals={false}
                        />

                        <YAxis
                          type="category"
                          dataKey="name"
                          width={150}
                          fontSize={11}
                        />

                        <Tooltip />

                        <Bar
                          dataKey="match_count"
                          name="Matches"
                          fill="#2563eb"
                          radius={[0, 5, 5, 0]}
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </article>

              <article className="rounded-xl border border-border bg-surface p-5 shadow-sm">
                <h2 className="m-0 text-lg font-bold text-text-primary">
                  Policy Status
                </h2>

                <p className="mt-1 text-sm text-text-muted">
                  Current policy lifecycle breakdown.
                </p>

                <div className="mt-5 space-y-3">
                  {Object.entries(
                    dashboard.summary
                      .policy_status_breakdown ?? {},
                  ).map(([status, count]) => (
                    <div
                      key={status}
                      className="flex items-center justify-between rounded-lg border border-border px-4 py-3"
                    >
                      <span className="text-sm font-medium text-text-secondary">
                        {status.replaceAll('_', ' ')}
                      </span>

                      <span className="rounded-full bg-surface-muted px-3 py-1 text-sm font-bold text-text-primary">
                        {count}
                      </span>
                    </div>
                  ))}

                  {Object.keys(
                    dashboard.summary
                      .policy_status_breakdown ?? {},
                  ).length === 0 && (
                    <p className="rounded-lg bg-surface-muted p-6 text-center text-sm text-text-muted">
                      Policy status metrics unavailable.
                    </p>
                  )}
                </div>
              </article>
            </div>
          </>
        )}
      </div>
    </section>
  )
}
