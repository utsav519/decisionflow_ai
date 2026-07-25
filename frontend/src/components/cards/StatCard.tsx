import type {
  LucideIcon,
} from 'lucide-react'

interface StatCardProps {
  title: string
  value: string | number
  description: string
  icon: LucideIcon
}

export function StatCard({
  title,
  value,
  description,
  icon: Icon,
}: StatCardProps) {
  return (
    <article className="rounded-xl border border-border bg-surface p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="m-0 text-sm font-medium text-text-secondary">
            {title}
          </p>

          <p className="mb-0 mt-3 text-3xl font-bold tracking-tight text-text-primary">
            {value}
          </p>
        </div>

        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-brand">
          <Icon className="h-5 w-5" />
        </div>
      </div>

      <p className="mb-0 mt-3 text-xs text-text-muted">
        {description}
      </p>
    </article>
  )
}
