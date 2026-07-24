import { render, type RenderOptions } from '@testing-library/react'
import { MemoryRouter, type MemoryRouterProps } from 'react-router-dom'
import { ToastProvider } from '@/components/common/ToastProvider'

interface Options extends Omit<RenderOptions, 'wrapper'> {
  routerProps?: MemoryRouterProps
}

export function renderWithProviders(ui: React.ReactElement, options: Options = {}) {
  const { routerProps, ...renderOptions } = options

  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <ToastProvider>
        <MemoryRouter {...routerProps}>{children}</MemoryRouter>
      </ToastProvider>
    )
  }

  return render(ui, { wrapper: Wrapper, ...renderOptions })
}

export * from '@testing-library/react'
export { default as userEvent } from '@testing-library/user-event'
export { fireEvent } from '@testing-library/react'
