BACKEND PRE-HANDOFF VALIDATION

Branch:
feature/backend-rule-engine

Complete every applicable step and return the requested report.

Run all initial commands from the repository root.

==================================================
1. BRANCH SYNCHRONIZATION
==================================================

git fetch origin
git switch feature/backend-rule-engine
git pull --ff-only origin feature/backend-rule-engine
git merge origin/main

Resolve conflicts and then run:

git status
git push origin feature/backend-rule-engine
git rev-parse HEAD
git log -1 --oneline

Expected:
- Branch is feature/backend-rule-engine
- Latest main has been merged
- Working tree is clean
- Commit is pushed

==================================================
2. BACKEND FILE OWNERSHIP CHECK
==================================================

git diff --name-status origin/main...HEAD

Expected backend changes should primarily be under:

backend/app/api/v1/config.py
backend/app/api/v1/policies.py
backend/app/api/v1/analytics.py
backend/app/api/v1/audit.py
backend/app/core/
backend/app/schemas/
backend/app/models/
backend/app/repositories/
backend/app/services/
backend/app/engine/
backend/app/db/
backend/alembic/
backend/tests/
backend/requirements.txt
backend/Dockerfile
backend/alembic.ini

Any change to these shared files must be called out:

backend/app/main.py
backend/app/api/dependencies.py
backend/app/core/error_handlers.py
backend/app/schemas/common.py
docker-compose.yml
README.md
docs/contracts/02_API_CONTRACT.md

The Integration Lead remains final owner of application wiring and shared contracts.

==================================================
3. DEPENDENCY AND CONFIGURATION CHECK
==================================================

cd backend

python3 --version

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

python -m pip check

Expected:
- Python 3.11 or newer
- Installation completes successfully
- pip check reports:
  No broken requirements found

Confirm requirements include equivalents of:

fastapi
uvicorn[standard]
pydantic
pydantic-settings
sqlalchemy
pymysql
alembic
python-dotenv
cryptography
pytest
pytest-asyncio
httpx

Confirm backend/.env.example documents all required settings without real secrets.

==================================================
4. MYSQL COMPOSE VALIDATION
==================================================

Return to the repository root:

cd ..

docker compose config

docker compose up -d mysql
docker compose ps
docker compose logs mysql --tail=50

Expected:
- docker compose config succeeds
- MySQL container is running
- MySQL eventually reports healthy
- No restart loop
- No authentication or initialization error

Run:

docker compose exec mysql \
  mysqladmin ping \
  -h localhost \
  -uroot \
  -proot

Expected:

mysqld is alive

Run:

docker compose exec mysql \
  mysql -udecisionflow -pdecisionflow \
  -Nse \
  "SELECT VERSION(), DATABASE();" \
  decisionflow

Expected:
- MySQL version is 8.x
- Selected database is decisionflow

Check charset and collation:

docker compose exec mysql \
  mysql -uroot -proot \
  -Nse \
  "SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
   FROM information_schema.SCHEMATA
   WHERE SCHEMA_NAME='decisionflow';"

Expected:

utf8mb4    utf8mb4_unicode_ci

If collation differs, document and correct it unless approved.

==================================================
5. ALEMBIC MIGRATION VALIDATION
==================================================

cd backend
source .venv/bin/activate

alembic heads
alembic current
alembic upgrade head
alembic current

Expected:
- Exactly one intended Alembic head, unless multiple heads are explicitly justified
- alembic upgrade head completes without error
- alembic current matches the head revision

Run:

alembic check

Expected:
- No new upgrade operations detected

If your Alembic version does not support alembic check, state that in the report.

List tables:

cd ..

docker compose exec mysql \
  mysql -udecisionflow -pdecisionflow \
  -e "SHOW TABLES;" \
  decisionflow

Expected core tables:

policies
policy_versions
evaluations
evaluation_rule_results
audit_logs
alembic_version

Equivalent names require explanation and approval.

==================================================
6. CLEAN DATABASE MIGRATION TEST
==================================================

This test must be done using disposable local data only.

