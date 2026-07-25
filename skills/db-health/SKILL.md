---
name: db-health
description: Diagnoses MySQL connectivity, migration state, table structure, and index verification against the database spec (§7, §11, §13, §50).
---

# Database Health Agent

## Purpose
Verifies MySQL is reachable, migrations are current, all 5 tables exist with correct columns and indexes, and the health check function works.

## How to Invoke

### As a User
```
/db-health
```

### As Another Agent
```
Before running any database-dependent operation, read and follow:
skills/db-health/SKILL.md
```

## Execution Steps

### Step 1: Test MySQL Connectivity
Run a quick connectivity test using the DATABASE_URL from `.env`:
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
.venv\Scripts\python -c "
from sqlalchemy import create_engine, text
from app.core.config import get_settings
settings = get_settings()
engine = create_engine(settings.database_url, pool_pre_ping=True)
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print(f'MySQL connection: OK')
    result = conn.execute(text('SELECT VERSION()'))
    print(f'MySQL version: {result.scalar()}')
    result = conn.execute(text('SELECT DATABASE()'))
    print(f'Database: {result.scalar()}')
"
```

If this fails, check:
- Is the MySQL host reachable? `ping 103.108.220.145`
- Is port 3306 open? `Test-NetConnection 103.108.220.145 -Port 3306`
- Are credentials correct in `.env`?
- Is the database created? (May need to create it — see §7.2)

### Step 2: Check Alembic Migration State
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
.venv\Scripts\python -m alembic current
.venv\Scripts\python -m alembic check
```

Expected: migration head matches current database state.

### Step 3: Verify Table Existence
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
.venv\Scripts\python -c "
from sqlalchemy import create_engine, inspect
from app.core.config import get_settings
settings = get_settings()
engine = create_engine(settings.database_url)
inspector = inspect(engine)
tables = inspector.get_table_names()
required = ['policies', 'policy_versions', 'evaluations', 'evaluation_rule_results', 'audit_logs']
for t in required:
    status = '✅' if t in tables else '❌'
    print(f'{status} {t}')
if set(required) <= set(tables):
    print('\nAll required tables present!')
else:
    missing = set(required) - set(tables)
    print(f'\nMISSING: {missing}')
"
```

### Step 4: Verify Column Structure (Spec §11)
For each table, verify columns match the spec:

**policies** must have: `id`, `name`, `description`, `domain`, `status`, `priority`, `decision`, `conditions_json`, `reason`, `source`, `current_version`, `ai_metadata_json`, `created_by`, `approved_by`, `created_at`, `updated_at`, `activated_at`, `disabled_at`

**policy_versions** must have: `id`, `policy_id`, `version`, `name`, `description`, `domain`, `status_snapshot`, `priority`, `decision`, `conditions_json`, `reason`, `source`, `ai_metadata_json`, `created_by`, `approved_by`, `created_at`

**evaluations** must have: `id`, `request_id`, `domain`, `customer_id`, `request_json`, `decision`, `decision_confidence`, `winning_policy_id`, `winning_policy_version`, `resolution_json`, `explanation_json`, `metrics_json`, `warnings_json`, `correlation_id`, `created_by`, `evaluated_at`

**evaluation_rule_results** must have: `id`, `evaluation_id`, `policy_id`, `policy_version`, `policy_name`, `priority`, `decision`, `result_status`, `matched`, `condition_results_json`, `missing_fields_json`, `reason`, `created_at`

**audit_logs** must have: `id`, `action`, `entity_type`, `entity_id`, `entity_version`, `performed_by`, `summary`, `request_snapshot_json`, `result_snapshot_json`, `metadata_json`, `correlation_id`, `created_at`

### Step 5: Verify Indexes
Key indexes to check:
- `policies`: domain, status, priority, decision
- `evaluations`: customer_id, decision, evaluated_at, winning_policy_id, correlation_id
- `audit_logs`: action, entity_type, entity_id, performed_by, created_at, correlation_id

### Step 6: Test Health Check Function
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
.venv\Scripts\python -c "
from app.db.session import SessionLocal
from app.db.init_db import check_database_health
db = SessionLocal()
try:
    healthy = check_database_health(db)
    print(f'Health check: {\"✅ HEALTHY\" if healthy else \"❌ UNHEALTHY\"}')
finally:
    db.close()
"
```

### Step 7: Generate Report
```
╔══════════════════════════════════════════╗
║       DATABASE HEALTH REPORT             ║
╠══════════════════════════════════════════╣
║ MySQL Connection:    ✅ / ❌              ║
║ MySQL Version:       X.X.X               ║
║ Database Exists:     ✅ / ❌              ║
║ Migration Current:   ✅ / ❌              ║
║ Tables (5/5):        ✅ / ❌              ║
║ Columns Match Spec:  ✅ / ❌              ║
║ Indexes Present:     ✅ / ❌              ║
║ Health Check Fn:     ✅ / ❌              ║
╚══════════════════════════════════════════╝
```

## Common Fixes
| Issue | Fix |
|---|---|
| Connection refused | Check if MySQL is running and port 3306 is accessible |
| Access denied | Verify credentials in `.env` match the MySQL user |
| Database not found | Run: `CREATE DATABASE decisionflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;` |
| Tables missing | Run: `alembic upgrade head` |
| Migration mismatch | Run: `alembic revision --autogenerate -m "fix"` then `alembic upgrade head` |
