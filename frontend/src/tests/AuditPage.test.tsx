import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { AuditPage } from '@/pages/AuditPage'
import * as auditApi from '@/services/auditApi'
import { mockAuditList } from '@/mocks/audit'
import { renderWithProviders, screen, userEvent, waitFor } from '@/tests/test-utils'

describe('AuditPage', () => {
  beforeEach(() => {
    vi.spyOn(auditApi, 'listAudit').mockResolvedValue({
      items: mockAuditList,
      meta: { page: 1, page_size: 10, total_items: mockAuditList.length, total_pages: 1 },
    })
    vi.spyOn(auditApi, 'getAuditDetail').mockImplementation(async (id) => ({
      ...mockAuditList.find((item) => item.audit_id === id)!,
      request_snapshot: { customer_id: 'CUST-1001' },
      result_snapshot: { decision: 'APPROVE' },
    }))
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders audit rows', async () => {
    renderWithProviders(<AuditPage />)

    expect(await screen.findByText('POLICY_ACTIVATED')).toBeInTheDocument()
  })

  it('opens audit detail panel', async () => {
    const user = userEvent.setup()
    renderWithProviders(<AuditPage />)

    await user.click(screen.getAllByRole('button', { name: /^view$/i })[0]!)

    expect(await screen.findByText(/audit detail/i)).toBeInTheDocument()
    expect(screen.getByText(/cor_demo001/i)).toBeInTheDocument()
  })

  it('shows copy button for correlation id in detail', async () => {
    const user = userEvent.setup()
    renderWithProviders(<AuditPage />)

    await user.click(screen.getAllByRole('button', { name: /^view$/i })[0]!)

    expect(await screen.findByRole('button', { name: /copy id/i })).toBeInTheDocument()
  })

  it('loads audit list on mount', async () => {
    renderWithProviders(<AuditPage />)

    await waitFor(() => {
      expect(auditApi.listAudit).toHaveBeenCalled()
    })
  })
})