Confirm no local data needs to be preserved before running:

docker compose down -v
docker compose up -d mysql

Wait until MySQL is healthy:

docker compose ps

Then:

cd backend
source .venv/bin/activate
alembic upgrade head

Expected:
- A completely empty MySQL instance migrates successfully
- No manual SQL intervention is required
- All expected tables are created

This proves migrations work from scratch rather than only on an already-modified database.

==================================================
7. SEED IDEMPOTENCY VALIDATION
==================================================

Run from backend:

python -m app.db.seed

Expected:
- Seed succeeds
- Demo policies are inserted
- No exception

Record the policy count:

cd ..

SEED_COUNT_1=$(
  docker compose exec -T mysql \
    mysql -udecisionflow -pdecisionflow \
    -Nse "SELECT COUNT(*) FROM policies;" \
    decisionflow
)

echo "Policy count after first seed: ${SEED_COUNT_1}"

Run the seed again:

cd backend
python -m app.db.seed
cd ..

SEED_COUNT_2=$(
  docker compose exec -T mysql \
    mysql -udecisionflow -pdecisionflow \
    -Nse "SELECT COUNT(*) FROM policies;" \
    decisionflow
)

echo "Policy count after second seed: ${SEED_COUNT_2}"

test "${SEED_COUNT_1}" = "${SEED_COUNT_2}" \
  && echo "SEED_IDEMPOTENCY_OK" \
  || echo "SEED_DUPLICATE_PROBLEM"

Expected:

SEED_IDEMPOTENCY_OK

The second seed run must not:
- Create duplicate policies
- Fail because of unique constraints
- Create unintended policy versions
- Corrupt active policy state

==================================================
8. NO SQLITE OR IN-MEMORY APPLICATION FALLBACK
==================================================

Run:

grep -RniE \
'sqlite|:memory:|in.memory|in_memory' \
backend/app \
backend/alembic \
--exclude-dir=__pycache__ \
|| true

Expected:
- No runtime SQLite configuration
- No in-memory repository fallback used by application startup

In-memory fixtures are acceptable only inside unit tests for the pure rule engine.

==================================================
9. STABLE IMPORT VALIDATION
==================================================

From the repository root:

PYTHONPATH=backend python - <<'PY'
from app.services.policy_service import PolicyService
from app.engine.evaluator import RuleEngine
from app.engine.resolver import PriorityResolver
from app.engine.confidence import DecisionConfidenceCalculator
from app.repositories.evaluation_repository import EvaluationRepository
from app.services.audit_service import AuditService
from app.services.analytics_service import AnalyticsService

print("BACKEND_INTEGRATION_IMPORTS_OK")
PY

Expected:

BACKEND_INTEGRATION_IMPORTS_OK

If an import path differs, provide the exact final import. Do not leave the Integration Lead guessing.

Also provide exact callable signatures for:

policy_service.get_active_policies(domain)
rule_engine.evaluate(request_data, policies)
priority_resolver.resolve(matched_policies)
confidence_calculator.calculate(...)
evaluation_repository.save(...)
audit_service.record_decision(...)
analytics_service.get_summary(...)

==================================================
10. AUTOMATED TESTS
==================================================

From backend:

pytest -q

Expected:
- Zero failed
- Zero errors
- Exact passed/skipped count provided

Run focused tests if these paths exist:

pytest tests/test_operators.py -q
pytest tests/test_evaluator.py -q
pytest tests/test_resolver.py -q
pytest tests/test_confidence.py -q
pytest tests/test_policy_service.py -q
pytest tests/test_repositories.py -q
pytest tests/test_api_policies.py -q
pytest tests/test_analytics.py -q
pytest tests/test_audit.py -q

Do not invent missing paths. Run the actual equivalent tests and list their names.

Required rule-engine test coverage:

- Every supported operator
- all condition group
- any condition group
- One nested condition level
- Incorrect value type
- Missing field
- Approval match
- Fraud rejection match
- Multiple matching rules
- Priority resolution
- Severity tie-breaker
- Deterministic confidence
- No-match behavior
- Condition-level traces
- Same input returns same output

