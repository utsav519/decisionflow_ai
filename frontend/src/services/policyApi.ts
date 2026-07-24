import { env } from '@/config/env'
import { apiClient, mockDelay, unwrap } from '@/services/apiClient'
import { getPolicyStore, setPolicyStore } from '@/mocks/policies'
import type { PaginationMeta } from '@/types/api'
import type { Policy } from '@/types/policy'

export interface PolicyFilters {
  page?: number
  page_size?: number
  status?: string
  decision?: string
  source?: string
  search?: string
}

function filterPolicies(filters: PolicyFilters = {}) {
  let items = [...getPolicyStore()]
  if (filters.status) items = items.filter((p) => p.status === filters.status)
  if (filters.decision) items = items.filter((p) => p.decision === filters.decision)
  if (filters.source) items = items.filter((p) => p.source === filters.source)
  if (filters.search) {
    const q = filters.search.toLowerCase()
    items = items.filter((p) => p.name.toLowerCase().includes(q))
  }
  return items
}

export async function listPolicies(filters: PolicyFilters = {}) {
  if (env.useMockApi) {
    const items = filterPolicies(filters)
    const page = filters.page ?? 1
    const pageSize = filters.page_size ?? 10
    const start = (page - 1) * pageSize
    const paged = items.slice(start, start + pageSize)
    const meta: PaginationMeta = {
      page,
      page_size: pageSize,
      total_items: items.length,
      total_pages: Math.max(1, Math.ceil(items.length / pageSize)),
    }
    return mockDelay({ items: paged, meta })
  }
  return unwrap<{ items: Policy[]; meta: PaginationMeta }>(
    apiClient.get('/policies', { params: filters }),
  )
}

export async function getPolicy(policyId: string) {
  if (env.useMockApi) {
    const policy = getPolicyStore().find((p) => p.id === policyId)
    if (!policy) throw new Error('Policy not found')
    return mockDelay(policy)
  }
  return unwrap<Policy>(apiClient.get(`/policies/${policyId}`))
}

export async function createPolicy(payload: Partial<Policy>) {
  if (env.useMockApi) {
    const now = new Date().toISOString()
    const policy: Policy = {
      id: `pol_${Date.now()}`,
      name: payload.name ?? 'Untitled policy',
      description: payload.description,
      domain: payload.domain ?? 'telecom',
      status: 'DRAFT',
      priority: payload.priority ?? 100,
      decision: payload.decision ?? 'APPROVE',
      conditions: payload.conditions ?? { all: [] },
      reason: payload.reason,
      source: payload.source ?? 'AI_GENERATED',
      version: 1,
      ai_metadata: payload.ai_metadata,
      created_by: 'demo_user',
      created_at: now,
      updated_at: now,
    }
    setPolicyStore([policy, ...getPolicyStore()])
    return mockDelay(policy)
  }
  return unwrap<Policy>(apiClient.post('/policies', payload))
}

export async function activatePolicy(policyId: string, approvalComment?: string) {
  if (env.useMockApi) {
    const policies = getPolicyStore().map((p) =>
      p.id === policyId
        ? {
            ...p,
            status: 'ACTIVE' as const,
            approved_by: 'demo_user',
            activated_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          }
        : p,
    )
    setPolicyStore(policies)
    return mockDelay(policies.find((p) => p.id === policyId)!)
  }
  return unwrap<Policy>(
    apiClient.post(`/policies/${policyId}/activate`, { approval_comment: approvalComment }),
  )
}

export async function disablePolicy(policyId: string, reason?: string) {
  if (env.useMockApi) {
    const policies = getPolicyStore().map((p) =>
      p.id === policyId
        ? { ...p, status: 'DISABLED' as const, updated_at: new Date().toISOString() }
        : p,
    )
    setPolicyStore(policies)
    return mockDelay(policies.find((p) => p.id === policyId)!)
  }
  return unwrap<Policy>(apiClient.post(`/policies/${policyId}/disable`, { reason }))
}
