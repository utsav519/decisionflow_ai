import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { PolicyStudioPage } from '@/pages/PolicyStudioPage'
import * as aiApi from '@/services/aiApi'
import * as policyApi from '@/services/policyApi'
import { resetPolicyStore } from '@/mocks/policies'
import {
  ambiguousPolicyText,
  mockAmbiguousPolicyResult,
  mockGeneratedPolicyResult,
  validPolicyText,
} from '@/tests/fixtures/policy'
import { renderWithProviders, screen, userEvent, waitFor } from '@/tests/test-utils'

const navigateMock = vi.fn()

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom')
  return {
    ...actual,
    useNavigate: () => navigateMock,
  }
})

async function fillPolicyText(user: ReturnType<typeof userEvent.setup>, text: string) {
  const textarea = screen.getByLabelText(/describe your business policy/i)
  await user.clear(textarea)
  await user.click(textarea)
  await user.paste(text)
}

describe('PolicyStudioPage', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
    resetPolicyStore()
    vi.spyOn(aiApi, 'generatePolicy').mockImplementation(vi.fn())
    vi.spyOn(policyApi, 'createPolicy').mockImplementation(vi.fn())
    vi.spyOn(policyApi, 'activatePolicy').mockImplementation(vi.fn())
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('blocks empty policy text submission', async () => {
    const user = userEvent.setup()
    renderWithProviders(<PolicyStudioPage />)

    await user.click(screen.getByRole('button', { name: /generate policy/i }))

    expect(await screen.findByText(/enter a more detailed policy/i)).toBeInTheDocument()
    expect(aiApi.generatePolicy).not.toHaveBeenCalled()
  })

  it('blocks short policy text', async () => {
    const user = userEvent.setup()
    renderWithProviders(<PolicyStudioPage />)

    await user.type(screen.getByLabelText(/describe your business policy/i), 'Too short')
    await user.click(screen.getByRole('button', { name: /generate policy/i }))

    expect(await screen.findByText(/enter a more detailed policy/i)).toBeInTheDocument()
    expect(aiApi.generatePolicy).not.toHaveBeenCalled()
  })

  it('submits valid policy text to generate API', async () => {
    vi.mocked(aiApi.generatePolicy).mockResolvedValue(mockGeneratedPolicyResult)
    const user = userEvent.setup()
    renderWithProviders(<PolicyStudioPage />)

    await fillPolicyText(user, validPolicyText)
    await user.click(screen.getByRole('button', { name: /generate policy/i }))

    await waitFor(() => {
      expect(aiApi.generatePolicy).toHaveBeenCalledWith(
        expect.objectContaining({ policy_text: validPolicyText, domain: 'telecom' }),
      )
    })
  })

  it('shows loading skeleton while generating', async () => {
    vi.mocked(aiApi.generatePolicy).mockImplementation(() => new Promise(() => {}))
    const user = userEvent.setup()
    renderWithProviders(<PolicyStudioPage />)

    await fillPolicyText(user, validPolicyText)
    await user.click(screen.getByRole('button', { name: /generate policy/i }))

    expect(screen.getByRole('status', { name: /loading content/i })).toBeInTheDocument()
  })

  it('renders successful generated policy and AI confidence', async () => {
    vi.mocked(aiApi.generatePolicy).mockResolvedValue(mockGeneratedPolicyResult)
    const user = userEvent.setup()
    renderWithProviders(<PolicyStudioPage />)

    await fillPolicyText(user, validPolicyText)
    await user.click(screen.getByRole('button', { name: /generate policy/i }))

    expect(await screen.findByRole('heading', { name: 'Premium device upgrade eligibility' })).toBeInTheDocument()
    expect(screen.getByText('95%')).toBeInTheDocument()
  })

  it('renders ambiguity clarification state', async () => {
    vi.mocked(aiApi.generatePolicy).mockResolvedValue(mockAmbiguousPolicyResult)
    const user = userEvent.setup()
    renderWithProviders(<PolicyStudioPage />)

    await fillPolicyText(user, ambiguousPolicyText)
    await user.click(screen.getByRole('button', { name: /generate policy/i }))

    expect(await screen.findByText(/clarification needed/i)).toBeInTheDocument()
    expect(screen.getByText(/how should loyalty be measured/i)).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /activate policy/i })).not.toBeInTheDocument()
  })

  it('calls createPolicy when saving draft', async () => {
    vi.mocked(aiApi.generatePolicy).mockResolvedValue(mockGeneratedPolicyResult)
    vi.mocked(policyApi.createPolicy).mockResolvedValue({
      id: 'pol_new_001',
      ...mockGeneratedPolicyResult.generated_policy!,
      version: 1,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    })

    const user = userEvent.setup()
    renderWithProviders(<PolicyStudioPage />)

    await fillPolicyText(user, validPolicyText)
    await user.click(screen.getByRole('button', { name: /generate policy/i }))
    await user.click(await screen.findByRole('button', { name: /save as draft/i }))

    await waitFor(() => {
      expect(policyApi.createPolicy).toHaveBeenCalled()
    })
  })

  it('shows activate confirmation dialog', async () => {
    vi.mocked(aiApi.generatePolicy).mockResolvedValue(mockGeneratedPolicyResult)
    vi.mocked(policyApi.createPolicy).mockResolvedValue({
      id: 'pol_new_001',
      ...mockGeneratedPolicyResult.generated_policy!,
      version: 1,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    })

    const user = userEvent.setup()
    renderWithProviders(<PolicyStudioPage />)

    await fillPolicyText(user, validPolicyText)
    await user.click(screen.getByRole('button', { name: /generate policy/i }))
    await user.click(await screen.findByRole('button', { name: /save as draft/i }))
    await user.click(await screen.findByRole('button', { name: /^activate policy$/i }))

    expect(await screen.findByRole('dialog')).toBeInTheDocument()
  })

  it('shows back link to policies list', () => {
    renderWithProviders(<PolicyStudioPage />)
    expect(screen.getByRole('link', { name: /back to policies/i })).toHaveAttribute('href', '/policies')
  })
})
