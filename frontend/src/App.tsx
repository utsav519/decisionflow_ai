import { ToastProvider } from '@/components/common/ToastProvider'
import { AppRouter } from '@/router/AppRouter'

export default function App() {
  return (
    <ToastProvider>
      <AppRouter />
    </ToastProvider>
  )
}
