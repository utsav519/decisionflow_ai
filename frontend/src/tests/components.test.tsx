import { describe, expect, it, vi } from 'vitest'
import { ConfirmDialog } from '@/components/common/ConfirmDialog'
import { CopyButton } from '@/components/common/CopyButton'
import { renderWithProviders, screen, userEvent } from '@/tests/test-utils'

describe('ConfirmDialog', () => {
  it('renders title and calls confirm handler', async () => {
    const onConfirm = vi.fn()
    const onCancel = vi.fn()
    const user = userEvent.setup()

    renderWithProviders(
      <ConfirmDialog
        open
        title="Activate this policy?"
        description="Once active, it will participate in evaluations."
        onConfirm={onConfirm}
        onCancel={onCancel}
      />,
    )

    expect(screen.getByRole('dialog')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: /^confirm$/i }))
    expect(onConfirm).toHaveBeenCalledTimes(1)
  })

  it('calls cancel handler from cancel button', async () => {
    const onCancel = vi.fn()
    const user = userEvent.setup()

    renderWithProviders(
      <ConfirmDialog
        open
        title="Disable policy?"
        confirmLabel="Disable"
        onConfirm={vi.fn()}
        onCancel={onCancel}
      />,
    )

    const cancelButtons = screen.getAllByRole('button', { name: /cancel/i })
    await user.click(cancelButtons[cancelButtons.length - 1]!)
    expect(onCancel).toHaveBeenCalledTimes(1)
  })
})

describe('CopyButton', () => {
  it('renders copy label', () => {
    renderWithProviders(<CopyButton value="cor_demo001" label="Copy ID" />)
    expect(screen.getByRole('button', { name: /copy id/i })).toBeInTheDocument()
  })
})
