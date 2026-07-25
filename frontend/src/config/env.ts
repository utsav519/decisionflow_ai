function readTimeout(): number {
  const configured = Number(
    import.meta.env.VITE_API_TIMEOUT_MS ?? 20000,
  )

  return Number.isFinite(configured)
    ? configured
    : 20000
}

export const env = {
  appName:
    import.meta.env.VITE_APP_NAME ??
    'DecisionFlow AI',

  apiBaseUrl:
    import.meta.env.VITE_API_BASE_URL ??
    'http://localhost:8000/api/v1',

  backendBaseUrl:
    import.meta.env.VITE_BACKEND_BASE_URL ??
    'http://localhost:8000',

  // Real backend is the default for the integrated app.
  useMockApi:
    import.meta.env.VITE_USE_MOCK_API === 'true',

  timeoutMs: readTimeout(),

  defaultUserId:
    import.meta.env.VITE_DEFAULT_USER_ID ??
    'demo_user',

  defaultUserRole:
    import.meta.env.VITE_DEFAULT_USER_ROLE ??
    'POLICY_MANAGER',
} as const
