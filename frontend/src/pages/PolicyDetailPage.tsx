import {
  useEffect,
  useState,
} from 'react'
import {
  ArrowLeft,
  CheckCircle2,
  Clock3,
  FileCode2,
  Power,
  RefreshCw,
  ShieldCheck,
  UserRound,
} from 'lucide-react'
import {
  Link,
  useParams,
} from 'react-router-dom'

import {
  getApiErrorMessage,
} from '@/api/client'
import {
  ConditionTree,
} from '@/components/policy/ConditionTree'
import {
  activatePolicy,
  disablePolicy,
  getPolicy,
} from '@/services/policyApi'
import type {
  Policy,
  PolicyDecision,
  PolicyStatus,
} from '@/types/policy'

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
  value?: string | null,
): string {
  if (!value) {
    return '—'
  }

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

function MetadataItem({
  label,
  value,
}: {
  label: string
  value: string | number
}) {
  return (
    <div className="rounded-lg border border-border bg-surface-muted p-4">
      <p className="m-0 text-xs font-semibold uppercase tracking-wide text-text-muted">
        {label}
      </p>

      <p className="mb-0 mt-2 break-all text-sm font-semibold text-text-primary">
        {value}
      </p>
    </div>
  )
}

export function PolicyDetailPage() {
  const { policyId } = useParams<{
    policyId: string
  }>()

  const [policy, setPolicy] =
    useState<Policy | null>(null)

  const [loading, setLoading] =
    useState(true)

  const [actionLoading, setActionLoading] =
    useState(false)

  const [error, setError] =
    useState<string | null>(null)

  const [actionMessage, setActionMessage] =
    useState<string | null>(null)

  const [actionNote, setActionNote] =
    useState('')

  useEffect(() => {
    if (!policyId) {
      return
    }

    let active = true

    void getPolicy(policyId)
      .then((result) => {
        if (!active) {
          return
        }

        setPolicy(result)
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

    return () => {
      active = false
    }
  }, [policyId])

  async function refreshPolicy(): Promise<void> {
    if (!policyId) {
      return
    }

    try {
      setLoading(true)
      setError(null)

      const result =
        await getPolicy(policyId)

      setPolicy(result)
    } catch (requestError) {
      setError(
        getApiErrorMessage(
          requestError,
        ),
      )
    } finally {
      setLoading(false)
    }
  }

  async function handleActivate(): Promise<void> {
    if (!policy) {
      return
    }

    const confirmed = window.confirm(
      `Activate policy "${policy.name}"?\n\n` +
      'The policy will become available to the decision engine.',
    )

    if (!confirmed) {
      return
    }

    try {
      setActionLoading(true)
      setError(null)
      setActionMessage(null)

      const updated =
        await activatePolicy(
          policy.id,
          actionNote.trim() || undefined,
        )

      setPolicy(updated)
      setActionNote('')
      setActionMessage(
        'Policy activated successfully.',
      )
    } catch (requestError) {
      setError(
        getApiErrorMessage(
          requestError,
        ),
      )
    } finally {
      setActionLoading(false)
    }
  }

  async function handleDisable(): Promise<void> {
    if (!policy) {
      return
    }

    const confirmed = window.confirm(
      `Disable policy "${policy.name}"?\n\n` +
      'The policy will no longer participate in new decisions.',
    )

    if (!confirmed) {
      return
    }

    try {
      setActionLoading(true)
      setError(null)
      setActionMessage(null)

      const updated =
        await disablePolicy(
          policy.id,
          actionNote.trim() || undefined,
        )

      setPolicy(updated)
      setActionNote('')
      setActionMessage(
        'Policy disabled successfully.',
      )
    } catch (requestError) {
      setError(
        getApiErrorMessage(
          requestError,
        ),
      )
    } finally {
      setActionLoading(false)
    }
  }

  const displayedError =
    policyId
      ? error
      : 'Policy ID is missing.'

  const canActivate =
    policy?.status === 'DRAFT' ||
    policy?.status === 'DISABLED'

  const canDisable =
    policy?.status === 'ACTIVE'

  return (
    <section className="p-8">
      <div className="mx-auto max-w-7xl">
        <Link
          to="/policies"
          className="mb-5 inline-flex items-center gap-2 text-sm font-semibold text-text-secondary no-underline hover:text-brand"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to policies
        </Link>

        {loading && !policy && policyId && (
          <div className="space-y-5">
            <div className="h-32 animate-pulse rounded-xl bg-surface" />
            <div className="h-72 animate-pulse rounded-xl bg-surface" />
          </div>
        )}

        {displayedError && (
          <div className="mb-6 rounded-xl border border-red-200 bg-red-50 p-5">
            <p className="m-0 font-semibold text-red-800">
              Policy request failed
            </p>

            <p className="mb-0 mt-2 text-sm text-red-700">
              {displayedError}
            </p>

            <button
              type="button"
              onClick={() => {
                void refreshPolicy()
              }}
              className="mt-4 inline-flex items-center gap-2 rounded-lg border border-red-300 bg-white px-3 py-2 text-sm font-semibold text-red-800"
            >
              <RefreshCw className="h-4 w-4" />
              Retry
            </button>
          </div>
        )}

        {actionMessage && (
          <div className="mb-6 flex items-center gap-3 rounded-xl border border-green-200 bg-green-50 p-4 text-sm font-semibold text-green-800">
            <CheckCircle2 className="h-5 w-5" />
            {actionMessage}
          </div>
        )}

        {policy && (
          <>
            <header className="mb-6 rounded-xl border border-border bg-surface p-6 shadow-sm">
              <div className="flex flex-wrap items-start justify-between gap-5">
                <div>
                  <p className="mb-2 text-xs font-bold uppercase tracking-[0.16em] text-brand">
                    Policy Detail
                  </p>

                  <h1 className="m-0 text-3xl font-bold tracking-tight text-text-primary">
                    {policy.name}
                  </h1>

                  <p className="mt-3 max-w-3xl text-sm leading-6 text-text-secondary">
                    {policy.description ||
                      'No policy description provided.'}
                  </p>

                  <div className="mt-4 flex flex-wrap gap-2">
                    <span
                      className={`rounded-full px-3 py-1 text-xs font-semibold ${statusClasses[policy.status]}`}
                    >
                      {policy.status.replaceAll(
                        '_',
                        ' ',
                      )}
                    </span>

                    <span
                      className={`rounded-full px-3 py-1 text-xs font-semibold ${decisionClasses[policy.decision]}`}
                    >
                      {policy.decision.replaceAll(
                        '_',
                        ' ',
                      )}
                    </span>

                    <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-brand">
                      {policy.domain}
                    </span>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() => {
                    void refreshPolicy()
                  }}
                  disabled={
                    loading ||
                    actionLoading
                  }
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

            <div className="grid gap-6 xl:grid-cols-[1.55fr_0.85fr]">
              <div className="space-y-6">
                <article className="rounded-xl border border-border bg-surface p-6 shadow-sm">
                  <div className="mb-5 flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-brand">
                      <FileCode2 className="h-5 w-5" />
                    </div>

                    <div>
                      <h2 className="m-0 text-lg font-bold text-text-primary">
                        Policy Conditions
                      </h2>

                      <p className="mb-0 mt-1 text-sm text-text-muted">
                        Deterministic condition tree
                        evaluated by the rule engine.
                      </p>
                    </div>
                  </div>

                  <ConditionTree
                    conditions={policy.conditions}
                  />
                </article>

                <article className="rounded-xl border border-border bg-surface p-6 shadow-sm">
                  <div className="mb-4 flex items-center gap-3">
                    <ShieldCheck className="h-5 w-5 text-brand" />

                    <h2 className="m-0 text-lg font-bold text-text-primary">
                      Decision Reason
                    </h2>
                  </div>

                  <p className="m-0 text-sm leading-7 text-text-secondary">
                    {policy.reason ||
                      'No decision reason provided.'}
                  </p>
                </article>

                {policy.ai_metadata && (
                  <article className="rounded-xl border border-border bg-surface p-6 shadow-sm">
                    <h2 className="m-0 text-lg font-bold text-text-primary">
                      AI Metadata
                    </h2>

                    <div className="mt-4 grid gap-3 md:grid-cols-2">
                      <MetadataItem
                        label="Generated by AI"
                        value={
                          policy.ai_metadata.generated
                            ? 'Yes'
                            : 'No'
                        }
                      />

                      <MetadataItem
                        label="AI confidence"
                        value={
                          policy.ai_metadata
                            .ai_confidence ??
                          '—'
                        }
                      />

                      <MetadataItem
                        label="Model"
                        value={
                          policy.ai_metadata.model ??
                          '—'
                        }
                      />

                      <MetadataItem
                        label="Warnings"
                        value={
                          policy.ai_metadata
                            .warnings?.length ??
                          0
                        }
                      />
                    </div>
                  </article>
                )}
              </div>

              <aside className="space-y-6">
                <article className="rounded-xl border border-border bg-surface p-5 shadow-sm">
                  <h2 className="m-0 text-base font-bold text-text-primary">
                    Policy Metadata
                  </h2>

                  <div className="mt-4 grid gap-3">
                    <MetadataItem
                      label="Policy ID"
                      value={policy.id}
                    />

                    <MetadataItem
                      label="Version"
                      value={`v${policy.version}`}
                    />

                    <MetadataItem
                      label="Priority"
                      value={policy.priority}
                    />

                    <MetadataItem
                      label="Source"
                      value={policy.source.replaceAll(
                        '_',
                        ' ',
                      )}
                    />
                  </div>
                </article>

                <article className="rounded-xl border border-border bg-surface p-5 shadow-sm">
                  <div className="flex items-center gap-2">
                    <Clock3 className="h-4 w-4 text-brand" />

                    <h2 className="m-0 text-base font-bold text-text-primary">
                      Timeline
                    </h2>
                  </div>

                  <dl className="mt-4 space-y-4">
                    <div>
                      <dt className="text-xs font-semibold uppercase tracking-wide text-text-muted">
                        Created
                      </dt>
                      <dd className="m-0 mt-1 text-sm text-text-secondary">
                        {formatDateTime(
                          policy.created_at,
                        )}
                      </dd>
                    </div>

                    <div>
                      <dt className="text-xs font-semibold uppercase tracking-wide text-text-muted">
                        Updated
                      </dt>
                      <dd className="m-0 mt-1 text-sm text-text-secondary">
                        {formatDateTime(
                          policy.updated_at,
                        )}
                      </dd>
                    </div>

                    <div>
                      <dt className="text-xs font-semibold uppercase tracking-wide text-text-muted">
                        Activated
                      </dt>
                      <dd className="m-0 mt-1 text-sm text-text-secondary">
                        {formatDateTime(
                          policy.activated_at,
                        )}
                      </dd>
                    </div>

                    <div>
                      <dt className="text-xs font-semibold uppercase tracking-wide text-text-muted">
                        Disabled
                      </dt>
                      <dd className="m-0 mt-1 text-sm text-text-secondary">
                        {formatDateTime(
                          policy.disabled_at,
                        )}
                      </dd>
                    </div>
                  </dl>
                </article>

                <article className="rounded-xl border border-border bg-surface p-5 shadow-sm">
                  <div className="flex items-center gap-2">
                    <UserRound className="h-4 w-4 text-brand" />

                    <h2 className="m-0 text-base font-bold text-text-primary">
                      Ownership
                    </h2>
                  </div>

                  <div className="mt-4 space-y-4">
                    <MetadataItem
                      label="Created by"
                      value={
                        policy.created_by ??
                        '—'
                      }
                    />

                    <MetadataItem
                      label="Approved by"
                      value={
                        policy.approved_by ??
                        '—'
                      }
                    />
                  </div>
                </article>

                {(canActivate || canDisable) && (
                  <article className="rounded-xl border border-border bg-surface p-5 shadow-sm">
                    <h2 className="m-0 text-base font-bold text-text-primary">
                      Lifecycle Action
                    </h2>

                    <p className="mb-0 mt-2 text-sm leading-6 text-text-muted">
                      Add an optional approval comment
                      or disable reason before changing
                      policy status.
                    </p>

                    <textarea
                      value={actionNote}
                      onChange={(event) => {
                        setActionNote(
                          event.target.value,
                        )
                      }}
                      rows={3}
                      placeholder={
                        canActivate
                          ? 'Approval comment'
                          : 'Reason for disabling'
                      }
                      className="mt-4 w-full resize-y rounded-lg border border-border px-3 py-2 text-sm outline-none focus:border-brand"
                    />

                    {canActivate && (
                      <button
                        type="button"
                        onClick={() => {
                          void handleActivate()
                        }}
                        disabled={actionLoading}
                        className="mt-3 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-green-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-green-700 disabled:opacity-60"
                      >
                        <Power className="h-4 w-4" />
                        {actionLoading
                          ? 'Activating...'
                          : 'Activate policy'}
                      </button>
                    )}

                    {canDisable && (
                      <button
                        type="button"
                        onClick={() => {
                          void handleDisable()
                        }}
                        disabled={actionLoading}
                        className="mt-3 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-red-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-red-700 disabled:opacity-60"
                      >
                        <Power className="h-4 w-4" />
                        {actionLoading
                          ? 'Disabling...'
                          : 'Disable policy'}
                      </button>
                    )}
                  </article>
                )}
              </aside>
            </div>
          </>
        )}
      </div>
    </section>
  )
}
