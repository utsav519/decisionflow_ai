---
name: contract-check
description: Compares every implemented FastAPI route against the API contract (02_API_CONTRACT) for exact paths, methods, field names, status codes, enums, response envelopes, and pagination metadata.
---

# API Contract Compliance Agent

## Purpose
Ensures every route in the backend matches the API contract exactly — paths, HTTP methods, request/response field names, status codes, enums, and envelope structure.

## How to Invoke

### As a User
```
/contract-check
```
Or target a specific router:
```
/contract-check policies
/contract-check analytics
```

### As Another Agent
```
After adding or modifying any route in backend/app/api/v1/, read and follow:
skills/contract-check/SKILL.md
```

## Execution Steps

### Step 1: Load the Contract
Read the API contract from:
```
e:\code\hackathon\decisionflow_ai\backend\02_API_CONTRACT(1).md
```

Extract the canonical route list:

| # | Method | Path | Status | Contract Section |
|---|---|---|---|---|
| 1 | POST | `/api/v1/policies` | 201 | §12 |
| 2 | GET | `/api/v1/policies` | 200 | §13 |
| 3 | GET | `/api/v1/policies/{policy_id}` | 200 | §14 |
| 4 | PUT | `/api/v1/policies/{policy_id}` | 200 | §15 |
| 5 | DELETE | `/api/v1/policies/{policy_id}` | 200 | §16 |
| 6 | POST | `/api/v1/policies/{policy_id}/activate` | 200 | §17 |
| 7 | POST | `/api/v1/policies/{policy_id}/disable` | 200 | §18 |
| 8 | GET | `/api/v1/config/fields` | 200 | §9 |
| 9 | GET | `/api/v1/config/operators` | 200 | §10 |
| 10 | GET | `/api/v1/analytics/summary` | 200 | contract |
| 11 | GET | `/api/v1/analytics/decision-distribution` | 200 | contract |
| 12 | GET | `/api/v1/analytics/decision-trend` | 200 | contract |
| 13 | GET | `/api/v1/analytics/top-policies` | 200 | contract |
| 14 | GET | `/api/v1/audit` | 200 | contract |
| 15 | GET | `/api/v1/audit/{audit_id}` | 200 | contract |

### Step 2: Compare Against OpenAPI Schema
Start the app briefly to get the OpenAPI schema:
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
# If app is running, fetch the schema:
.venv\Scripts\python -c "
import httpx
r = httpx.get('http://localhost:8000/openapi.json')
import json
schema = r.json()
paths = schema.get('paths', {})
for path, methods in sorted(paths.items()):
    for method in methods:
        print(f'{method.upper():6s} {path}')
"
```

If the app isn't running, statically scan the router files:
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
Select-String -Path "app/api/v1/*.py" -Pattern "@router\.(get|post|put|delete|patch)" | ForEach-Object { $_.Line.Trim() }
```

### Step 3: Verify Each Route
For each route, check:

- [ ] **Path**: Exact match including hyphens (e.g., `decision-distribution` not `decision_distribution`)
- [ ] **Method**: GET/POST/PUT/DELETE matches contract
- [ ] **Request body**: Field names match contract exactly (camelCase vs snake_case check)
- [ ] **Response body**: All fields present in `data` object
- [ ] **Success status code**: Matches contract (especially 201 for POST create)
- [ ] **Error status codes**: 400, 404, 409, 422 used correctly
- [ ] **Response envelope**: `success`, `data`, `meta`, `correlation_id` present
- [ ] **Error envelope**: `success`, `error.code`, `error.message`, `error.details` present
- [ ] **Pagination**: `meta.page`, `meta.page_size`, `meta.total_items`, `meta.total_pages`
- [ ] **Correlation ID**: Present in response body AND `X-Correlation-ID` response header
- [ ] **Enum values**: Status, decision, source, action match contract §5.5

### Step 4: Check Query Parameters (List Endpoints)
For `GET /api/v1/policies`:
- [ ] `page` (int, optional, default 1)
- [ ] `page_size` (int, optional, default 20)
- [ ] `status` (string, optional)
- [ ] `decision` (string, optional)
- [ ] `source` (string, optional)
- [ ] `search` (string, optional)
- [ ] `sort_by` (string, optional)
- [ ] `sort_order` (string, optional)

### Step 5: Generate Compliance Report
```
ROUTE                                    | Method | Status | Fields | Envelope | Enums | RESULT
-----------------------------------------|--------|--------|--------|----------|-------|---------
/api/v1/policies                   POST  | ✅      | ✅      | ✅      | ✅        | ✅     | PASS
/api/v1/policies                   GET   | ✅      | ✅      | ✅      | ✅        | ✅     | PASS
/api/v1/policies/{id}              GET   | ✅      | ✅      | ⚠️      | ✅        | ✅     | WARN
/api/v1/policies/{id}/activate     POST  | ❌      | —      | —      | —        | —     | MISSING
...
```

### Step 6: Flag Deviations
For each deviation:
1. Show what the contract says (with section reference)
2. Show what the code currently does
3. Rate severity: BLOCKING (must fix) vs WARNING (nice to fix)
4. Propose the exact fix
5. **Wait for approval before applying**

## Critical Contract Rules
- Do NOT change the contract without architect approval (§47 of backend spec)
- Use snake_case for all JSON field names in backend responses
- Use hyphenated paths for URL routes (e.g., `decision-distribution`)
- Correlation ID format: `cor_` prefix (§36 of backend spec)
