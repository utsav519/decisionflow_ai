---
name: progress-sync
description: Tracks development progress by scanning built files, mapping them to the 6-phase plan, running available tests, updating PROGRESS.md, and creating structured git commits with resumability metadata.
---

# Progress Sync Agent

## Purpose
Scans the current state of the project, determines what has been built, runs tests, updates the living PROGRESS.md tracker, and creates structured git commits so any model can resume work.

## How to Invoke

### As a User
```
/progress-sync
```
Or after completing a specific step:
```
/progress-sync completed P3.4
```

### As Another Agent
```
At the end of each work session or phase completion, read and follow:
skills/progress-sync/SKILL.md
```

## Execution Steps

### Step 1: Scan Project Structure
List all files under `backend/app/` and `backend/tests/`:
```powershell
cd e:\code\hackathon\decisionflow_ai
Get-ChildItem -Path backend/app -Recurse -File | Select-Object FullName | Sort-Object FullName
Get-ChildItem -Path backend/tests -Recurse -File -ErrorAction SilentlyContinue | Select-Object FullName | Sort-Object FullName
```

### Step 2: Map Files to Phase Plan
Compare found files against the expected file list per phase:

**Phase 1 — Foundation:**
- [ ] `app/core/config.py`
- [ ] `app/core/exceptions.py`
- [ ] `app/core/error_handlers.py`
- [ ] `app/core/ids.py`
- [ ] `app/core/logging.py`
- [ ] `app/db/base.py`
- [ ] `app/db/session.py`
- [ ] `app/db/init_db.py`
- [ ] `app/models/policy.py`
- [ ] `app/models/policy_version.py`
- [ ] `app/models/evaluation.py`
- [ ] `app/models/evaluation_rule_result.py`
- [ ] `app/models/audit.py`
- [ ] `app/main.py`
- [ ] `alembic/` directory
- [ ] `alembic.ini`
- [ ] `requirements.txt`

**Phase 2 — Schemas:**
- [ ] `app/schemas/common.py`
- [ ] `app/schemas/policy.py`
- [ ] `app/schemas/evaluation.py`
- [ ] `app/schemas/analytics.py`
- [ ] `app/schemas/audit.py`
- [ ] `app/core/domain_catalogue.py`

**Phase 3 — Engine:**
- [ ] `app/engine/operators.py`
- [ ] `app/engine/evaluator.py`
- [ ] `app/engine/resolver.py`
- [ ] `app/engine/confidence.py`
- [ ] `app/engine/result_models.py`
- [ ] `app/engine/exceptions.py`
- [ ] `tests/test_operators.py`
- [ ] `tests/test_evaluator.py`
- [ ] `tests/test_resolver.py`
- [ ] `tests/test_confidence.py`

**Phase 4 — Policy CRUD:**
- [ ] `app/api/dependencies.py`
- [ ] `app/repositories/policy_repository.py`
- [ ] `app/repositories/policy_version_repository.py`
- [ ] `app/repositories/audit_repository.py`
- [ ] `app/services/policy_service.py`
- [ ] `app/services/validation_service.py`
- [ ] `app/services/audit_service.py`
- [ ] `app/api/v1/policies.py`
- [ ] `app/api/v1/config.py`
- [ ] `app/db/seed.py`
- [ ] `tests/test_validation_service.py`
- [ ] `tests/test_policy_repository.py`
- [ ] `tests/test_policy_service.py`
- [ ] `tests/test_policy_api.py`

**Phase 5 — Analytics:**
- [ ] `app/repositories/evaluation_repository.py`
- [ ] `app/repositories/analytics_repository.py`
- [ ] `app/services/analytics_service.py`
- [ ] `app/api/v1/analytics.py`
- [ ] `app/api/v1/audit.py`
- [ ] `tests/test_analytics_api.py`
- [ ] `tests/test_audit_api.py`

**Phase 6 — Packaging:**
- [ ] `Dockerfile`
- [ ] `entrypoint.sh`
- [ ] `tests/conftest.py`

### Step 3: Run Available Tests
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
.venv\Scripts\python -m pytest -v --tb=short 2>&1
```

Parse results to get: passed, failed, skipped, errors.

### Step 4: Determine Current Phase
Based on file scan and test results, determine:
- Current phase (1-6)
- Current step within phase
- Next step to complete
- Any blockers

### Step 5: Update PROGRESS.md
Update `backend/PROGRESS.md` with:
- Current phase and step
- Last commit hash
- File completion checklist
- Test results table
- Next action
- Blockers

### Step 6: Create Structured Git Commit
Stage and commit with this format:
```
[P{phase}.{step}] {descriptive action}

PROGRESS: Phase {X} step {Y} of {Z} complete
NEXT: P{X}.{Y+1} — {description} at {file_path} per §{section}
BLOCKED: {blockers or "none"}
TESTS: {passed} passed, {failed} failed, {skipped} skipped
SPEC_REF: §{relevant sections}
```

Example:
```powershell
cd e:\code\hackathon\decisionflow_ai
git add backend/
git commit -m "[P3.4] add recursive condition evaluator

PROGRESS: Phase 3 step 4 of 10 complete
NEXT: P3.5 — add priority resolver at app/engine/resolver.py per §22
BLOCKED: none
TESTS: 24 passed, 0 failed, 0 skipped
SPEC_REF: §20, §21"
```

### Step 7: Tag if Milestone Reached
| Phase Complete | Tag | Handoff |
|---|---|---|
| Phase 1 | `v0.1-foundation` | — |
| Phase 2 | `v0.2-schemas` | — |
| Phase 3 | `v0.3-engine` | **Handoff 1** |
| Phase 4 | `v0.4-policy-crud` | **Handoff 2** |
| Phase 5 | `v0.5-analytics` | **Handoff 3** |
| Phase 6 | `v1.0-handoff` | **Final** |

```powershell
git tag -a v0.X-name -m "Phase X complete: description"
```

## Important Rules
- NEVER commit `.env` — it's in `.gitignore`
- ALWAYS include PROGRESS/NEXT/BLOCKED/TESTS metadata in commits
- The PROGRESS.md file is the single source of truth for resumability
- Any model reading the last 3 git commits should understand the project state
