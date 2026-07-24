# DecisionFlow AI
## Git Workflow, Branching, Handoff, Merge, and Release Guide

**Document ID:** DFA-GIT-008  
**Version:** 1.0  
**Status:** Hackathon POC Baseline  
**Primary Owner:** Technical Architect and Integration Lead  
**Applies To:** All four team members  
**Repository Type:** Single monorepo  
**Main Branch:** `main`  
**Integration Branch:** `feature/integration`

---

# 1. Purpose

This document defines how the four-person team will use Git to develop DecisionFlow AI safely in parallel.

The purpose is to prevent:

- Developers overwriting each other's work
- Last-minute integration failures
- Unclear code ownership
- Silent API-contract changes
- Duplicate files and competing implementations
- Unreviewed merges into `main`
- Broken Docker or environment configuration
- Secrets being committed
- Large, untraceable commits
- Lost work during conflict resolution

The Git workflow must allow:

```text
Backend Engineer
AI Engineer
Frontend Engineer
Integration Lead
```

to work independently while still producing one clean, stable application.

The central rule is:

> Every module may evolve internally, but shared contracts, shared schemas, and integration files must change only through controlled review.

---

# 2. Repository Strategy

Use one monorepo.

```text
decisionflow-ai/
├── backend/
├── frontend/
├── docs/
├── scripts/
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

Do not use separate repositories for frontend, backend, and AI during the hackathon.

A monorepo is preferred because:

- Shared documents stay synchronized.
- Docker Compose remains centralized.
- Integration branches are simpler.
- The demo runs from one repository.
- Cross-module changes are visible.
- Handoffs require fewer moving parts.
- Versioning is easier.
- Reviewers can understand the entire solution in one place.

---

# 3. Branch Model

Use these primary branches:

```text
main
feature/backend-rule-engine
feature/ai-policy-studio
feature/frontend-dashboard
feature/integration
```

Optional short-lived branches may be created from a module branch.

Examples:

```text
feature/backend-rule-engine/mysql-models
feature/backend-rule-engine/policy-crud
feature/ai-policy-studio/mock-provider
feature/frontend-dashboard/policy-studio-ui
feature/integration/decision-service
```

For a short hackathon, deeply nested branches are optional. The main requirement is that nobody commits directly to `main`.

---

# 4. Branch Ownership

## `main`

Owner:

```text
Technical Architect and Integration Lead
```

Purpose:

- Stable, demo-ready code only
- Final release candidate
- Documentation matching implementation
- No half-finished work
- No experimental commits

Only the Integration Lead should merge into `main`.

---

## `feature/backend-rule-engine`

Owner:

```text
Backend and Rule Engine Engineer
```

Contains:

- MySQL
- SQLAlchemy
- Alembic
- Policy CRUD
- Rule engine
- Priority resolver
- Decision confidence
- Repositories
- Audit persistence
- Analytics queries
- Seed data
- Backend tests

---

## `feature/ai-policy-studio`

Owner:

```text
AI Engineer
```

Contains:

- Provider abstraction
- Mock provider
- Policy generator
- Ambiguity detector
- AI confidence
- Conflict explanation
- Decision explanation
- Test-case generation
- AI fallbacks
- AI tests
- Prompt versions

---

## `feature/frontend-dashboard`

Owner:

```text
Frontend Engineer
```

Contains:

- React app
- UI shell
- Dashboard
- AI Policy Studio
- Policy screens
- Decision Center
- Analytics
- Audit
- API client
- Mock mode
- Frontend tests

---

## `feature/integration`

Owner:

```text
Technical Architect and Integration Lead
```

Contains:

- Decision Service
- FastAPI app wiring
- Dependency injection
- Shared error handling
- CORS
- Health/readiness
- Docker Compose
- End-to-end tests
- README
- Cross-module fixes
- Final integration work

---

# 5. Branch Creation

Create branches from the same stable baseline.

```bash
git checkout main
git pull origin main

git checkout -b feature/backend-rule-engine
git push -u origin feature/backend-rule-engine
```

Repeat for:

```text
feature/ai-policy-studio
feature/frontend-dashboard
feature/integration
```

Nobody should create their module branch from another feature branch.

Correct:

```text
main
├── backend branch
├── AI branch
├── frontend branch
└── integration branch
```

Incorrect:

```text
main
└── backend branch
    └── AI branch
        └── frontend branch