Expected:
- All critical tests pass
- No test depends on a live AI provider
- Rule-engine tests do not require MySQL unless specifically testing persistence

==================================================
11. START API
==================================================

Run from backend:

uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  > /tmp/decisionflow-backend.log 2>&1 &

API_PID=$!

sleep 5

curl --fail --silent --show-error \
  http://127.0.0.1:8000/openapi.json \
  > /tmp/decisionflow-openapi.json

echo "API_PID=${API_PID}"

Expected:
- Uvicorn starts
- openapi.json returns HTTP 200
- No import or startup errors

If startup fails:

cat /tmp/decisionflow-backend.log

==================================================
12. SYSTEM AND CONFIG ENDPOINTS
==================================================

curl -i http://127.0.0.1:8000/health

Expected:
- HTTP 200

curl -i http://127.0.0.1:8000/ready

Expected:
- HTTP 200 when database is ready
- Database dependency reported available
- Rule-engine capability reported available after backend integration

curl -sS \
  -H "X-Correlation-ID: cor_backend_handoff_001" \
  -D /tmp/backend-headers.txt \
  http://127.0.0.1:8000/api/v1/config/fields \
  | python -m json.tool

grep -i "X-Correlation-ID: cor_backend_handoff_001" \
  /tmp/backend-headers.txt

Expected:
- HTTP 200
- success is true
- data is a non-empty field catalogue
- correlation_id is present
- response header preserves cor_backend_handoff_001

Run:

curl -sS \
  http://127.0.0.1:8000/api/v1/config/operators \
  | python -m json.tool

Expected:
- HTTP 200
- success is true
- operator list is non-empty
- supported data types are present

==================================================
13. POLICY API VALIDATION
==================================================

First verify seeded policies:

curl -sS \
  "http://127.0.0.1:8000/api/v1/policies?page=1&page_size=20" \
  | tee /tmp/policies.json \
  | python -m json.tool

Expected:
- HTTP 200
- success is true
- data is a list
- meta contains page, page_size, total_items, total_pages
- correlation_id is present

Verify filters:

curl -sS \
  "http://127.0.0.1:8000/api/v1/policies?status=ACTIVE&sort_by=priority&sort_order=desc" \
  | python -m json.tool

Expected:
- Only ACTIVE policies
- Highest priority first
- Valid pagination envelope

Create a unique draft:

POLICY_NAME="Handoff approval $(date +%s)"

cat > /tmp/create-policy.json <<EOF
{
  "name": "${POLICY_NAME}",
  "description": "Backend handoff validation policy.",
  "domain": "telecom",
  "priority": 100,
  "decision": "APPROVE",
  "conditions": {
    "all": [
      {
        "field": "customer_tenure_months",
        "operator": "greater_than_or_equal",
        "value": 24
      },
      {
        "field": "payment_defaults",
        "operator": "equals",
        "value": 0
      },
      {
        "field": "credit_score",
        "operator": "greater_than_or_equal",
        "value": 750
      },
      {
        "field": "fraud_risk_score",
        "operator": "less_than",
        "value": 0.6
      }
    ]
  },
  "reason": "Validates backend policy lifecycle.",
  "source": "MANUAL"
}
EOF

curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  -H "X-User-ID: backend_handoff_user" \
  -H "X-User-Role: POLICY_MANAGER" \
  --data @/tmp/create-policy.json \
  http://127.0.0.1:8000/api/v1/policies \
  | tee /tmp/create-policy-response.json \
  | python -m json.tool

Expected:
- HTTP 201
- success is true
- status is DRAFT
- returned ID is a string
- source is MANUAL
- correlation_id is present

Extract the policy ID using the implemented response structure. If jq is installed:

POLICY_ID=$(
  jq -r '.data.id' \
  /tmp/create-policy-response.json
)

echo "${POLICY_ID}"

Expected:
- Non-empty ID beginning with the agreed policy-ID format

Retrieve it:

curl -sS \
  "http://127.0.0.1:8000/api/v1/policies/${POLICY_ID}" \
  | python -m json.tool

