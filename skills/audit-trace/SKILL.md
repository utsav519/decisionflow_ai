---
name: audit-trace
description: Verifies audit trail completeness by performing a policy action and checking that the audit record has correct action, entity, summary, snapshots, and correlation ID per spec §30 and §36.
---

# Audit Trace Agent

## Purpose
Validates that every auditable action (policy CRUD, decisions) creates a proper audit record with the correct fields, JSON snapshots, and correlation tracking.

## How to Invoke

### As a User
```
/audit-trace
```
Or for a specific entity:
```
/audit-trace check pol_abc123
```

### As Another Agent
```
When verifying audit completeness, read and follow:
skills/audit-trace/SKILL.md
```

## Execution Steps

### Step 1: Check Audit Table Exists
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
.venv\Scripts\python -c "
from sqlalchemy import create_engine, inspect
from app.core.config import get_settings
engine = create_engine(get_settings().database_url)
inspector = inspect(engine)
columns = [c['name'] for c in inspector.get_columns('audit_logs')]
print('audit_logs columns:', columns)
"
```

### Step 2: Check Audit Records for an Entity
If a policy_id is provided, query audit records:
```powershell
.venv\Scripts\python -c "
from app.db.session import SessionLocal
from sqlalchemy import text
db = SessionLocal()
result = db.execute(text(
    'SELECT id, action, entity_type, entity_id, performed_by, summary, correlation_id, created_at '
    'FROM audit_logs WHERE entity_id = :eid ORDER BY created_at'
), {'eid': 'POLICY_ID_HERE'})
for row in result:
    print(f'{row.action:25s} | {row.entity_type:10s} | {row.correlation_id} | {row.created_at}')
db.close()
"
```

### Step 3: Verify Audit Record Fields (Spec §30)
For each audit record, verify:
- [ ] `id` starts with `aud_`
- [ ] `action` is one of: `POLICY_CREATED`, `POLICY_UPDATED`, `POLICY_ACTIVATED`, `POLICY_DISABLED`, `POLICY_DELETED`, `DECISION_EVALUATED`
- [ ] `entity_type` is set (e.g., `POLICY`, `EVALUATION`)
- [ ] `entity_id` matches the affected entity
- [ ] `entity_version` is set for versioned entities
- [ ] `performed_by` identifies the actor (or `demo_user`)
- [ ] `summary` is human-readable
- [ ] `correlation_id` starts with `cor_`
- [ ] `created_at` is in UTC

### Step 4: Verify JSON Snapshots
- [ ] `request_snapshot_json` contains the request body (for create/update)
- [ ] `result_snapshot_json` contains the response data
- [ ] Neither snapshot contains secrets, passwords, or API keys
- [ ] Snapshots are valid JSON (parseable)

### Step 5: Cross-Check Correlation IDs
For a given `correlation_id`:
1. Find the original API request (if logged)
2. Find the audit record
3. Verify both use the same correlation_id
4. Check that the audit's entity_id matches the API response's entity ID

### Step 6: Verify Audit API Endpoints
```
GET /api/v1/audit → returns paginated list
GET /api/v1/audit/{audit_id} → returns full detail with snapshots
```

Test pagination:
```powershell
.venv\Scripts\python -c "
import httpx, json
r = httpx.get('http://localhost:8000/api/v1/audit?page=1&page_size=5')
data = r.json()
print(f'Total audit records: {data.get(\"meta\", {}).get(\"total_items\", \"?\")}')
print(f'Records returned: {len(data.get(\"data\", []))}')
"
```

### Step 7: Verify Audit Principles (Spec §30)
- [ ] Audit records are append-only (no updates/deletes)
- [ ] No secrets stored in snapshots
- [ ] Enough context to explain each event
- [ ] Actor is recorded where available

### Step 8: Generate Report
```
╔══════════════════════════════════════════╗
║       AUDIT TRACE REPORT                 ║
╠══════════════════════════════════════════╣
║ Audit table exists:      ✅ / ❌          ║
║ Records found:           X               ║
║ Action field valid:      ✅ / ❌          ║
║ Entity tracking:         ✅ / ❌          ║
║ Correlation IDs:         ✅ / ❌          ║
║ JSON snapshots valid:    ✅ / ❌          ║
║ No secrets in snapshots: ✅ / ❌          ║
║ API list endpoint:       ✅ / ❌          ║
║ API detail endpoint:     ✅ / ❌          ║
║ Pagination works:        ✅ / ❌          ║
╚══════════════════════════════════════════╝
```
