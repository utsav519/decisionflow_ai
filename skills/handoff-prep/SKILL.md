---
name: handoff-prep
description: Prepares the integration handoff package by verifying all §57 Definition of Done items, running the full test suite, checking for secrets/SQLite, and generating the handoff message in the exact template from §59.
---

# Handoff Preparation Agent

## Purpose
Performs the final verification checklist and generates the integration handoff package in the exact format required by spec §58-59.

## How to Invoke

### As a User
```
/handoff-prep
```

### As Another Agent
```
When all phases are complete and you're ready to hand off, read and follow:
skills/handoff-prep/SKILL.md
```

## Execution Steps

### Step 1: Run the Definition of Done Checklist (Spec §57)

#### Database ✅/❌
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
# Check MySQL connection
.venv\Scripts\python -c "
from sqlalchemy import create_engine, text
from app.core.config import get_settings
engine = create_engine(get_settings().database_url, pool_pre_ping=True)
with engine.connect() as conn:
    conn.execute(text('SELECT 1'))
    print('✅ MySQL connects')
"
```
- [ ] MySQL container/server starts
- [ ] Database is created
- [ ] Migrations succeed (`alembic upgrade head`)
- [ ] Seed succeeds (`python -m app.db.seed`)
- [ ] Re-running seed creates no duplicates

#### Policy Management ✅/❌
Test each via API:
- [ ] Create works (POST returns 201)
- [ ] List works (GET returns paginated)
- [ ] Filter works (status, decision, source params)
- [ ] Detail works (GET by ID returns full object)
- [ ] Update works (PUT returns updated)
- [ ] Activate works (POST activate changes status)
- [ ] Disable works (POST disable changes status)
- [ ] History is preserved (version snapshots exist)

#### Rule Engine ✅/❌
Run engine tests:
```powershell
.venv\Scripts\python -m pytest tests/test_operators.py tests/test_evaluator.py tests/test_resolver.py tests/test_confidence.py -v --tb=short
```
- [ ] Supported operators work
- [ ] All/any groups work
- [ ] Nested conditions work
- [ ] Missing fields are traced
- [ ] Multiple rules are resolved
- [ ] No-match fallback is deterministic
- [ ] Confidence is deterministic

#### Persistence ✅/❌
- [ ] Evaluations can be saved
- [ ] Rule traces can be saved
- [ ] Audit events can be saved
- [ ] Transactions roll back on failure

#### Analytics ✅/❌
- [ ] Summary works
- [ ] Distribution works
- [ ] Trend works
- [ ] Top policies works

#### Quality ✅/❌
- [ ] All tests pass
- [ ] Swagger reflects contract (`/docs` loads)
- [ ] Correlation IDs work (present in responses)
- [ ] Standard errors work (envelope format correct)
- [ ] No secrets are committed
- [ ] No SQLite references remain

### Step 2: Check for Secrets
```powershell
cd e:\code\hackathon\decisionflow_ai
Select-String -Path backend -Include "*.py","*.yml","*.yaml","*.txt","*.cfg","*.ini" -Pattern "password|secret|api_key|token" -Recurse | Where-Object { $_.Path -notlike "*\.env*" -and $_.Path -notlike "*\.git*" }
```

### Step 3: Check for SQLite References
```powershell
cd e:\code\hackathon\decisionflow_ai
Select-String -Path backend -Include "*.py" -Pattern "sqlite|SQLite|:memory:" -Recurse
```
There must be ZERO results.

### Step 4: Run Full Test Suite
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
.venv\Scripts\python -m pytest -v --tb=short 2>&1
```

### Step 5: Get Git Info
```powershell
cd e:\code\hackathon\decisionflow_ai
git branch --show-current
git log -1 --format="%H %s"
```

### Step 6: Generate Handoff Message (Spec §59 Template)
Create `backend/HANDOFF.md` with the exact template:

```markdown
# Backend module handoff

## Branch
feature/backend-rule-engine

## Latest commit
<commit hash>

## Completed
- MySQL models and migrations
- Policy CRUD
- Policy activation and disable
- Rule engine
- Priority resolver
- Confidence calculator
- Audit persistence
- Analytics queries

## Run
1. docker compose up -d mysql  (or connect to remote MySQL)
2. cd backend
3. .venv\Scripts\activate  (Windows)
4. alembic upgrade head
5. python -m app.db.seed
6. uvicorn app.main:app --reload

## Tests
pytest -q
Result: <passed count> passed

## Integration imports
- app.services.policy_service.PolicyService
- app.engine.evaluator.RuleEngine
- app.engine.resolver.PriorityResolver
- app.engine.confidence.DecisionConfidenceCalculator
- app.repositories.evaluation_repository.EvaluationRepository
- app.services.audit_service.AuditService

## Known limitations
- <list>

## API contract deviations
- None
```

### Step 7: Final Swagger Check
If the app is running:
```powershell
.venv\Scripts\python -c "
import httpx
r = httpx.get('http://localhost:8000/openapi.json')
schema = r.json()
paths = schema.get('paths', {})
print(f'Total routes: {sum(len(m) for m in paths.values())}')
for path in sorted(paths):
    methods = ', '.join(m.upper() for m in paths[path])
    print(f'  {methods:10s} {path}')
"
```

### Step 8: Generate Final Report
```
╔══════════════════════════════════════════════╗
║       HANDOFF READINESS REPORT               ║
╠══════════════════════════════════════════════╣
║ Database:           ✅ / ❌  (5 checks)      ║
║ Policy CRUD:        ✅ / ❌  (8 checks)      ║
║ Rule Engine:        ✅ / ❌  (7 checks)      ║
║ Persistence:        ✅ / ❌  (4 checks)      ║
║ Analytics:          ✅ / ❌  (4 checks)      ║
║ Quality:            ✅ / ❌  (6 checks)      ║
║ No Secrets:         ✅ / ❌                   ║
║ No SQLite:          ✅ / ❌                   ║
║ Tests:              XX passed, XX failed      ║
║ Swagger:            XX routes registered       ║
║ HANDOFF.md:         ✅ / ❌  Generated        ║
╠══════════════════════════════════════════════╣
║ READY TO HANDOFF:   ✅ YES / ❌ NO           ║
╚══════════════════════════════════════════════╝
```
