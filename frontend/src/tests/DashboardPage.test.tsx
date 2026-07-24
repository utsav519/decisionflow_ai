import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { DashboardPage } from '@/pages/DashboardPage'
import * as analyticsApi from '@/services/analyticsApi'
import * as auditApi from '@/services/auditApi'
import { mockAnalyticsSummary, mockDecisionDistribution, mockTopPolicies } from '@/mocks/analytics'
import { mockAuditList } from '@/mocks/audit'
import { renderWithProviders, screen, waitFor } from '@/tests/test-utils'

describe('DashboardPage', () => {
  beforeEach(() => {
    vi.spyOn(analyticsApi, 'getSummary').mockResolvedValue(mockAnalyticsSummary)
    vi.spyOn(analyticsApi, 'getDecisionDistribution').mockResolvedValue(mockDecisionDistribution)
    vi.spyOn(analyticsApi, 'getTopPolicies').mockResolvedValue(mockTopPolicies)
    vi.spyOn(auditApi, 'listAudit').mockResolvedValue({
      items: mockAuditList,
      meta: { page: 1, page_size: 5, total_items: mockAuditList.length, total_pages: 1 },
    })
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders summary statistic cards', async () => {
    renderWithProviders(<DashboardPage />)

    expect(await screen.findByText('Total Policies')).toBeInTheDocument()
    expect(screen.getByText('6')).toBeInTheDocument()
    expect(screen.getByText('Active Policies')).toBeInTheDocument()
    expect(screen.getByText('Approval Rate')).toBeInTheDocument()
  })

  it('renders recent audit activity', async () => {
    renderWithProviders(<DashboardPage />)

    expect(await screen.findByText(/Customer CUST-1001 evaluated/i)).toBeInTheDocument()
  })

  it('renders quality indicators', async () => {
    renderWithProviders(<DashboardPage />)

    expect(await screen.findByText('Conflicts detected')).toBeInTheDocument()
  })

  it('keeps page usable when one API fails', async () => {
    vi.mocked(auditApi.listAudit).mockRejectedValue(new Error('Audit unavailable'))
    renderWithProviders(<DashboardPage />)

    await waitFor(() => {
      expect(screen.getByText(/audit unavailable/i)).toBeInTheDocument()
    })
    expect(screen.getByText('Total Policies')).toBeInTheDocument()
  })
})
