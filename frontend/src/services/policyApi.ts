import {
  apiClient,
  unwrap,
} from '@/api/client'
import type {
  ApiSuccess,
  PaginationMeta,
} from '@/types/api'
import type {
  Policy,
  PolicyDecision,
  PolicyListItem,
  PolicyListResult,
  PolicySource,
  PolicyStatus,
} from '@/types/policy'

export interface PolicyFilters {
  page?: number
  page_size?: number
  status?: PolicyStatus | ''
  decision?: PolicyDecision | ''
  source?: PolicySource | ''
  domain?: string
  search?: string
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

function createDefaultPagination(
  filters: PolicyFilters,
  itemCount: number,
): PaginationMeta {
  return {
    page: filters.page ?? 1,
    page_size: filters.page_size ?? 20,
    total_items: itemCount,
    total_pages: 1,
  }
}

export async function listPolicies(
  filters: PolicyFilters = {},
): Promise<PolicyListResult> {
  const params = Object.fromEntries(
    Object.entries(filters).filter(
      ([, value]) =>
        value !== undefined &&
        value !== null &&
        value !== '',
    ),
  )

  const response = await apiClient.get<
    ApiSuccess<PolicyListItem[], PaginationMeta>
  >(
    '/policies',
    {
      params,
    },
  )

  return {
    items: response.data.data,
    pagination:
      response.data.meta ??
      createDefaultPagination(
        filters,
        response.data.data.length,
      ),
  }
}

export function getPolicy(
  policyId: string,
): Promise<Policy> {
  return unwrap(
    apiClient.get(
      `/policies/${encodeURIComponent(policyId)}`,
    ),
  )
}

export function activatePolicy(
  policyId: string,
  approvalComment?: string,
): Promise<Policy> {
  return unwrap(
    apiClient.post(
      `/policies/${encodeURIComponent(policyId)}/activate`,
      approvalComment
        ? {
            approval_comment: approvalComment,
          }
        : {},
    ),
  )
}

export function disablePolicy(
  policyId: string,
  reason?: string,
): Promise<Policy> {
  return unwrap(
    apiClient.post(
      `/policies/${encodeURIComponent(policyId)}/disable`,
      reason
        ? {
            reason,
          }
        : {},
    ),
  )
}
