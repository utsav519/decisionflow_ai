import {
  BarChart3,
  ClipboardList,
  FileText,
  LayoutDashboard,
  Scale,
  Settings,
  Sparkles,
} from 'lucide-react'
import { NavLink } from 'react-router-dom'

import { env } from '@/config/env'
import { cn } from '@/utils/cn'

const navItems = [
  {
    to: '/',
    label: 'Dashboard',
    icon: LayoutDashboard,
    end: true,
  },
  {
    to: '/policies/new',
    label: 'AI Policy Studio',
    icon: Sparkles,
  },
  {
    to: '/policies',
    label: 'Policies',
    icon: FileText,
  },
  {
    to: '/decisions',
    label: 'Decision Center',
    icon: Scale,
  },
  {
    to: '/analytics',
    label: 'Analytics',
    icon: BarChart3,
  },
  {
    to: '/audit',
    label: 'Audit Logs',
    icon: ClipboardList,
  },
  {
    to: '/settings',
    label: 'Settings',
    icon: Settings,
  },
]

export function Sidebar() {
  return (
    <aside className="flex h-screen w-64 shrink-0 flex-col border-r border-border bg-surface">
      <div className="border-b border-border px-5 py-5">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand text-brand-foreground shadow-sm">
            <Sparkles className="h-5 w-5" />
          </div>

          <div>
            <p className="m-0 text-sm font-bold text-text-primary">
              {env.appName}
            </p>
            <p className="m-0 text-xs text-text-muted">
              Telecom Decision POC
            </p>
          </div>
        </div>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto p-3">
        {navItems.map((item) => {
          const Icon = item.icon

          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-blue-50 text-brand'
                    : 'text-text-secondary hover:bg-surface-muted hover:text-text-primary',
                )
              }
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </NavLink>
          )
        })}
      </nav>

      <div className="border-t border-border px-5 py-4 text-xs text-text-muted">
        Governed AI · Deterministic Decisions
      </div>
    </aside>
  )
}
