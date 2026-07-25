---
name: policy-lifecycle
description: Tests the full policy lifecycle — create, read, update, activate, disable — with proper correlation IDs, actor context, audit verification, and version snapshot checks per spec §26-27.
---

# Policy Lifecycle Agent

## Purpose
Runs an end-to-end test of the complete policy lifecycle through the API, verifying every state transition, audit trail, version history, and response format.

## How to Invoke

### As a User
```
/policy-lifecycle
```
Or test a specific operation:
```
/policy-lifecycle activate pol_abc123
```

### As Another Agent
```
When verifying policy CRUD is working correctly, read and follow:
skills/policy-lifecycle/SKILL.md
```

## Execution Steps

### Step 1: Verify Backend is Running
```powershell
.venv\Scripts\python -c "import httpx; r = httpx.get('http://localhost:8000/api/v1/config/fields'); print(f'Status: {r.status_code}')"
```
If not running, start it:
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
.venv\Scripts\python -m uvicorn app.main:app --reload
```

### Step 2: CREATE — Create a Test Policy
```powershell
.venv\Scripts\python -c "
import httpx, json
r = httpx.post('http://localhost:8000/api/v1/policies',
    json={
        'name': 'Lifecycle Test Policy',
        'description': 'Created by lifecycle agent',
        'domain': 'telecom',
        'priority': 150,
        'decision': 'APPROVE',
        'conditions': {
            'all': [
                {'field': 'credit_score', 'operator': 'greater_than_or_equal', 'value': 700},
                {'field': 'payment_defaults', 'operator': 'equals', 'value': 0}
            ]
        },
        'reason': 'Test policy for lifecycle validation',
        'source': 'MANUAL'
    },
    headers={'X-Correlation-ID': 'cor_lifecycle_test', 'X-User-ID': 'lifecycle_agent'}
)
print(f'Status: {r.status_code}')
print(json.dumps(r.json(), indent=2))
"
```

**Verify:**
- [ ] Status code is `201`
- [ ] `data.status` is `DRAFT` (forced by server, spec §26)
- [ ] `data.version` is `1`
- [ ] `data.id` starts with `pol_`
- [ ] `correlation_id` matches sent header
- [ ] `meta.validation_status` is `PASSED`

Save the `policy_id` from response for subsequent steps.

### Step 3: READ — Get Policy by ID
```
GET /api/v1/policies/{policy_id}
```
**Verify:**
- [ ] Returns all 19 fields from contract §11.1
- [ ] `status` is still `DRAFT`

### Step 4: LIST — List with Filters
```
GET /api/v1/policies?status=DRAFT&page=1&page_size=10
```
**Verify:**
- [ ] Pagination meta present
- [ ] Policy appears in list
- [ ] List item has expected fields

### Step 5: UPDATE — Update the Draft
```
PUT /api/v1/policies/{policy_id}
```
Body: change priority to 160, update description
**Verify:**
- [ ] Status is still `DRAFT`
- [ ] Priority updated to 160

### Step 6: ACTIVATE — Activate the Policy
```
POST /api/v1/policies/{policy_id}/activate
```
Body: `{"approval_comment": "Approved by lifecycle agent"}`
**Verify:**
- [ ] Status changes to `ACTIVE`
- [ ] `approved_by` is set
- [ ] `activated_at` is set
- [ ] `meta.validation_status` is `PASSED`

### Step 7: VERIFY VERSION — Check Version Snapshot
After activation, a policy version snapshot should exist (spec §26):
- Query the policy and verify `version` reflects the snapshot

### Step 8: DUPLICATE NAME — Test Rejection
```
POST /api/v1/policies
```
Body: same name as the test policy
**Verify:**
- [ ] Status code is `409`
- [ ] Error code is `DUPLICATE_POLICY_NAME`

### Step 9: DISABLE — Disable the Active Policy
```
POST /api/v1/policies/{policy_id}/disable
```
Body: `{"reason": "Lifecycle test completed"}`
**Verify:**
- [ ] Status changes to `DISABLED`
- [ ] `disabled_at` is set (if returned)

### Step 10: AUDIT — Verify Audit Trail
```
GET /api/v1/audit?entity_id={policy_id}
```
**Verify:**
- [ ] At least 3 audit entries: POLICY_CREATED, POLICY_ACTIVATED, POLICY_DISABLED
- [ ] Each has: action, entity_type, entity_id, summary, correlation_id

### Step 11: CLEANUP — Delete the Test Policy
```
DELETE /api/v1/policies/{policy_id}
```
**Verify:**
- [ ] Policy is archived or deleted per contract §16

### Step 12: Generate Report
```
╔══════════════════════════════════════════╗
║       POLICY LIFECYCLE REPORT            ║
╠══════════════════════════════════════════╣
║ Create (DRAFT):         ✅ / ❌           ║
║ Read (by ID):           ✅ / ❌           ║
║ List (with filters):    ✅ / ❌           ║
║ Update (draft):         ✅ / ❌           ║
║ Activate:               ✅ / ❌           ║
║ Version Snapshot:       ✅ / ❌           ║
║ Duplicate Rejection:    ✅ / ❌           ║
║ Disable:                ✅ / ❌           ║
║ Audit Trail (3+ events):✅ / ❌           ║
║ Delete/Archive:         ✅ / ❌           ║
║ Correlation IDs:        ✅ / ❌           ║
╚══════════════════════════════════════════╝
```
