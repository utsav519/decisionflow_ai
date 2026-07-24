import { format, parseISO } from 'date-fns'

export function formatDateTime(value: string): string {
  try {
    return format(parseISO(value), 'dd MMM yyyy, h:mm a')
  } catch {
    return value
  }
}

export function formatCurrency(value: number, currency = 'INR'): string {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency,
    maximumFractionDigits: 0,
  }).format(value)
}

export function formatPercent(value: number): string {
  return `${Math.round(value * 100)}%`
}

export function formatMs(value: number): string {
  return `${value} ms`
}

export function fieldLabel(field: string): string {
  return field
    .split('_')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ')
}
