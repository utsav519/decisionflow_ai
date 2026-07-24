import { useEffect, useState } from 'react'
import { CopyButton } from '@/components/common/CopyButton'
import { ErrorState } from '@/components/common/ErrorState'
import { JsonViewer } from '@/components/common/JsonViewer'
import { TableSkeleton } from '@/components/common/LoadingSkeleton'
import { PageHeader } from '@/components/common/PageHeader'
import { getAuditDetail, listAudit } from '@/services/auditApi'
import type { AuditDetail, AuditListItem } from '@/types/audit'
import { formatDateTime } from '@/utils/formatters'

export function AuditPage() {
  const [items, setItems] = useState<AuditListItem[]>([])
  const [selected, setSelected] = useState<AuditDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    listAudit()
      .then((data) => setItems((data as { items: AuditListItem[] }).items))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  async function viewDetail(auditId: string) {
    const detail = await getAuditDetail(auditId)
    setSelected(detail)
  }

  if (loading) return <TableSkeleton rows={5} />
  if (error) return <ErrorState message={error} />

  return (
    <div>
      <PageHeader title="Audit Logs" subtitle="Trace policy changes and decision evaluations." />

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="overflow-x-auto rounded-xl border border-border bg-surface shadow-sm">
          <table className="min-w-full text-sm">
            <thead className="border-b border-border bg-surface-muted text-left">
              <tr>
                <th className="px-4 py-3">Timestamp</th>
                <th className="px-4 py-3">Action</th>
                <th className="px-4 py-3">Summary</th>
                <th className="px-4 py-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.audit_id} className="border-b border-border">
                  <td className="px-4 py-3 text-xs">{formatDateTime(item.created_at)}</td>
                  <td className="px-4 py-3">{item.action}</td>
                  <td className="px-4 py-3">{item.summary}</td>
                  <td className="px-4 py-3">
                    <button type="button" onClick={() => viewDetail(item.audit_id)} className="text-brand hover:underline">
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
          {selected ? (
            <div className="space-y-3 text-sm">
              <h2 className="font-semibold">Audit Detail</h2>
              <p>ID: {selected.audit_id}</p>
              <p>Action: {selected.action}</p>
              <p>Entity: {selected.entity_type} / {selected.entity_id}</p>
              <p>Correlation: {selected.correlation_id} <CopyButton value={selected.correlation_id} label="Copy ID" /></p>
              <p>{selected.summary}</p>
              {selected.request_snapshot && (
                <div>
                  <p className="mb-1 font-medium">Request snapshot</p>
                  <JsonViewer data={selected.request_snapshot} />
                </div>
              )}
              {selected.result_snapshot && (
                <div>
                  <p className="mb-1 font-medium">Result snapshot</p>
                  <JsonViewer data={selected.result_snapshot} />
                </div>
              )}
            </div>
          ) : (
            <p className="py-20 text-center text-text-muted">Select an audit entry to view details.</p>
          )}
        </div>
      </div>
    </div>
  )
}

export function AuditDetailPage() {
  return (
    <div>
      <PageHeader backTo="/audit" backLabel="Back to Audit Logs" title="Audit Detail" />
      <p className="text-sm text-text-muted">Select an entry from the audit list to view full details.</p>
    </div>
  )
}