```

---

# 6. Initial Baseline Commit

Before module development begins, the Integration Lead should create one baseline commit containing:

- Repository folder structure
- `.gitignore`
- `.env.example`
- Initial README
- Docker Compose MySQL skeleton
- FastAPI skeleton
- React skeleton
- Shared documentation
- Shared API contract
- Shared field catalogue
- Shared operator catalogue
- Branch naming rules

Recommended commit:

```text
chore: initialize decisionflow project structure
```

All feature branches must begin from this commit.

---

# 7. Daily or Session Start Workflow

Every developer should begin work with:

```bash
git checkout <their-branch>
git pull origin <their-branch>
git fetch origin
```

Then check if `main` or integration contains required shared updates.

If the Integration Lead announces a shared-contract update:

```bash
git merge origin/main
```

or:

```bash
git rebase origin/main
```

Use one agreed approach consistently.

For a hackathon, merge is simpler and safer for less experienced teams.

Recommended:

```text
Use merge, not rebase, for shared team branches.
```

---

# 8. Recommended Commit Style

Use small, meaningful commits.

Format:

```text
<type>: <clear action>
```

Recommended types:

```text
feat
fix
refactor
test
docs
chore
build
ci
perf
```

Examples:

```text
feat: add policy activation endpoint
fix: handle missing fraud risk field
test: add priority resolver coverage
docs: update AI provider setup
chore: add mysql health check
refactor: isolate evaluation response builder
build: add frontend dockerfile
```

Avoid vague messages:

```text
changes
update
fixes
done
final
new code
```

---

# 9. Commit Size

A commit should represent one coherent change.

Good:

```text
feat: add operator registry
test: add operator registry tests
```

Acceptable combined:

```text
feat: add operator registry with tests
```

Bad:

```text
feat: add mysql models frontend chart ai prompt docker and docs
```

Large mixed commits make conflict resolution and rollback difficult.

---

# 10. Commit Frequency

Commit whenever a meaningful unit works.

Recommended checkpoints:

- File structure completed
- Service interface created
- API endpoint working
- Test suite passing
- UI page complete
- Mock flow working
- Real API connected
- Migration verified
- Docker service working

Do not wait until the end of the day to make one giant commit.

---

# 11. Push Frequency

Push at least after every major working checkpoint.

Recommended:

```text
Every 30–60 minutes during active hackathon development
```

Push before:

- Taking a break
- Switching tasks
- Asking for integration
- Requesting review
- Resolving risky conflicts
- Running large refactors

A local-only branch is not a valid handoff.

---

# 12. Pull Before Push

Before pushing:

```bash
git pull origin <your-branch>
```

Resolve any branch-local updates.

Then:

```bash
git push origin <your-branch>
```

Do not use force push on shared branches.

---

# 13. Force Push Rule

Prohibited on:

```text
main
feature/integration
feature/backend-rule-engine
feature/ai-policy-studio
feature/frontend-dashboard
```

Allowed only on personal temporary branches when nobody else depends on them.

Never run:

```bash
git push --force
```

on a shared branch.

---

# 14. Shared Files and Ownership

Some files have a high risk of merge conflicts.

## Integration Lead ownership

```text
backend/app/main.py
backend/app/api/dependencies.py
backend/app/core/config.py
backend/app/core/error_handlers.py
backend/app/schemas/common.py
backend/app/schemas/decision.py
docker-compose.yml
README.md
.env.example
```

## Backend ownership

```text
backend/app/models/*
backend/app/repositories/*
backend/app/engine/*
backend/app/db/*
backend/alembic/*
```

## AI ownership

```text
backend/app/ai/*
backend/tests/ai/*
```

## Frontend ownership

```text
frontend/src/*
frontend/package.json
frontend/vite.config.ts
frontend/tailwind.config.*
```

If a developer needs to modify another owner's file, they should inform the owner before pushing.

---

# 15. Shared Contract Files

These files require Integration Lead approval before change:

```text
docs/02_API_CONTRACT.md
backend/app/schemas/common.py
backend/app/schemas/decision.py
frontend/src/types/api.ts
frontend/src/types/decision.ts
backend/app/core/domain_catalogue.py
backend/app/engine/operators.py
```

Any change here may affect multiple modules.

---

# 16. API Contract Change Process

If a developer discovers that the contract must change, they must submit:

```text
Current field or route:
Proposed change:
Reason:
Affected modules:
Backward compatible:
Required by demo:
```

Example:

```text
Current field:
explanation.summary

Proposed change:
Add explanation.generated_by

Reason:
Frontend must indicate deterministic fallback.

Affected:
Backend, AI, Frontend, Tests

Backward compatible:
Yes, optional field
```

The Integration Lead approves or rejects the change.

No developer may silently rename:

```text
decision_confidence
matched_policies
generated_policy
correlation_id
```

---

# 17. Pull Request Strategy

If the Git hosting platform supports pull requests, use them for module handoffs.

Recommended PRs:

```text
backend → integration
AI → integration
frontend → integration
integration → main
```

A PR does not need formal enterprise-level review, but it should include:

- Scope
- Setup
- Tests
- Screenshots or payloads
- Known limitations
- Contract deviations
- Handoff checklist

---

# 18. Pull Request Template

Create:

```text
.github/pull_request_template.md
```

Suggested content:

```markdown
## Summary

Describe what this PR adds.

## Module

- [ ] Backend
- [ ] AI
- [ ] Frontend
- [ ] Integration
- [ ] Documentation

## Completed

- 

## API contract impact

- [ ] No contract change
- [ ] Contract change approved and documented

## Database impact

- [ ] No schema change
- [ ] Alembic migration included

## Tests

Command:

Result:

## Setup changes

- 

## Known limitations

- 

## Handoff imports or routes

- 

## Screenshots or example responses

- 
```

---

# 19. Module Handoff Rule

A branch is not ready for integration until the owner provides:

- Branch name
- Latest commit hash
- Completed features
- Setup commands
- Test commands
- Test results
- Stable imports
- API routes
- Known limitations
- Contract deviations
- Required environment variables

The Integration Lead may reject incomplete handoffs.

---

# 20. Backend Handoff Example

```text
Branch:
feature/backend-rule-engine

Commit:
abc1234

Completed:
- MySQL models
- Alembic migration
- Policy CRUD
- Rule engine
- Priority resolver
- Seed data

Run:
docker compose up -d mysql
cd backend
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload

Tests:
pytest tests/test_evaluator.py -q
Result: 18 passed

Imports:
app.engine.evaluator.RuleEngine
app.engine.resolver.PriorityResolver
app.services.policy_service.PolicyService

Known limitations:
- Conflict detector supports simple numeric overlap only

Contract deviations:
- None
```

---

# 21. AI Handoff Example

```text
Branch:
feature/ai-policy-studio

Commit:
def5678

Completed:
- Provider abstraction
- Mock provider
- Policy generation
- Ambiguity detection
- Explanation
- Fallback

Run:
LLM_PROVIDER=mock
USE_MOCK_LLM=true

Tests:
pytest backend/tests/ai -q
Result: 22 passed

Imports:
app.ai.policy_generator.AIPolicyGenerator
app.ai.explainer.DecisionExplainer
app.ai.fallback.build_fallback_explanation

Known limitations:
- Live provider smoke test not run

Contract deviations:
- None
```

---

# 22. Frontend Handoff Example

```text
Branch:
feature/frontend-dashboard

Commit:
ghi9012

Completed:
- Dashboard
- Policy Studio
- Policies
- Decision Center
- Analytics
- Audit
- Mock mode
- Real API client

Run:
cd frontend
npm install
npm run dev

Tests:
npm run test:run
Result: 16 passed

Build:
npm run build
Result: passed

Known limitations:
- Mobile audit table uses horizontal scroll

Contract deviations:
- None
```

---

# 23. Integration Review Process

When a module is handed off, the Integration Lead should:

1. Fetch the branch.
2. Review file changes.
3. Run setup.
4. Run tests.
5. Verify stable imports.
6. Compare API output to contract.
7. Check for secrets.
8. Check for duplicate files.
9. Merge into integration branch.
10. Run integration tests.
11. Report accepted or rejected.

---

# 24. Fetching a Handoff Branch

```bash
git fetch origin
git checkout feature/integration
git pull origin feature/integration
git merge origin/feature/backend-rule-engine
```

Resolve conflicts with module owner available.

After merge:

```bash
pytest -q
```

Then push:

```bash
git push origin feature/integration
```

---

# 25. Merge Order

Recommended order into `feature/integration`:

```text
1. Backend structure and MySQL
2. Shared backend schemas
3. Rule engine
4. Policy service and CRUD
5. AI provider abstraction and mock provider
6. AI policy generation
7. AI explanation and fallback
8. Decision Service
9. Evaluation persistence
10. Audit and analytics
11. Frontend shell and mock mode
12. Frontend real API integration
13. Docker Compose
14. README and final docs
```

This order reduces unresolved dependencies.

---

# 26. Merge Strategy

Recommended:

```text
Merge commits for module handoffs
```

Example:

```bash
git merge --no-ff origin/feature/backend-rule-engine \
  -m "merge: integrate backend rule engine module"
```

Why:

- Preserves module history
- Makes rollback easier
- Clearly identifies handoff point
- Helps presentation and review

---

# 27. Squash Guidance

Squash may be used only for noisy personal temporary branches.

Do not squash away meaningful module history if it will make debugging harder.

For the hackathon:

```text
Module branch → integration: normal merge
Integration → main: normal merge or squash if history is extremely noisy
```

---

# 28. Conflict Resolution Process

When a merge conflict occurs:

1. Stop and identify file owner.
2. Open both versions.
3. Check API contract.
4. Preserve required behavior from both sides.
5. Ask module owner if semantics are unclear.
6. Run relevant tests.
7. Commit explicit conflict-resolution message.

Example:

```text
fix: resolve decision schema integration conflict
```

Never resolve a shared schema conflict by choosing one side blindly.

---

# 29. Conflict Categories

## Safe conflicts

Examples:

- Imports
- Formatting
- Documentation links

May be resolved by Integration Lead.

## Semantic conflicts

Examples:

- API response models
- Rule-engine output
- AI result shape
- Database transaction flow
- Frontend request payload

Must involve relevant owner.

## Environment conflicts

Examples:

- `requirements.txt`
- `package.json`
- `.env.example`
- Docker Compose

Integration Lead owns final resolution.

---

# 30. Conflict Resolution Checklist

After resolving:

- File compiles
- Imports resolve
- Type check passes
- Tests pass
- Contract matches
- No functionality lost
- No duplicate implementation remains
- No secret introduced
- Documentation updated if required

---

# 31. Duplicate File Prevention

Common duplicate risks:

```text
rule_engine.py
rules_engine.py
engine.py

config.py
settings.py

api_client.ts
apiClient.ts

policy_service.py
policies_service.py
```

Before merge:

```bash
find backend -type f | sort
find frontend/src -type f | sort
```

Choose one canonical file.

Delete obsolete duplicates.

---

# 32. Dependency File Ownership

## `backend/requirements.txt`

Backend owner may add backend libraries.

AI owner may propose AI libraries.

Integration Lead reviews final list.

Every new dependency must have a reason.

Avoid unnecessary additions.

## `frontend/package.json`

Frontend owner controls.

Integration Lead verifies build.

## `docker-compose.yml`

Integration Lead owns final version.

---

# 33. Dependency Update Rule

When adding a dependency, include:

```text
Package:
Version:
Purpose:
Module:
```

Example:

```text
Package:
pymysql

Purpose:
MySQL SQLAlchemy driver

Module:
Backend
```

Do not add packages “just in case.”

---

# 34. Environment Variable Change Rule

Any new environment variable must be added to:

```text
.env.example
README.md
Relevant module guide if critical
Docker Compose if needed
```

Never introduce an undocumented required variable.

---

# 35. Secret Management

Never commit:

```text
.env
API keys
MySQL passwords beyond demo defaults in examples
Private tokens
Credentials
Cloud secrets
```

Required `.gitignore` entries:

```text
.env
.env.*
!.env.example
*.pem
*.key
__pycache__/
.venv/
node_modules/
dist/
coverage/
.pytest_cache/
.vscode/
.idea/
```

---

# 36. Secret Scan Before Merge

Run:

```bash
git grep -n "sk-"
git grep -n "API_KEY="
git grep -n "PASSWORD="
git grep -n "BEGIN PRIVATE KEY"
```

Review all matches.

Demo defaults in `.env.example` are acceptable only when clearly non-secret.

---

# 37. Generated Files

Do not commit:

```text
node_modules
frontend/dist
Python virtual environments
MySQL data
coverage output
pytest caches
local logs
temporary JSON outputs
IDE settings
```

Commit only source, config templates, migrations, tests, and documentation.

---

# 38. MySQL Migration Workflow

Backend engineer creates migration:

```bash
alembic revision --autogenerate -m "add evaluation tables"
```

Then:

```bash
alembic upgrade head
```

Before handoff, provide:

- Revision ID
- Migration purpose
- Upgrade result
- Downgrade status
- Schema impact

Integration Lead verifies migration on a clean database.

---

# 39. Migration Merge Conflicts

Alembic conflicts may happen when two branches create separate heads.

Avoid this by:

- Backend engineer remains sole migration owner.
- Other developers do not create migrations.
- Schema requests go through backend owner.

If multiple heads appear:

```bash
alembic heads
```

Create merge revision only when necessary:

```bash
alembic merge -m "merge migration heads" <head1> <head2>
```

For the hackathon, prevention is preferred.

---

# 40. Shared Schema Synchronization

Whenever backend response schema changes, update:

```text
Backend Pydantic model
API contract
Frontend TypeScript type
Frontend mock fixture
Backend test
Frontend test
```

A schema change is not complete until all five are aligned.

---

# 41. Mock-to-Real Integration Rule

Frontend may develop with mocks.

Before final handoff:

1. Switch to real API mode.
2. Compare every payload.
3. Remove mock-only assumptions.
4. Keep mock mode as fallback.
5. Verify no mock route is used unintentionally.

Environment:

```text
VITE_USE_MOCK_API=false
```

---

# 42. Main Branch Protection

Recommended settings:

- No direct pushes except Integration Lead
- Pull request required when practical
- No force push
- No branch deletion until final integration verified
- Require passing checks if CI exists

If branch protection cannot be configured, the team must follow the rule manually.

---

# 43. Integration Branch Protection

Treat `feature/integration` as protected.

Only the Integration Lead should merge module branches into it.

Other developers may create fixes on their own branches and request another handoff.

---

# 44. Hotfix Workflow

If a critical bug is found after merge:

Create:

```text
hotfix/<short-description>
```

from `feature/integration` or `main`, depending on release stage.

Example:

```bash
git checkout feature/integration
git checkout -b hotfix/fallback-explanation
```

Fix, test, and merge back.

---

# 45. Bugfix Ownership

## Backend bug

Backend owner fixes on backend branch or hotfix branch.

## AI bug

AI owner fixes.

## Frontend bug

Frontend owner fixes.

## Cross-module bug

Integration Lead owns coordination.

## Demo blocker

Whoever can fix fastest may assist, but ownership and review remain clear.

---

# 46. Code Review Checklist

Before accepting a PR:

## General

- Scope is clear
- No unrelated changes
- Naming is consistent
- No secrets
- No dead code
- No duplicate files
- Documentation updated

## Backend

- API contract followed
- MySQL used
- Transactions safe
- Error handling present
- Tests pass

## AI

- Structured output
- Validation present
- No final decision by AI
- Fallback present
- Mock provider works

## Frontend

- API types match
- No business decision logic
- Loading/error/empty states
- Build passes
- Real API mode works

## Integration

- Full flow works
- CORS works
- Health/readiness work
- Docker works
- README accurate

---

# 47. Review Comment Style

Review comments should be specific.

Good:

```text
This response returns "manualReview" but the API contract requires "MANUAL_REVIEW". Please update the backend response, frontend type, and test fixture.
```

Bad:

```text
Wrong.
```

Good:

```text
This repository method commits internally, which prevents the activation service from keeping version creation and status update atomic. Please remove the commit and let the service own the transaction.
```

---

# 48. Test Requirements Before Push

## Backend

```bash
pytest -q
```

## AI

```bash
pytest backend/tests/ai -q
```

## Frontend

```bash
npm run typecheck
npm run test:run
npm run build
```

## Integration

```bash
pytest backend/tests/integration -q
docker compose config
```

A developer should not request merge while known critical tests fail unless the failure is explicitly documented and accepted.

---

# 49. Minimal CI Pipeline

If time permits, add GitHub Actions or equivalent.

Recommended jobs:

```text
backend-tests
frontend-typecheck
frontend-tests
frontend-build
docker-compose-config
```

Example structure:

```text
.github/workflows/ci.yml
```

Do not spend excessive time on CI before the MVP works locally.

---

# 50. Suggested CI Commands

Backend:

```bash
pip install -r backend/requirements.txt
pytest backend/tests -q
```

Frontend:

```bash
cd frontend
npm ci
npm run typecheck
npm run test:run
npm run build
```

Docker:

```bash
docker compose config
```

MySQL integration tests require a service container if enabled.

---

# 51. Documentation Commit Rules

Documentation changes should use:

```text
docs: update API contract for explanation fallback
docs: add MySQL reset procedure
docs: document frontend mock mode
```

Do not let implementation diverge from documentation.

---

# 52. README Update Timing

Update README when:

- Setup command changes
- New environment variable added
- Docker behavior changes
- New required migration added
- Demo flow changes
- Known limitation changes

The Integration Lead owns final README accuracy.

---

# 53. Branch Synchronization Checkpoints

At each major checkpoint:

```text
Checkpoint 1:
All branches created from baseline

Checkpoint 2:
Backend interfaces available
AI mock available
Frontend mock available

Checkpoint 3:
Policy flow integrated

Checkpoint 4:
Decision flow integrated

Checkpoint 5:
Full Docker demo stable
```

At each checkpoint, developers should push and tag or record commit hashes.

---

# 54. Optional Checkpoint Tags

Tags may be used:

```text
checkpoint-1-skeleton
checkpoint-2-modules
checkpoint-3-policy-flow
checkpoint-4-decision-flow
release-demo-v1
```

Create:

```bash
git tag checkpoint-3-policy-flow
git push origin checkpoint-3-policy-flow
```

This provides a safe rollback point.

---

# 55. Rollback Strategy

If a merge breaks integration:

1. Identify merge commit.
2. Decide whether to fix forward or revert.
3. For a major unstable merge, revert merge commit.

Example:

```bash
git revert -m 1 <merge-commit>
```

Do not manually delete random files to simulate rollback.

---

# 56. Stable Demo Tag

Before presentation, create:

```text
release-demo-v1
```

Only after:

- Docker works
- Tests pass
- Demo rehearsal succeeds
- Secrets checked
- README verified

Command:

```bash
git tag -a release-demo-v1 -m "Stable DecisionFlow AI demo"
git push origin release-demo-v1
```

---

# 57. Release Branch

A separate release branch is optional.

For a short hackathon:

```text
main + stable tag
```

is sufficient.

Do not create unnecessary branch complexity.

---

# 58. Final Integration Into Main

Recommended process:

```bash
git checkout main
git pull origin main
git merge --no-ff feature/integration \
  -m "release: integrate DecisionFlow AI hackathon POC"
```

Then run all verification again.

Push:

```bash
git push origin main
```

Tag stable release.

---

# 59. Final Pre-Merge Verification

Before `feature/integration → main`:

- Backend tests pass
- AI tests pass
- Integration tests pass
- Frontend type check passes
- Frontend tests pass
- Frontend build passes
- Docker Compose starts
- MySQL migration succeeds
- Seed succeeds
- Policy generation works
- Policy activation works
- Approval works
- Rejection works
- Manual review works
- Fallback explanation works
- Audit works
- Analytics works
- No secrets found
- README is accurate
- Docs are updated

---

# 60. Final Repository Cleanup

Before release:

- Remove debug print statements
- Remove unused mock-only code from production path
- Keep mock provider intentionally
- Remove duplicate files
- Remove commented-out dead code
- Remove temporary scripts
- Remove local data files
- Remove screenshots not needed
- Remove unused dependencies
- Format code
- Update documentation links

---

# 61. Final Branch Retention

Do not delete feature branches until:

- Main is stable
- Demo completed
- Stable tag exists
- No urgent rollback needed

Afterward, branches may be retained for review or deleted.

---

# 62. Team Communication Format

When sending progress, use:

```text
Module:
Current branch:
Latest commit:
Completed:
In progress:
Blocked by:
Need from:
Next handoff:
```

Example:

```text
Module:
AI

Current branch:
feature/ai-policy-studio

Latest commit:
def5678

Completed:
Mock provider and policy generation

In progress:
Decision explanation

Blocked by:
Final evaluation-result schema

Need from:
Integration Lead approval on explanation input

Next handoff:
45 minutes
```

This is more useful than “working on it.”

---

# 63. Blocker Escalation

A blocker should be raised immediately when:

- Shared schema missing
- API contract ambiguous
- Import path uncertain
- Required environment variable unknown
- MySQL migration conflict
- Another module response differs
- Build dependency broken
- Merge conflict semantic

Do not silently create a workaround that violates architecture.

---

# 64. Contract Freeze Point

Recommended contract freeze:

```text
Before frontend real API integration begins
```

After freeze:

- Only backward-compatible optional fields
- No route renaming
- No enum renaming
- No required-field changes without team approval

---

# 65. File Locking by Agreement

Git does not lock files automatically.

For high-risk files, use team agreement.

Example:

```text
“I am editing docker-compose.yml for the next 20 minutes. Please do not modify it until I push.”
```

Use this for:

```text
docker-compose.yml
main.py
common schemas
README.md
.env.example
```

---

# 66. Formatting Tools

Recommended backend:

```text
ruff
black
```

Recommended frontend:

```text
prettier
eslint
```

If formatters are introduced, configure once in baseline.

Do not reformat the entire repository late in the project because it creates huge conflicts.

---

# 67. Pre-Commit Hooks

Optional.

Useful checks:

```text
Trailing whitespace
Python formatting
Secret detection
Frontend formatting
```

Do not spend significant hackathon time on complex hook setup.

---

# 68. Large Binary Files

Do not commit:

```text
Videos
Large images
Database backups
MySQL volumes
Large model files
Audio
Build archives
```

If the frontend needs one small logo or illustration, optimize it before commit.

---

# 69. Documentation Directory

Recommended:

```text
docs/
├── 01_MASTER_ARCHITECTURE.md
├── 02_API_CONTRACT.md
├── 03_BACKEND_MODULE_GUIDE.md
├── 04_AI_MODULE_GUIDE.md
├── 05_FRONTEND_MODULE_GUIDE.md
├── 06_INTEGRATION_GUIDE.md
├── 07_DATABASE_DESIGN.md
├── 08_GIT_WORKFLOW.md
├── 09_DEMO_GUIDE.md
└── AI_ENGINEERING_LOG.md
```

All documents should be committed to the repository.

---

# 70. Commit Example Timeline

## Baseline

```text
chore: initialize decisionflow project structure
```

## Backend

```text
feat: add mysql policy models
feat: add alembic core schema migration
feat: add operator registry
feat: add deterministic rule evaluator
test: cover priority resolution
feat: add policy CRUD service
```

## AI

```text
feat: add llm provider abstraction
feat: add mock llm provider
feat: add structured policy generator
feat: add ambiguity detector
feat: add decision explanation fallback
```

## Frontend

```text
feat: add application shell
feat: add policy studio mock flow
feat: add decision center result view
feat: connect policy APIs
feat: connect decision evaluation API
```

## Integration

```text
feat: add decision service orchestration
feat: add health and readiness endpoints
build: integrate mysql backend and frontend compose services
test: add approval and fraud override integration tests
docs: finalize quick-start and demo flow
```

---

# 71. Commit Anti-Patterns

Avoid:

```text
final final
working now
all files
last change
everything
hackathon code
temp
```

Avoid commits that:

- Mix backend, frontend, AI, and docs without reason
- Include generated files
- Contain secrets
- Remove another owner's work
- Change contract silently
- Disable tests
- Comment out validation for demo

---

# 72. Test Failure Policy

If tests fail:

- Do not hide the failure
- Do not delete the test
- Identify whether contract or implementation is wrong
- Fix root cause
- Document known non-blocking failure only if accepted

Never commit:

```python
@pytest.mark.skip(reason="does not work")
```

for critical business flows merely to get a green build.

---

# 73. Temporary Workarounds

Temporary workaround requirements:

- Clearly marked
- Documented in known limitations
- Does not violate core architecture
- Has owner
- Has removal plan

Example acceptable:

```text
Mock provider used because live event network is unavailable.
```

Example unacceptable:

```text
Frontend hardcodes APPROVE because backend is incomplete.
```

---

# 74. Demo-Day Freeze

Recommended freeze:

```text
60–90 minutes before presentation
```

After freeze:

Allowed:

- P0 bug fixes
- Text correction
- Demo-data correction

Not allowed:

- Large refactor
- Dependency upgrade
- New page
- Schema redesign
- New provider
- New database migration unless critical

---

# 75. Demo-Day Stable Workflow

1. Checkout stable main.
2. Pull latest.
3. Verify tag.
4. Start Docker.
5. Run smoke test.
6. Do not switch branches during demo.
7. Do not pull new changes during demo.
8. Keep mock-provider fallback ready.
9. Keep reset procedure documented.
10. Keep terminal commands prepared.

---

# 76. Emergency Fix Before Demo

If a critical fix is necessary:

```bash
git checkout -b hotfix/demo-<issue>
```

Fix and test.

Merge into integration or main.

Create new tag:

```text
release-demo-v1.1
```

Do not edit source directly on `main` without commit.

---

# 77. Git Recovery Commands

## See status

```bash
git status
```

## See recent history

```bash
git log --oneline --graph --decorate -20
```

## Discard one local file change

```bash
git restore <file>
```

## Stash unfinished work

```bash
git stash push -m "temporary integration work"
```

## Restore stash

```bash
git stash pop
```

## Abort merge

```bash
git merge --abort
```

## Abort rebase

```bash
git rebase --abort
```

Use carefully.

---

# 78. Avoiding Lost Work

Before risky operation:

```bash
git status
git add .
git commit -m "chore: checkpoint before integration merge"
git push
```

or stash.

Never resolve a risky conflict with uncommitted local work.

---

# 79. Git Log for Demo or Review

Useful command:

```bash
git log --oneline --graph --all --decorate
```

This can demonstrate parallel module development and integration.

It is optional in presentation but useful for technical reviewers.

---

# 80. Ownership Matrix

| Area | Owner | Reviewer |
|---|---|---|
| Architecture | Integration Lead | Team |
| API contract | Integration Lead | All owners |
| MySQL | Backend Engineer | Integration Lead |
| Rule engine | Backend Engineer | Integration Lead |
| Policy CRUD | Backend Engineer | Integration Lead |
| AI provider | AI Engineer | Integration Lead |
| AI prompts | AI Engineer | Integration Lead |
| AI fallback | AI Engineer | Integration Lead |
| React UI | Frontend Engineer | Integration Lead |
| Frontend API types | Frontend Engineer | Integration Lead |
| Decision Service | Integration Lead | Backend + AI |
| Docker Compose | Integration Lead | Backend + Frontend |
| README | Integration Lead | Team |
| Demo release | Integration Lead | Team |

---

# 81. Definition of Ready for Integration

A module is ready when:

- Branch pushed
- Commit hash provided
- Tests pass
- Setup works
- Imports stable
- Contract followed
- Environment documented
- No secrets
- Known limitations listed
- Owner available for merge support

---

# 82. Definition of Integrated

A module is integrated when:

- Merged into integration branch
- Relevant tests pass
- Cross-module imports work
- Real API or service call works
- No contract mismatch
- Docker still starts
- End-to-end flow remains stable
- Integration branch pushed

---

# 83. Definition of Released

The POC is released when:

- Integration merged into main
- Stable tag created
- Docker stack works
- README works
- Full demo flow rehearsed
- No P0 or P1 bugs
- Secrets checked
- All documents committed

---

# 84. Final Git Checklist for Each Developer

Before handoff:

```text
[ ] On correct branch
[ ] Pulled latest branch
[ ] Changes committed
[ ] Meaningful commit messages
[ ] Branch pushed
[ ] Tests passed
[ ] No secrets
[ ] No generated files
[ ] No contract deviation
[ ] Handoff message prepared
```

---

# 85. Final Git Checklist for Integration Lead

Before final release:

```text
[ ] All module branches fetched
[ ] Handoffs accepted
[ ] Merge order followed
[ ] Conflicts reviewed with owners
[ ] Backend tests passed
[ ] AI tests passed
[ ] Integration tests passed
[ ] Frontend type check passed
[ ] Frontend tests passed
[ ] Frontend build passed
[ ] Docker Compose passed
[ ] MySQL migration passed
[ ] Seed passed
[ ] Smoke flow passed
[ ] Secrets scanned
[ ] README updated
[ ] Docs updated
[ ] Main merged
[ ] Stable tag created
```

---

# 86. Final Team Rule

The team should optimize for a stable, integrated product rather than individual code volume.

That means:

```text
Small commits
Frequent pushes
Early handoffs
Stable contracts
Clear ownership
Controlled merges
Visible limitations
Repeatable setup
One demo-ready main branch
```

The final measure of success is not:

```text
How many files each person wrote
```

It is:

```text
Whether the complete product runs reliably from one repository.
```