Expected:
- HTTP 200
- Same policy
- Status DRAFT

Activate it:

curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  -H "X-User-ID: backend_handoff_approver" \
  -H "X-User-Role: POLICY_MANAGER" \
  --data '{
    "approval_comment": "Reviewed during backend handoff."
  }' \
  "http://127.0.0.1:8000/api/v1/policies/${POLICY_ID}/activate" \
  | python -m json.tool

Expected:
- HTTP 200
- Status ACTIVE
- Immutable policy version created
- Approver captured
- Audit record created
- correlation_id present

Disable it:

curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  -H "X-User-ID: backend_handoff_approver" \
  --data '{
    "reason": "Backend handoff lifecycle completed."
  }' \
  "http://127.0.0.1:8000/api/v1/policies/${POLICY_ID}/disable" \
  | python -m json.tool

Expected:
- HTTP 200
- Status DISABLED
- Audit record created

==================================================
14. POLICY VALIDATION ERROR CASES
==================================================

Unsupported field:

curl -i \
  -X POST \
  -H "Content-Type: application/json" \
  --data '{
    "name": "Invalid field policy",
    "domain": "telecom",
    "priority": 100,
    "decision": "APPROVE",
    "conditions": {
      "all": [
        {
          "field": "customer_loyalty_aura",
          "operator": "greater_than",
          "value": 80
        }
      ]
    },
    "source": "MANUAL"
  }' \
  http://127.0.0.1:8000/api/v1/policies

Expected:
- HTTP 400 or contract-approved validation status
- success false
- error.code is POLICY_VALIDATION_ERROR
- details identify unsupported field
- correlation_id present

Duplicate name:

Repeat a create request using the same valid policy name.

Expected:
- HTTP 409
- error.code is DUPLICATE_POLICY_NAME
- correlation_id present

Incorrect numeric type:

Send credit_score as a string such as "high".

Expected:
- HTTP 400 or 422 according to the contract implementation
- Standard error envelope
- Path to incorrect value
- No database row created

==================================================
15. RULE-ENGINE BUSINESS PROOF
==================================================

Provide actual test output or a small executable script for:

A. Approval

Input:
- tenure 36
- payment defaults 0
- credit score 790
- fraud risk 0.12

Expected:
- Approval policy matches
- Complete condition trace
- Decision candidate APPROVE

B. Fraud rejection

Input:
- fraud risk 0.91
- A high-priority fraud rejection policy exists

Expected:
- Fraud rejection policy matches
- REJECT candidate
- Rejection wins over lower-priority approval when both match

C. Missing field

Remove credit_score from a request requiring it.

Expected:
- No crash
- Policy marked SKIPPED_MISSING_FIELD or contract-equivalent
- missing_fields contains credit_score
- Condition trace remains available

D. Priority resolution

Two policies match:
- REJECT priority 300
- APPROVE priority 100

Expected:
- Both matches retained in trace
- REJECT priority 300 wins
- Resolution strategy is deterministic

E. Repeatability

Execute the same case at least five times.

Expected:
- Same matched policies
- Same winning policy
- Same decision
- Same deterministic confidence

==================================================
16. PERSISTENCE VALIDATION
==================================================

Provide a direct service-level test or repository test proving:

- Evaluation can be inserted
- Rule-level results can be inserted
- Correlation ID is stored
- Winning policy/version is stored
- Audit event is inserted
- Transaction rolls back on forced failure

Run after a persistence test:

cd ..

docker compose exec mysql \
  mysql -udecisionflow -pdecisionflow \
  -e "
    SELECT id, request_id, decision, decision_confidence,
           winning_policy_id, correlation_id
    FROM evaluations
    ORDER BY evaluated_at DESC
    LIMIT 5;
  " \
  decisionflow

docker compose exec mysql \
  mysql -udecisionflow -pdecisionflow \
  -e "
    SELECT evaluation_id, policy_id, policy_version,
           matched, result_status
    FROM evaluation_rule_results
    ORDER BY created_at DESC
    LIMIT 10;
  " \
  decisionflow

