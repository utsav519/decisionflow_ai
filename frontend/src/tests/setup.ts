import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'

class ResizeObserverMock {
  observe() {}
  unobserve() {}
  disconnect() {}
}

globalThis.ResizeObserver = ResizeObserverMock as unknown as typeof ResizeObserver

afterEach(() => {
  cleanup()
})
