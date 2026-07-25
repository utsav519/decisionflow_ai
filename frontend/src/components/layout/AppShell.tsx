import {
  useEffect,
  useState,
} from 'react'
import { Outlet } from 'react-router-dom'

import { Sidebar } from '@/components/layout/Sidebar'
import { env } from '@/config/env'
import {
  getHealth,
  type HealthStatus,
} from '@/services/healthApi'

const statusClasses: Record<HealthStatus, string> = {
  healthy: 'bg-green-500',
  degraded: 'bg-amber-500',
  unavailable: 'bg-red-500',
}

export function AppShell() {
  const [health, setHealth] =
    useState<HealthStatus>('degraded')

  const [healthMessage, setHealthMessage] =
    useState('Checking backend health...')

  useEffect(() => {
    let active = true

    void getHealth().then((result) => {
      if (!active) {
        return
      }

      setHealth(result.status)
      setHealthMessage(result.message)
    })

    return () => {
      active = false
    }
  }, [])

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-14 shrink-0 items-center justify-between border-b border-border bg-surface px-6">
          <div className="flex items-center gap-3">
            <span className="rounded-full bg-blue-100 px-2.5 py-1 text-xs font-semibold text-blue-800">
              Integrated POC
            </span>

            {env.useMockApi && (
              <span className="rounded-full bg-amber-100 px-2.5 py-1 text-xs font-semibold text-amber-800">
                Mock API
              </span>
            )}
          </div>

          <div className="flex items-center gap-6 text-sm">
            <div
              className="flex items-center gap-2"
              title={healthMessage}
            >
              <span
                className={`h-2.5 w-2.5 rounded-full ${statusClasses[health]}`}
              />
              <span className="capitalize text-text-secondary">
                {health}
              </span>
            </div>

            <div className="text-text-secondary">
              <span className="font-semibold text-text-primary">
                {env.defaultUserId}
              </span>
              <span className="mx-1">·</span>
              <span>
                {env.defaultUserRole.replaceAll('_', ' ')}
              </span>
            </div>
          </div>
        </header>

        <main className="min-w-0 flex-1 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
