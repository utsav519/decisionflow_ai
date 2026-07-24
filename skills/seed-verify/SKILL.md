---
name: seed-verify
description: Verifies seed data idempotency by running the seed command twice and confirming no duplicates are created, and all 5 required policies exist with correct data per spec §39.
---

# Seed Verify Agent

## Purpose
Validates that seed data is idempotent (running twice creates no duplicates) and all 5 spec-required policies are correctly seeded.

## How to Invoke

### As a User
```
/seed-verify
```

### As Another Agent
```
After modifying backend/app/db/seed.py, read and follow:
skills/seed-verify/SKILL.md
```

## Execution Steps

### Step 1: Count Before First Seed
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
.venv\Scripts\python -c "
from app.db.session import SessionLocal
from sqlalchemy import text
db = SessionLocal()
result = db.execute(text('SELECT COUNT(*) FROM policies'))
print(f'Policies before seed: {result.scalar()}')
db.close()
"
```

### Step 2: Run Seed (First Time)
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
.venv\Scripts\python -m app.db.seed
```

### Step 3: Count After First Seed
```powershell
.venv\Scripts\python -c "
from app.db.session import SessionLocal
from sqlalchemy import text
db = SessionLocal()
result = db.execute(text('SELECT COUNT(*) FROM policies'))
count_after_first = result.scalar()
print(f'Policies after first seed: {count_after_first}')
db.close()
"
```

### Step 4: Run Seed (Second Time)
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
.venv\Scripts\python -m app.db.seed
```

### Step 5: Count After Second Seed
```powershell
.venv\Scripts\python -c "
from app.db.session import SessionLocal
from sqlalchemy import text
db = SessionLocal()
result = db.execute(text('SELECT COUNT(*) FROM policies'))
count_after_second = result.scalar()
print(f'Policies after second seed: {count_after_second}')
db.close()
"
```

**CRITICAL CHECK:** `count_after_first` MUST equal `count_after_second`

### Step 6: Verify Required Policies Exist
The spec (§39) requires exactly these 5 seed policies:

| # | Name | Status | Priority | Decision |
|---|---|---|---|---|
| 1 | Fraud rejection | ACTIVE | 300 | REJECT |
| 2 | Fraud manual review | ACTIVE | 250 | MANUAL_REVIEW |
| 3 | Outstanding balance rejection | ACTIVE | 220 | REJECT |
| 4 | Standard upgrade approval | ACTIVE | 100 | APPROVE |
| 5 | Premium override approval | ACTIVE | 120 | APPROVE |

```powershell
.venv\Scripts\python -c "
from app.db.session import SessionLocal
from sqlalchemy import text
db = SessionLocal()
result = db.execute(text(
    'SELECT name, status, priority, decision FROM policies WHERE source = \"SEEDED\" ORDER BY priority DESC'
))
for row in result:
    print(f'{row.priority:4d} | {row.status:10s} | {row.decision:15s} | {row.name}')
db.close()
"
```

### Step 7: Verify Seed Policy Conditions
For each seed policy, verify the conditions JSON matches the spec.

### Step 8: Generate Report
```
╔══════════════════════════════════════════╗
║       SEED VERIFICATION REPORT           ║
╠══════════════════════════════════════════╣
║ First seed ran:         ✅ / ❌           ║
║ Count after first:      X                ║
║ Second seed ran:        ✅ / ❌           ║
║ Count after second:     X                ║
║ Idempotent:             ✅ / ❌           ║
║ 5 required policies:    ✅ / ❌           ║
║ All ACTIVE status:      ✅ / ❌           ║
║ Conditions match spec:  ✅ / ❌           ║
║ Source is SEEDED:        ✅ / ❌           ║
╚══════════════════════════════════════════╝
```
