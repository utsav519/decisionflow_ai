import { cn } from '@/utils/cn'
import { decisionStyles } from '@/utils/decisionStyles'
import type { DecisionOutcome } from '@/types/policy'

export function DecisionBadge({ decision }: { decision: DecisionOutcome | string }) {
  const styles = decisionStyles(decision)
  const label = decision === 'MANUAL_REVIEW' ? 'MANUAL REVIEW' : decision.replace('_', ' ')
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold uppercase tracking-wide',
        styles.bg,
        styles.text,
        styles.border,
      )}
    >
      {label}
    </span>
  )
}
