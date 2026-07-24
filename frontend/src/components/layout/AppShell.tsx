import { useEffect, useState } from 'react'
import { Sidebar } from '@/components/layout/Sidebar'
import { env } from '@/config/env'
import { getHealth, type HealthStatus } from '@/services/healthApi'

const statusColors: Record<HealthStatus, string> = {
  healthy: 'bg-green-500',
  degraded: 'bg-amber-500',
  unavailable: 'bg-red-500',
}

export function Topbar() {
  const [health, setHealth] = useState<HealthStatus>('healthy')
  const [message, setMessage] = useState('Checking...')

  useEffect(() => {
    getHealth().then((result) => {
      setHealth(result.status)
      setMessage(result.message)
    })
  }, [])

  return (
    <header className="flex h-14 items-center justify-between border-b border-border bg-surface px-6">
      <div className="flex items-center gap-3">
        <span className="rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800">Demo</span>
        {env.useMockApi && (
          <span className="rounded-full bg-amber-100 px-2.5 py-0.5 text-xs font-medium text-amber-800">Mock API</span>
        )}
      </div>
      <div className="flex items-center gap-6 text-sm">
        <div className="flex items-center gap-2" title={message}>
          <span className={`h-2 w-2 rounded-full ${statusColors[health]}`} />
          <span className="text-text-secondary capitalize">{health}</span>
        </div>
        <div className="text-text-secondary">
          <span className="font-medium text-text-primary">{env.defaultUserId}</span>
          <span className="mx-1">·</span>
          <span>{env.defaultUserRole.replace('_', ' ')}</span>
        </div>
      </div>
    </header>
  )
}

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar />
        <main className="flex-1 overflow-auto p-6">{children}</main>
      </div>
    </div>
  )
}
