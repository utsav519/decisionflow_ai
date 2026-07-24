import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AppShell } from '@/components/layout/AppShell'
import { AnalyticsPage } from '@/pages/AnalyticsPage'
import { AuditDetailPage, AuditPage } from '@/pages/AuditPage'
import { DashboardPage } from '@/pages/DashboardPage'
import { DecisionCenterPage } from '@/pages/DecisionCenterPage'
import { DecisionDetailPage, NotFoundPage, SettingsPage } from '@/pages/SettingsPage'
import { PoliciesPage } from '@/pages/PoliciesPage'
import { PolicyDetailPage } from '@/pages/PolicyDetailPage'
import { PolicyStudioPage } from '@/pages/PolicyStudioPage'

export function AppRouter() {
  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/policies" element={<PoliciesPage />} />
          <Route path="/policies/new" element={<PolicyStudioPage />} />
          <Route path="/policies/:policyId" element={<PolicyDetailPage />} />
          <Route path="/decisions" element={<DecisionCenterPage />} />
          <Route path="/decisions/:evaluationId" element={<DecisionDetailPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/audit" element={<AuditPage />} />
          <Route path="/audit/:auditId" element={<AuditDetailPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="/404" element={<NotFoundPage />} />
          <Route path="*" element={<Navigate to="/404" replace />} />
        </Routes>
      </AppShell>
    </BrowserRouter>
  )
}
