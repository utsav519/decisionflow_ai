import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from 'react-router-dom'

import { AppShell } from '@/components/layout/AppShell'
import { DashboardPage } from '@/pages/DashboardPage'
import { DecisionCenterPage } from '@/pages/DecisionCenterPage'
import { PlaceholderPage } from '@/pages/PlaceholderPage'

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route
            index
            element={<DashboardPage />}
          />

          <Route
            path="policies/new"
            element={
              <PlaceholderPage
                title="AI Policy Studio"
                description="Generate, clarify, validate and review governed policy drafts using AI assistance."
              />
            }
          />

          <Route
            path="policies"
            element={
              <PlaceholderPage
                title="Policies"
                description="View and manage policy versions, priorities, lifecycle status and activation."
              />
            }
          />

          <Route
            path="policies/:policyId"
            element={
              <PlaceholderPage
                title="Policy Details"
                description="Review a policy definition, conditions, versions and lifecycle controls."
              />
            }
          />

          <Route
            path="decisions"
            element={<DecisionCenterPage />}
          />

          <Route
            path="decisions/:evaluationId"
            element={
              <PlaceholderPage
                title="Decision Details"
                description="Retrieve and inspect a persisted decision evaluation and its complete trace."
              />
            }
          />

          <Route
            path="analytics"
            element={
              <PlaceholderPage
                title="Analytics"
                description="Explore decision distributions, trends, latency and top-policy performance."
              />
            }
          />

          <Route
            path="audit"
            element={
              <PlaceholderPage
                title="Audit Logs"
                description="Review decision, policy lifecycle and AI-provider audit events."
              />
            }
          />

          <Route
            path="audit/:auditId"
            element={
              <PlaceholderPage
                title="Audit Details"
                description="Inspect one audit event with entity, user and correlation information."
              />
            }
          />

          <Route
            path="settings"
            element={
              <PlaceholderPage
                title="Settings"
                description="Review application environment and backend health information."
              />
            }
          />

          <Route
            path="404"
            element={
              <PlaceholderPage
                title="Page not found"
                description="The requested DecisionFlow page does not exist."
              />
            }
          />

          <Route
            path="*"
            element={<Navigate to="/404" replace />}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
