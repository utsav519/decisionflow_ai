export function LoadingSkeleton({ rows = 3 }: { rows?: number }) {
  return (
    <div className="space-y-3" role="status" aria-busy="true" aria-label="Loading content">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="h-16 animate-pulse rounded-lg bg-slate-200" />
      ))}
    </div>
  )
}

export function StatCardSkeleton({ count = 3 }: { count?: number }) {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3" aria-busy="true" aria-label="Loading statistics">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="h-28 animate-pulse rounded-xl border border-border bg-slate-200" />
      ))}
    </div>
  )
}

export function ChartSkeleton() {
  return (
    <div
      className="h-60 animate-pulse rounded-xl border border-border bg-slate-200"
      aria-busy="true"
      aria-label="Loading chart"
    />
  )
}

export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div className="overflow-hidden rounded-xl border border-border" aria-busy="true" aria-label="Loading table">
      <div className="h-10 animate-pulse bg-slate-200" />
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="h-14 animate-pulse border-t border-border bg-slate-100" />
      ))}
    </div>
  )
}

export function PageSkeleton() {
  return (
    <div className="space-y-6" aria-busy="true" aria-label="Loading page">
      <div className="h-16 animate-pulse rounded-lg bg-slate-200" />
      <StatCardSkeleton count={6} />
      <div className="grid gap-6 lg:grid-cols-2">
        <ChartSkeleton />
        <ChartSkeleton />
      </div>
    </div>
  )
}
