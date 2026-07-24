import type { DecisionOutcome, PolicyStatus } from '@/types/policy'

export function decisionStyles(decision: DecisionOutcome | string) {
  switch (decision) {
    case 'APPROVE':
      return { bg: 'bg-green-100', text: 'text-green-800', border: 'border-green-200' }
    case 'REJECT':
      return { bg: 'bg-red-100', text: 'text-red-800', border: 'border-red-200' }
    case 'MANUAL_REVIEW':
      return { bg: 'bg-amber-100', text: 'text-amber-800', border: 'border-amber-200' }
    default:
      return { bg: 'bg-slate-100', text: 'text-slate-700', border: 'border-slate-200' }
  }
}

export function policyStatusStyles(status: PolicyStatus) {
  switch (status) {
    case 'ACTIVE':
      return { bg: 'bg-green-100', text: 'text-green-800' }
    case 'DRAFT':
      return { bg: 'bg-slate-100', text: 'text-slate-700' }
    case 'PENDING_APPROVAL':
      return { bg: 'bg-amber-100', text: 'text-amber-800' }
    case 'DISABLED':
    case 'ARCHIVED':
      return { bg: 'bg-slate-100', text: 'text-slate-500' }
    default:
      return { bg: 'bg-slate-100', text: 'text-slate-700' }
  }
}

export function confidenceLabel(score: number): string {
  if (score >= 90) return 'High confidence'
  if (score >= 70) return 'Review recommended'
  if (score >= 40) return 'Needs careful review'
  return 'Clarification required'
}
