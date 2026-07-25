interface PlaceholderPageProps {
  title: string
  description: string
}

export function PlaceholderPage({
  title,
  description,
}: PlaceholderPageProps) {
  return (
    <section className="p-8">
      <div className="mx-auto max-w-5xl">
        <p className="mb-2 text-xs font-bold uppercase tracking-[0.16em] text-brand">
          DecisionFlow AI
        </p>

        <h1 className="m-0 text-3xl font-bold text-text-primary">
          {title}
        </h1>

        <p className="mt-3 max-w-2xl text-sm leading-7 text-text-secondary">
          {description}
        </p>

        <div className="mt-8 rounded-xl border border-dashed border-border bg-surface p-10 text-center shadow-sm">
          <p className="m-0 text-sm font-semibold text-text-primary">
            Page integration pending
          </p>

          <p className="mt-2 text-sm text-text-muted">
            The existing frontend implementation will be
            connected to the real backend API in the next
            integration stages.
          </p>
        </div>
      </div>
    </section>
  )
}
