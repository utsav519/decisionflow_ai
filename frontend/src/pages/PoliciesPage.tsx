import {
  useEffect,
  useState,
} from 'react'
import {
  ChevronLeft,
  ChevronRight,
  FileText,
  Plus,
  RefreshCw,
  Search,
} from 'lucide-react'
import { Link } from 'react-router-dom'

import {
  getApiErrorMessage,
} from '@/api/client'
import {
  listPolicies,
} from '@/services/policyApi'
import type {
  PaginationMeta,
} from '@/types/api'
import type {
  PolicyDecision,
  PolicyListItem,
  PolicyStatus,
} from '@/types/policy'

const emptyPagination: PaginationMeta = {
  page: 1,
  page_size: 20,
  total_items: 0,
  total_pages: 1,
}

const statusClasses: Record<
  PolicyStatus,
  string
> = {
  DRAFT:
    'bg-slate-100 text-slate-700',
  PENDING_APPROVAL:
    'bg-amber-100 text-amber-800',
  ACTIVE:
    'bg-green-100 text-green-800',
  DISABLED:
    'bg-red-100 text-red-800',
  ARCHIVED:
    'bg-zinc-100 text-zinc-700',
}

const decisionClasses: Record<
  PolicyDecision,
  string
> = {
  APPROVE:
    'bg-green-50 text-green-700',
  REJECT:
    'bg-red-50 text-red-700',
  MANUAL_REVIEW:
    'bg-orange-50 text-orange-700',
}

function formatDateTime(
  value: string,
): string {
  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return value
  }

  return new Intl.DateTimeFormat(
    'en-IN',
    {
      dateStyle: 'medium',
      timeStyle: 'short',
    },
  ).format(date)
}

