export function createCorrelationId(): string {
  return `cor_ui_${crypto.randomUUID().replaceAll('-', '')}`
}

export function createRequestId(): string {
  return `req_ui_${crypto.randomUUID().replaceAll('-', '')}`
}
