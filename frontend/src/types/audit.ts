export interface AuditListItem {
  audit_id: string
  action: string
  entity_type: string
  entity_id: string
  entity_version?: number
  performed_by?: string
  summary: string
  correlation_id: string
  created_at: string
}

export interface AuditDetail extends AuditListItem {
  request_snapshot?: Record<string, unknown>
  result_snapshot?: Record<string, unknown>
  rule_versions?: Array<{ policy_id: string; version: number }>
  metadata?: Record<string, unknown>
}