docker compose exec mysql \
  mysql -udecisionflow -pdecisionflow \
  -e "
    SELECT action, entity_type, entity_id,
           performed_by, correlation_id, created_at
    FROM audit_logs
    ORDER BY created_at DESC
    LIMIT 10;
  " \
  decisionflow

Expected:
- Relevant stored records exist
- IDs are linked correctly
- Correlation IDs are present
- Rule traces belong to the correct evaluation

==================================================
17. AUDIT AND ANALYTICS APIs
==================================================

curl -sS \
  http://127.0.0.1:8000/api/v1/audit \
  | python -m json.tool

Expected:
- HTTP 200
- Standard success envelope
- Policy activation/disable events appear
- Correlation IDs appear

curl -sS \
  "http://127.0.0.1:8000/api/v1/analytics/summary?domain=telecom" \
  | python -m json.tool

curl -sS \
  "http://127.0.0.1:8000/api/v1/analytics/decision-distribution?domain=telecom" \
  | python -m json.tool

curl -sS \
  "http://127.0.0.1:8000/api/v1/analytics/decision-trend?domain=telecom" \
  | python -m json.tool

curl -sS \
  "http://127.0.0.1:8000/api/v1/analytics/top-policies?domain=telecom" \
  | python -m json.tool

Expected:
- HTTP 200
- Standard envelopes
- Valid numeric results
- Zero-state works when there are no evaluations
- Results update after evaluations are stored

==================================================
18. SWAGGER CONTRACT
==================================================

Open:

http://127.0.0.1:8000/docs

Also inspect:

python - <<'PY'
import json

with open("/tmp/decisionflow-openapi.json") as f:
    specification = json.load(f)

required_paths = [
    "/api/v1/config/fields",
    "/api/v1/config/operators",
    "/api/v1/policies",
    "/api/v1/policies/{policy_id}",
    "/api/v1/policies/{policy_id}/activate",
    "/api/v1/policies/{policy_id}/disable",
    "/api/v1/analytics/summary",
    "/api/v1/audit",
]

missing = [
    path
    for path in required_paths
    if path not in specification.get("paths", {})
]

print("Missing paths:", missing)
assert not missing, missing
print("BACKEND_OPENAPI_PATHS_OK")
PY

Expected:

Missing paths: []
BACKEND_OPENAPI_PATHS_OK

==================================================
19. STOP LOCAL API
==================================================

kill "${API_PID}"

==================================================
20. REQUIRED BACKEND HANDOFF RESPONSE
==================================================

Return:

BACKEND MODULE HANDOFF

Branch:
feature/backend-rule-engine

Latest full commit hash:

Latest main merged:
Yes / No

Working tree clean:
Yes / No

Completed:
- MySQL models and migrations
- Policy CRUD
- Policy activation
- Policy disable
- Immutable policy versions
- Operator catalogue
- Field catalogue
- Rule engine
- Priority resolver
- Confidence calculator
- Evaluation persistence
- Rule-trace persistence
- Audit
- Analytics
- Seed
- Dockerfile
- Tests

Not completed:
-

Setup commands:
-

Migration result:
-

Migration head:
-

Clean database migration result:
-

Seed run 1 result:
-

Seed run 2 result:
-

Seed count after run 1:
-

Seed count after run 2:
-

Full test command:
-

Full test result:
<pasted pytest summary>

Focused test results:
-

Stable imports:
<exact Python import statements>

Exact method signatures:
-

Completed endpoints:
-

Incomplete endpoints:
-

Example policy ID:
-

Approval engine output:
-

Fraud rejection engine output:
-

Missing-field output:
-

Priority-resolution output:
-

Persistence proof:
-

Audit proof:
-

Analytics proof:
-

Swagger result:
-

Required environment variables:
-

Known limitations:
-

API contract deviations:
None / exact list

Database-design deviations:
None / exact list

Shared files modified:
-

Files likely to conflict during merge:
-

Integration Lead action required:
-

Do not request merge unless all applicable checks pass.