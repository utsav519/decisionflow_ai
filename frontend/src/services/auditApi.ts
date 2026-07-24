import { env } from '@/config/env'
import { apiClient, mockDelay, unwrap } from '@/services/apiClient'
import { mockAuditDetails, mockAuditList } from '@/mocks/audit'
import type { AuditDetail } from '@/types/audit'

export async function listAudit(filters: Record<string, string | number> = {}) {
  if (env.useMockApi) {
    return mockDelay({ items: mockAuditList, meta: { page: 1, page_size: 10, total_items: mockAuditList.length, total_pages: 1 } })
  }
  return unwrap(apiClient.get('/audit', { params: filters }))
}

export async function getAuditDetail(auditId: string) {
  if (env.useMockApi) {
    const detail = mockAuditDetails[auditId]
    if (!detail) throw new Error('Audit not found')
    return mockDelay(detail)
  }
  return unwrap<AuditDetail>(apiClient.get(`/audit/${auditId}`))
}
