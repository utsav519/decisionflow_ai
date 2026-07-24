import type { ConditionGroup, ConditionNode } from '@/types/policy'
import { fieldLabel } from '@/utils/formatters'

function isGroup(node: ConditionNode): node is ConditionGroup {
  return 'all' in node || 'any' in node
}

function renderNode(node: ConditionNode, index: number) {
  if (isGroup(node)) {
    const type = node.all ? 'all' : 'any'
    const children = node.all ?? node.any ?? []
    return (
      <div key={index} className="rounded-lg border border-border bg-surface-muted p-3">
        <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-text-muted">
          {type === 'all' ? 'ALL conditions must match' : 'ANY of the following may match'}
        </p>
        <div className="space-y-2">{children.map((child, i) => renderNode(child, i))}</div>
      </div>
    )
  }

  return (
    <div key={index} className="flex items-start gap-3 rounded-md bg-white p-2">
      <span className="mt-0.5 text-xs font-medium text-text-muted">{index + 1}.</span>
      <div>
        <p className="font-medium">{fieldLabel(node.field)}</p>
        <p className="text-sm text-text-secondary">
          {node.operator.replaceAll('_', ' ')} {node.value !== undefined ? String(node.value) : ''}
        </p>
        <p className="text-xs text-text-muted">{node.field}</p>
      </div>
    </div>
  )
}

export function ConditionTree({ conditions }: { conditions: ConditionGroup }) {
  const nodes = conditions.all ?? conditions.any ?? []

  return (
    <div className="space-y-2">
      {nodes.length === 0 ? (
        <p className="text-sm text-text-muted">No conditions defined.</p>
      ) : (
        nodes.map((node, i) => renderNode(node, i))
      )}
    </div>
  )
}
