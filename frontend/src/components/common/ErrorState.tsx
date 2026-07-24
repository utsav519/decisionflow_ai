export function ErrorState({
  message,
  code,
  correlationId,
  onRetry,
}: {
  message: string
  code?: string
  correlationId?: string
  onRetry?: () => void
}) {
  return (
    <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm" role="alert">
      <p className="font-medium text-red-800">{message}</p>
      {code && <p className="mt-1 text-red-700">Code: {code}</p>}
      {correlationId && <p className="mt-1 text-red-600">Correlation ID: {correlationId}</p>}
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-3 rounded-md bg-red-600 px-3 py-1.5 text-white hover:bg-red-700"
        >
          Retry
        </button>
      )}
    </div>
  )
}
