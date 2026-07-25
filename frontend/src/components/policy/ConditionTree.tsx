import type {
  PolicyCondition,
  PolicyConditionGroup,
  PolicyConditionNode,
} from '@/types/policy'

function isConditionGroup(
  node: PolicyConditionNode,
): node is PolicyConditionGroup {
  return (
    'all' in node ||
    'any' in node
  )
}

function formatValue(value: unknown): string {
  if (typeof value === 'string') {
    return value
  }

  if (
    value === null ||
    value === undefined
  ) {
    return '—'
  }

  return JSON.stringify(value)
}

function ConditionRow({
  condition,
  index,
}: {
  condition: PolicyCondition
  index: number
}) {
  return (
    <div className="rounded-lg border border-border bg-white p-3">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="m-0 text-sm font-semibold text-text-primary">
            {condition.field}
          </p>

          <p className="mb-0 mt-1 text-xs text-text-muted">
            Condition {index + 1}
          </p>
        </div>

        <span className="rounded-full bg-blue-50 px-2.5 py-1 text-xs font-semibold text-brand">
          {condition.operator.replaceAll(
            '_',
            ' ',
          )}
        </span>
      </div>

      <div className="mt-3 rounded-md bg-surface-muted px-3 py-2">
        <p className="m-0 text-xs font-medium uppercase tracking-wide text-text-muted">
          Expected value
        </p>

        <p className="mb-0 mt-1 break-all text-sm font-medium text-text-secondary">
          {formatValue(condition.value)}
        </p>
      </div>
    </div>
  )
}

function ConditionNodeView({
  node,
  index,
  depth,
}: {
  node: PolicyConditionNode
  index: number
  depth: number
}) {
  if (!isConditionGroup(node)) {
    return (
      <ConditionRow
        condition={node}
        index={index}
      />
    )
  }

  const mode = node.all
    ? 'ALL'
    : 'ANY'

  const children =
    node.all ??
    node.any ??
    []

  return (
    <section
      className={
        depth === 0
          ? 'space-y-3'
          : 'rounded-xl border border-border bg-surface-muted p-4'
      }
    >
      <div className="flex items-center gap-2">
        <span className="rounded-full bg-slate-200 px-2.5 py-1 text-xs font-bold text-slate-700">
          {mode}
        </span>

        <p className="m-0 text-xs text-text-muted">
          {mode === 'ALL'
            ? 'Every nested condition must match'
            : 'At least one nested condition must match'}
        </p>
      </div>

      <div className="space-y-3">
        {children.map(
          (child, childIndex) => (
            <ConditionNodeView
              key={`${depth}-${childIndex}`}
              node={child}
              index={childIndex}
              depth={depth + 1}
            />
          ),
        )}
      </div>
    </section>
  )
}

export function ConditionTree({
  conditions,
}: {
  conditions: PolicyConditionGroup
}) {
  const root: PolicyConditionNode =
    conditions

  return (
    <ConditionNodeView
      node={root}
      index={0}
      depth={0}
    />
  )
}
