export function createCorrelationId(): string {
  return `cor_${crypto.randomUUID().replaceAll('-', '')}`
}