export function PoliciesPage() {
  const [policies, setPolicies] =
    useState<PolicyListItem[]>([])

  const [pagination, setPagination] =
    useState<PaginationMeta>(
      emptyPagination,
    )

  const [search, setSearch] =
    useState('')

  const [status, setStatus] =
    useState<PolicyStatus | ''>('')

  const [decision, setDecision] =
    useState<PolicyDecision | ''>('')

  const [domain, setDomain] =
    useState('')

  const [page, setPage] =
    useState(1)

  const [refreshKey, setRefreshKey] =
    useState(0)

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState<string | null>(null)

  useEffect(() => {
    let active = true

    const timer = window.setTimeout(() => {
      void listPolicies({
        page,
        page_size: 20,
        search: search.trim() || undefined,
        status,
        decision,
        domain: domain.trim() || undefined,
        sort_by: 'created_at',
        sort_order: 'desc',
      })
        .then((result) => {
          if (!active) {
            return
          }

          setPolicies(result.items)
          setPagination(result.pagination)
          setError(null)
        })
        .catch((requestError: unknown) => {
          if (!active) {
            return
          }

          setError(
            getApiErrorMessage(
              requestError,
            ),
          )
        })
        .finally(() => {
          if (active) {
            setLoading(false)
          }
        })
    }, 250)

    return () => {
      active = false
      window.clearTimeout(timer)
    }
  }, [
    page,
    search,
    status,
    decision,
    domain,
    refreshKey,
  ])

  function reloadFromFirstPage(): void {
    setLoading(true)
    setPage(1)
    setRefreshKey(
      (current) => current + 1,
    )
  }

  return (
    <section className="p-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-7 flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="mb-2 text-xs font-bold uppercase tracking-[0.16em] text-brand">
              Policy Governance
            </p>

            <h1 className="m-0 text-3xl font-bold tracking-tight text-text-primary">
              Policies
            </h1>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-text-secondary">
              Search, filter and review the
              deterministic policies available
              to the DecisionFlow engine.
            </p>
          </div>

          <div className="flex gap-3">
            <button
              type="button"
              onClick={reloadFromFirstPage}
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

            <Link
              to="/policies/new"
              className="inline-flex items-center gap-2 rounded-lg bg-brand px-4 py-2.5 text-sm font-semibold text-white no-underline hover:bg-blue-700"
            >
              <Plus className="h-4 w-4" />
              Create policy
            </Link>
          </div>
        </header>

        <div className="mb-5 grid gap-3 rounded-xl border border-border bg-surface p-4 shadow-sm md:grid-cols-2 xl:grid-cols-[2fr_1fr_1fr_1fr]">
          <label className="relative">
            <span className="sr-only">
              Search policies
            </span>

            <Search className="pointer-events-none absolute left-3 top-3 h-4 w-4 text-text-muted" />

            <input
              type="search"
              value={search}
              onChange={(event) => {
                setLoading(true)
                setPage(1)
                setSearch(event.target.value)
              }}
              placeholder="Search by policy name"
              className="w-full rounded-lg border border-border bg-white py-2.5 pl-9 pr-3 text-sm outline-none focus:border-brand"
            />
          </label>

          <select
            value={status}
            onChange={(event) => {
              setLoading(true)
              setPage(1)
              setStatus(
                event.target.value as
                  | PolicyStatus
                  | '',
              )
            }}
            className="rounded-lg border border-border bg-white px-3 py-2.5 text-sm outline-none focus:border-brand"
          >
            <option value="">
              All statuses
            </option>
            <option value="ACTIVE">
              Active
            </option>
            <option value="DRAFT">
              Draft
            </option>
            <option value="PENDING_APPROVAL">
              Pending approval
            </option>
            <option value="DISABLED">
              Disabled
            </option>
            <option value="ARCHIVED">
              Archived
            </option>
          </select>

          <select
            value={decision}
            onChange={(event) => {
              setLoading(true)
              setPage(1)
              setDecision(
                event.target.value as
                  | PolicyDecision
                  | '',
              )
            }}
            className="rounded-lg border border-border bg-white px-3 py-2.5 text-sm outline-none focus:border-brand"
          >
            <option value="">
              All decisions
            </option>
            <option value="APPROVE">
              Approve
            </option>
            <option value="REJECT">
              Reject
            </option>
            <option value="MANUAL_REVIEW">
              Manual review
            </option>
          </select>

          <input
            type="text"
            value={domain}
            onChange={(event) => {
              setLoading(true)
              setPage(1)
              setDomain(event.target.value)
            }}
            placeholder="Domain, e.g. telecom"
            className="rounded-lg border border-border bg-white px-3 py-2.5 text-sm outline-none focus:border-brand"
          />
        </div>

        {error && (
          <div className="mb-5 rounded-xl border border-red-200 bg-red-50 p-5">
            <p className="m-0 font-semibold text-red-800">
              Policies could not be loaded
            </p>

            <p className="mb-0 mt-2 text-sm text-red-700">
              {error}
            </p>
          </div>
        )}

        <div className="overflow-hidden rounded-xl border border-border bg-surface shadow-sm">
          <div className="flex items-center justify-between border-b border-border px-5 py-4">
            <div>
              <h2 className="m-0 text-base font-bold text-text-primary">
                Policy Repository
              </h2>

              <p className="mb-0 mt-1 text-xs text-text-muted">
                {pagination.total_items}{' '}
                policies found
              </p>
            </div>

            <FileText className="h-5 w-5 text-text-muted" />
          </div>

          {loading && policies.length === 0 ? (
            <div className="space-y-3 p-5">
              {[1, 2, 3, 4, 5].map(
                (item) => (
                  <div
                    key={item}
                    className="h-16 animate-pulse rounded-lg bg-surface-muted"
                  />
                ),
              )}
            </div>
          ) : policies.length === 0 ? (
            <div className="p-12 text-center">
              <FileText className="mx-auto h-10 w-10 text-text-muted" />

              <p className="mb-0 mt-4 font-semibold text-text-primary">
                No policies found
              </p>

              <p className="mb-0 mt-2 text-sm text-text-muted">
                Change the filters or create
                a new policy.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full border-collapse text-left">
                <thead>
                  <tr className="border-b border-border bg-surface-muted text-xs uppercase tracking-wide text-text-muted">
                    <th className="px-5 py-3 font-semibold">
                      Policy
                    </th>
                    <th className="px-5 py-3 font-semibold">
                      Status
                    </th>
                    <th className="px-5 py-3 font-semibold">
                      Decision
                    </th>
                    <th className="px-5 py-3 font-semibold">
                      Priority
                    </th>
                    <th className="px-5 py-3 font-semibold">
                      Version
                    </th>
                    <th className="px-5 py-3 font-semibold">
                      Updated
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {policies.map(
                    (policy) => (
                      <tr
                        key={policy.id}
                        className="border-b border-border last:border-b-0 hover:bg-surface-muted"
                      >
                        <td className="px-5 py-4">
                          <Link
                            to={`/policies/${encodeURIComponent(policy.id)}`}
                            className="font-semibold text-text-primary no-underline hover:text-brand"
                          >
                            {policy.name}
                          </Link>

                          <p className="mb-0 mt-1 text-xs text-text-muted">
                            {policy.domain}
                            {' · '}
                            {policy.id}
                          </p>
                        </td>

                        <td className="px-5 py-4">
                          <span
                            className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ${statusClasses[policy.status]}`}
                          >
                            {policy.status.replaceAll(
                              '_',
                              ' ',
                            )}
                          </span>
                        </td>

                        <td className="px-5 py-4">
                          <span
                            className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ${decisionClasses[policy.decision]}`}
                          >
                            {policy.decision.replaceAll(
                              '_',
                              ' ',
                            )}
                          </span>
                        </td>

                        <td className="px-5 py-4 text-sm font-semibold text-text-primary">
                          {policy.priority}
                        </td>

                        <td className="px-5 py-4 text-sm text-text-secondary">
                          v{policy.version}
                        </td>

                        <td className="px-5 py-4 text-sm text-text-secondary">
                          {formatDateTime(
                            policy.updated_at,
                          )}
                        </td>
                      </tr>
                    ),
                  )}
                </tbody>
              </table>
            </div>
          )}

          <footer className="flex flex-wrap items-center justify-between gap-4 border-t border-border px-5 py-4">
            <p className="m-0 text-sm text-text-muted">
              Page {pagination.page} of{' '}
              {pagination.total_pages}
            </p>

            <div className="flex gap-2">
              <button
                type="button"
                disabled={
                  loading ||
                  page <= 1
                }
                onClick={() => {
                  setLoading(true)
                  setPage(
                    (current) =>
                      Math.max(
                        1,
                        current - 1,
                      ),
                  )
                }}
                className="inline-flex items-center gap-1 rounded-lg border border-border px-3 py-2 text-sm font-semibold text-text-primary hover:bg-surface-muted disabled:cursor-not-allowed disabled:opacity-40"
              >
                <ChevronLeft className="h-4 w-4" />
                Previous
              </button>

              <button
                type="button"
                disabled={
                  loading ||
                  page >=
                    pagination.total_pages
                }
                onClick={() => {
                  setLoading(true)
                  setPage(
                    (current) =>
                      current + 1,
                  )
                }}
                className="inline-flex items-center gap-1 rounded-lg border border-border px-3 py-2 text-sm font-semibold text-text-primary hover:bg-surface-muted disabled:cursor-not-allowed disabled:opacity-40"
              >
                Next
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>
          </footer>
        </div>
      </div>
    </section>
  )
}
