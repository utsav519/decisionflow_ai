import type { AuditDetail, AuditListItem } from '@/types/audit'

const now = new Date().toISOString()

export const mockAuditList: AuditListItem[] = [
  {
    audit_id: 'aud_001',
    action: 'POLICY_ACTIVATED',
    entity_type: 'policy',
    entity_id: 'pol_std_001',
    entity_version: 1,
    performed_by: 'demo_user',
    summary: 'Standard upgrade approval activated.',
    correlation_id: 'cor_demo001',
    created_at: now,
  },
  {
    audit_id: 'aud_002',
    action: 'DECISION_EVALUATED',
    entity_type: 'evaluation',
    entity_id: 'eval_1001',
    performed_by: 'demo_user',
    summary: 'Customer CUST-1001 evaluated — APPROVE.',
    correlation_id: 'cor_demo002',
    created_at: now,
  },
  {
    audit_id: 'aud_003',
    action: 'DECISION_EVALUATED',
    entity_type: 'evaluation',
    entity_id: 'eval_1002',
    performed_by: 'demo_user',
    summary: 'Customer CUST-1002 evaluated — REJECT.',
    correlation_id: 'cor_demo003',
    created_at: now,
  },
  {
    audit_id: 'aud_004',
    action: 'POLICY_CREATED',
    entity_type: 'policy',
    entity_id: 'pol_draft_001',
    entity_version: 1,
    performed_by: 'demo_user',
    summary: 'New device promo draft saved.',
    correlation_id: 'cor_demo004',
    created_at: now,
  },
]

export const mockAuditDetails: Record<string, AuditDetail> = Object.fromEntries(
  mockAuditList.map((item) => [
    item.audit_id,
    {
      ...item,
      request_snapshot: { customer_id: 'CUST-1001' },
      result_snapshot: { decision: 'APPROVE', confidence: 96 },
      rule_versions: [{ policy_id: 'pol_std_001', version: 1 }],
      metadata: { source: 'mock' },
    },
  ]),
)
