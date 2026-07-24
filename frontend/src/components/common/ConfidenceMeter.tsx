import { confidenceLabel } from '@/utils/decisionStyles'

export function ConfidenceMeter({ score, label = 'AI confidence' }: { score: number; label?: string }) {
  const color =
    score >= 90 ? 'bg-green-500' : score >= 70 ? 'bg-blue-500' : score >= 40 ? 'bg-amber-500' : 'bg-red-500'

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-sm">
        <span className="text-text-secondary">{label}</span>
        <span className="font-semibold">{score}%</span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-slate-200">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${score}%` }} />
      </div>
      <p className="text-xs text-text-muted">{confidenceLabel(score)}</p>
    </div>
  )
}
