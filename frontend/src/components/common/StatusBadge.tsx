import { cn } from '@/utils/cn'
import { policyStatusStyles } from '@/utils/decisionStyles'
import type { PolicyStatus } from '@/types/policy'

export function StatusBadge({ status }: { status: PolicyStatus | string }) {
  const styles = policyStatusStyles(status as PolicyStatus)
  return (
    <span className={cn('inline-flex rounded-md px-2 py-0.5 text-xs font-medium', styles.bg, styles.text)}>
      {status.replace('_', ' ')}
    </span>
  )
}
