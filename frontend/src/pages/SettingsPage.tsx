import { env } from '@/config/env'
import { PageHeader } from '@/components/common/PageHeader'

export function SettingsPage() {
  return (
    <div>
      <PageHeader title="Settings" subtitle="Application and integration configuration (display only for POC)." />

      <div className="max-w-2xl rounded-xl border border-border bg-surface p-6 shadow-sm">
        <dl className="space-y-4 text-sm">
          <div className="flex justify-between border-b border-border pb-3">
            <dt className="text-text-secondary">Application</dt>
            <dd className="font-medium">{env.appName}</dd>
          </div>
          <div className="flex justify-between border-b border-border pb-3">
            <dt className="text-text-secondary">Environment</dt>
            <dd className="font-medium">Demo</dd>
          </div>
          <div className="flex justify-between border-b border-border pb-3">
            <dt className="text-text-secondary">API Base URL</dt>
            <dd className="font-medium">{env.apiBaseUrl}</dd>
          </div>
          <div className="flex justify-between border-b border-border pb-3">
            <dt className="text-text-secondary">Mock API Mode</dt>
            <dd className="font-medium">{env.useMockApi ? 'Enabled' : 'Disabled'}</dd>
          </div>
          <div className="flex justify-between border-b border-border pb-3">
            <dt className="text-text-secondary">Database</dt>
            <dd className="font-medium">MySQL (backend)</dd>
          </div>
          <div className="flex justify-between border-b border-border pb-3">
            <dt className="text-text-secondary">Default User</dt>
            <dd className="font-medium">{env.defaultUserId}</dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-text-secondary">Default Role</dt>
            <dd className="font-medium">{env.defaultUserRole}</dd>
          </div>
        </dl>
      </div>
    </div>
  )
}

export function NotFoundPage() {
  return (
    <div className="py-20 text-center">
      <h1 className="text-2xl font-semibold">Page not found</h1>
      <p className="mt-2 text-text-secondary">The page you requested does not exist.</p>
    </div>
  )
}

export function DecisionDetailPage() {
  return (
    <div>
      <PageHeader
        backTo="/decisions"
        backLabel="Back to Decision Center"
        title="Decision Detail"
        subtitle="Full persisted evaluation result."
      />
      <p className="text-sm text-text-muted">Connect to GET /api/v1/decisions/:id when backend is available.</p>
    </div>
  )
}
