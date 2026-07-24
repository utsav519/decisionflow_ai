import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { PoliciesPage } from '@/pages/PoliciesPage'
import * as policyApi from '@/services/policyApi'
import { mockPolicies, resetPolicyStore } from '@/mocks/policies'
import { renderWithProviders, screen, userEvent, waitFor } from '@/tests/test-utils'

describe('PoliciesPage', () => {
  beforeEach(() => {
    resetPolicyStore()
    vi.spyOn(policyApi, 'listPolicies').mockResolvedValue({
      items: mockPolicies,
      meta: { page: 1, page_size: 10, total_items: mockPolicies.length, total_pages: 1 },
    })
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders policy rows after loading', async () => {
    renderWithProviders(<PoliciesPage />)

    expect(await screen.findByText('Standard upgrade approval')).toBeInTheDocument()
    expect(screen.getByText('Fraud rejection')).toBeInTheDocument()
  })

  it('shows empty state when no policies returned', async () => {
    vi.mocked(policyApi.listPolicies).mockResolvedValue({
      items: [],
      meta: { page: 1, page_size: 10, total_items: 0, total_pages: 1 },
    })

    renderWithProviders(<PoliciesPage />)

    expect(await screen.findByText(/no policies found/i)).toBeInTheDocument()
  })

  it('calls listPolicies with search filter', async () => {
    const user = userEvent.setup()
    renderWithProviders(<PoliciesPage />)
    await screen.findByText('Standard upgrade approval')

    await user.type(screen.getByPlaceholderText(/search policies/i), 'fraud')

    await waitFor(() => {
      const calls = vi.mocked(policyApi.listPolicies).mock.calls
      expect(calls.at(-1)?.[0]).toEqual(expect.objectContaining({ search: 'fraud' }))
    })
  })

  it('calls listPolicies with status filter', async () => {
    const user = userEvent.setup()
    renderWithProviders(<PoliciesPage />)
    await screen.findByText('Standard upgrade approval')

    await user.selectOptions(screen.getByRole('combobox'), 'ACTIVE')

    await waitFor(() => {
      const calls = vi.mocked(policyApi.listPolicies).mock.calls
      expect(calls.at(-1)?.[0]).toEqual(expect.objectContaining({ status: 'ACTIVE' }))
    })
  })

  it('links each policy to its detail page', async () => {
    renderWithProviders(<PoliciesPage />)
    await screen.findByText('Standard upgrade approval')

    const viewLinks = screen.getAllByRole('link', { name: /view/i })
    expect(viewLinks[0]).toHaveAttribute('href', expect.stringContaining('/policies/'))
  })

  it('shows create policy action', async () => {
    renderWithProviders(<PoliciesPage />)
    expect(await screen.findByRole('link', { name: /create policy/i })).toHaveAttribute('href', '/policies/new')
  })
})
