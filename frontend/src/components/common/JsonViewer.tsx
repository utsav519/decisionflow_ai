import { CopyButton } from '@/components/common/CopyButton'

export function JsonViewer({ data, copyable = true }: { data: unknown; copyable?: boolean }) {
  const json = JSON.stringify(data, null, 2)

  return (
    <div className="relative">
      {copyable && (
        <div className="absolute right-2 top-2">
          <CopyButton value={json} label="Copy JSON" className="bg-slate-800 text-slate-100 border-slate-600" />
        </div>
      )}
      <pre className="overflow-auto rounded-lg bg-slate-900 p-4 pt-10 text-xs text-slate-100">{json}</pre>
    </div>
  )
}
