import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { DecisionCenterPage } from '@/pages/DecisionCenterPage'
import * as decisionApi from '@/services/decisionApi'
import type { DecisionEvaluationResult } from '@/types/decision'
import { fireEvent, renderWithProviders, screen, userEvent, waitFor } from '@/tests/test-utils'

const approveResult: DecisionEvaluationResult = {
  evaluation_id: 'eval_test_001',
  decision: 'APPROVE',
  decision_confidence: 96,
  winning_policy: {
    id: 'pol_std_001',
    name: 'Standard upgrade approval',
    priority: 100,
    decision: 'APPROVE',
    version: 1,
  },
  matched_policies: [],
  unmatched_policies: [],
  skipped_policies: [],
  resolution: { strategy: 'HIGHEST_PRIORITY', reason: 'Standard policy matched.' },
  explanation: {
    summary: 'The request was approved because all thresholds were satisfied.',
    generated_by: 'AI',
    fallback_used: false,
  },
  metrics: {
    policies_loaded: 5,
    policies_evaluated: 5,
    policies_matched: 1,
    policies_skipped: 0,
    condition_count: 10,
    conflicts_detected: 0,
    engine_latency_ms: 41,
    explanation_latency_ms: 290,
    total_latency_ms: 331,
  },
  warnings: [],
  evaluated_at: new Date().toISOString(),
}

const rejectResult: DecisionEvaluationResult = {
  ...approveResult,
  evaluation_id: 'eval_test_002',
  decision: 'REJECT',
  decision_confidence: 92,
  winning_policy: {
    id: 'pol_fraud_001',
    name: 'Fraud rejection',
    priority: 300,
    decision: 'REJECT',
    version: 1,
  },
  explanation: {
    summary: 'The request was rejected because fraud risk exceeded the permitted threshold.',
    generated_by: 'AI',
    fallback_used: false,
  },
}

const manualReviewResult: DecisionEvaluationResult = {
  ...approveResult,
  evaluation_id: 'eval_test_003',
  decision: 'MANUAL_REVIEW',
  decision_confidence: 55,
  winning_policy: null,
  explanation: {
    summary: 'Manual review required because required fields were missing.',
    generated_by: 'DETERMINISTIC_FALLBACK',
    fallback_used: true,
  },
}

describe('DecisionCenterPage', () => {
  beforeEach(() => {
    vi.spyOn(decisionApi, 'evaluateDecision').mockImplementation(vi.fn())
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  async function evaluateEligibleCustomer(user: ReturnType<typeof userEvent.setup>) {
    await user.click(screen.getByRole('button', { name: /eligible customer/i }))
    await waitFor(() => {
      expect(screen.getByDisplayValue('CUST-1001')).toBeInTheDocument()
    })
    fireEvent.submit(screen.getByTestId('evaluation-form'))
  }

  it('fills form from eligible customer preset', async () => {
    const user = userEvent.setup()
    renderWithProviders(<DecisionCenterPage />)

    await user.click(screen.getByRole('button', { name: /eligible customer/i }))

    expect(screen.getByDisplayValue('CUST-1001')).toBeInTheDocument()
    expect(screen.getByDisplayValue('790')).toBeInTheDocument()
  })

  it('submits evaluation request with customer data', async () => {
    vi.mocked(decisionApi.evaluateDecision).mockResolvedValue(approveResult)
    const user = userEvent.setup()
    renderWithProviders(<DecisionCenterPage />)

    await evaluateEligibleCustomer(user)

    await waitFor(() => {
      expect(decisionApi.evaluateDecision).toHaveBeenCalledWith(
        expect.objectContaining({
          domain: 'telecom',
          customer: expect.objectContaining({ customer_id: 'CUST-1001' }),
        }),
      )
    })
  })

  it('renders approval result', async () => {
    vi.mocked(decisionApi.evaluateDecision).mockResolvedValue(approveResult)
    const user = userEvent.setup()
    renderWithProviders(<DecisionCenterPage />)

    await evaluateEligibleCustomer(user)

    expect(await screen.findByText('Standard upgrade approval')).toBeInTheDocument()
    expect(screen.getAllByText('APPROVE').length).toBeGreaterThan(0)
  })

  it('renders rejection result', async () => {
    vi.mocked(decisionApi.evaluateDecision).mockResolvedValue(rejectResult)
    const user = userEvent.setup()
    renderWithProviders(<DecisionCenterPage />)

    await user.click(screen.getByRole('button', { name: /high fraud risk/i }))
    await waitFor(() => expect(screen.getByDisplayValue('CUST-1002')).toBeInTheDocument())
    fireEvent.submit(screen.getByTestId('evaluation-form'))

    expect(await screen.findByText('Fraud rejection')).toBeInTheDocument()
    expect(screen.getAllByText('REJECT').length).toBeGreaterThan(0)
  })

  it('renders manual review and fallback explanation notice', async () => {
    vi.mocked(decisionApi.evaluateDecision).mockResolvedValue(manualReviewResult)
    const user = userEvent.setup()
    renderWithProviders(<DecisionCenterPage />)

    await user.click(screen.getByRole('button', { name: /missing info/i }))
    await waitFor(() => expect(screen.getByDisplayValue('CUST-1003')).toBeInTheDocument())
    fireEvent.submit(screen.getByTestId('evaluation-form'))

    expect(await screen.findByText(/deterministic fallback/i)).toBeInTheDocument()
    expect(screen.getByText(/manual review required/i)).toBeInTheDocument()
  })

  it('shows metrics after evaluation', async () => {
    vi.mocked(decisionApi.evaluateDecision).mockResolvedValue(approveResult)
    const user = userEvent.setup()
    renderWithProviders(<DecisionCenterPage />)

    await evaluateEligibleCustomer(user)

    expect(await screen.findByText(/policies loaded:/i)).toBeInTheDocument()
    expect(screen.getByText(/total latency:/i)).toBeInTheDocument()
  })

  it('shows API error without clearing form input', async () => {
    vi.mocked(decisionApi.evaluateDecision).mockRejectedValue(new Error('Evaluation failed'))
    const user = userEvent.setup()
    renderWithProviders(<DecisionCenterPage />)

    await evaluateEligibleCustomer(user)

    expect(await screen.findByText('Evaluation failed')).toBeInTheDocument()
    expect(screen.getByDisplayValue('CUST-1001')).toBeInTheDocument()
  })
})
