# DecisionFlow AI

AI-assisted configurable decision automation platform demonstrated through telecom device-upgrade eligibility and risk decisioning.

> **Core principle:** AI assists with policy authoring, clarification, conflict analysis, test generation and explanations. The final business decision is always produced by the deterministic rule engine.

## Current status

The complete POC is integrated and demo-ready on:

```text
feature/integration
```

Validated capabilities:

- Deterministic policy evaluation and priority-based conflict resolution
- Decision-confidence calculation
- AI-assisted policy authoring and decision explanation
- Deterministic fallback when AI is unavailable
- MySQL persistence with Alembic migrations
- Condition-level evaluation trace and audit trail
- Correlation-ID propagation across API, persistence, logs and audit
- React Decision Center connected to the live backend
- Approval, rejection, missing-field and AI-failure flows

Validation baseline:

```text
Backend: 140 tests passed
Frontend: production build passed
Frontend: ESLint passed
Browser E2E: approval, rejection and missing-field flows passed
AI failure E2E: deterministic fallback and audit records passed
```

## Architecture

```text
React Decision Center
        |
        v
FastAPI REST API
        |
        v
DecisionService orchestration
        |
        +-------------------------------+
        |                               |
        v                               v
Deterministic Rule Engine        AI Services
        |                         - policy generation
        |                         - clarification
        |                         - conflict analysis
        |                         - explanation
        |                               |
        +---------------+---------------+
                        |
                        v
             MySQL + Audit Trail
```

### Decision workflow

1. Validate the request.
2. Load active policies for the requested domain.
3. Evaluate policy conditions deterministically.
4. Resolve multiple matches by priority.
5. Calculate decision confidence.
6. Generate an AI explanation when enabled.
7. Fall back to a deterministic explanation if AI is unavailable.
8. Persist the evaluation, trace, explanation and warnings.
9. Write decision and AI-failure audit records.
10. Return the response with the correlation ID.

AI output never changes the deterministic decision.

## Technology stack

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PyMySQL
- Alembic
- MySQL
- Pytest
- OpenAI, Groq, Google and Anthropic provider integrations
- Mock LLM provider for local development and repeatable demos

### Frontend

- React 19
- TypeScript
- Vite 8
- Axios
- Recharts
- ESLint

## Repository structure

```text
decisionflow_ai/
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── ai/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── engine/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── types/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── index.css
│   ├── .env.example
│   └── package.json
├── docs/
├── skills/
├── docker-compose.yml
└── README.md
```

## Prerequisites

- Git
- Docker and Docker Compose
- Python 3.12 recommended
- Node.js and npm

## Quick start

### 1. Clone and switch to the integrated branch

```bash
git clone https://github.com/utsav519/decisionflow_ai.git
cd decisionflow_ai
git switch feature/integration
```

### 2. Start MySQL

```bash
docker compose up -d mysql
docker compose ps
```

Wait until MySQL is healthy.

### 3. Configure the backend

```bash
cd backend
cp .env.example .env
```

Example local configuration:

```env
APP_NAME=DecisionFlow AI
APP_ENV=development
API_V1_PREFIX=/api/v1
LOG_LEVEL=INFO

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=decisionflow
MYSQL_USER=decisionflow
MYSQL_PASSWORD=your_password_here

DATABASE_URL=mysql+pymysql://decisionflow:your_password_here@localhost:3306/decisionflow

LLM_PROVIDER=mock
LLM_MODEL=mock-model
LLM_API_KEY=
USE_MOCK_LLM=true
ENABLE_AI_POLICY_GENERATION=true
ENABLE_AI_EXPLANATION=true

ALLOWED_ORIGINS=http://localhost:5173
```

Never commit `.env` or real credentials.

### 4. Install backend dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Apply migrations and seed policies

```bash
alembic upgrade head
alembic current
python -m app.db.seed
```

The seed creates five active telecom policies:

| Priority | Policy | Decision |
|---:|---|---|
| 300 | Fraud rejection | REJECT |
| 250 | Fraud manual review | MANUAL_REVIEW |
| 220 | Outstanding balance rejection | REJECT |
| 120 | Premium override approval | APPROVE |
| 100 | Standard upgrade approval | APPROVE |

### 6. Start the backend

```bash
export LLM_PROVIDER=mock
export USE_MOCK_LLM=true
export ENABLE_AI_EXPLANATION=true

uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
```

Backend URLs:

```text
API:       http://localhost:8000
Swagger:   http://localhost:8000/docs
OpenAPI:   http://localhost:8000/openapi.json
Health:    http://localhost:8000/health
Readiness: http://localhost:8000/ready
```

### 7. Start the frontend

Open a second terminal:

```bash
cd decisionflow_ai/frontend
cp .env.example .env.local
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

Use `localhost` because the default CORS configuration permits `http://localhost:5173`.

## Docker backend option

The Compose file exposes `mysql` and `backend` services:

```bash
docker compose up -d mysql backend
docker compose ps
```

The frontend currently runs separately with Vite.

## Decision Center demo

### Approval preset

Expected result:

```text
Decision: APPROVE
Confidence: 70%
Winning policy: Premium override approval
Matched policies: 2
Skipped policies: 0
```

### Rejection preset

Expected result:

```text
Decision: REJECT
Confidence: 60%
Winning policy: Outstanding balance rejection
Matched policies: 3
Conflicts detected: at least 1
```

### Missing-fields preset

Expected result:

```text
Decision: MANUAL_REVIEW
Confidence: 0%
Winning policy: none
Explanation: DETERMINISTIC_FALLBACK
Warning: MISSING_REQUIRED_FIELDS
```

## Decision API

### Evaluate a decision

```http
POST /api/v1/decisions/evaluate
```

Example:

```bash
curl -X POST \
  http://localhost:8000/api/v1/decisions/evaluate \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: cor_demo_001" \
  -H "X-User-ID: demo_user" \
  -d '{
    "request_id": "req_demo_001",
    "domain": "telecom",
    "customer": {
      "customer_id": "CUST-DEMO-001",
      "customer_tenure_months": 36,
      "credit_score": 790,
      "payment_defaults": 0,
      "fraud_risk_score": 0.12,
      "customer_segment": "PREMIUM",
      "outstanding_balance": 0,
      "account_status": "current"
    },
    "context": {
      "channel": "ADMIN_PORTAL",
      "currency": "INR",
      "requested_action": "DEVICE_UPGRADE"
    },
    "options": {
      "include_explanation": true,
      "include_unmatched_rules": true,
      "include_condition_trace": true
    }
  }'
```

Important response fields:

```text
evaluation_id
request_id
decision
decision_confidence
winning_policy
matched_policies
unmatched_policies
skipped_policies
resolution
explanation
metrics
warnings
evaluated_at
correlation_id
```

### Retrieve a decision

```http
GET /api/v1/decisions/{evaluation_id}
```

## API endpoint summary

### Decisions

```text
POST /api/v1/decisions/evaluate
GET  /api/v1/decisions/{evaluation_id}
```

### Evaluations

```text
POST /api/v1/evaluations
GET  /api/v1/evaluations/{evaluation_id}
```

### Policies

```text
POST   /api/v1/policies
GET    /api/v1/policies
GET    /api/v1/policies/{policy_id}
PUT    /api/v1/policies/{policy_id}
DELETE /api/v1/policies/{policy_id}
POST   /api/v1/policies/{policy_id}/activate
POST   /api/v1/policies/{policy_id}/disable
```

### AI policy studio

```text
POST /api/v1/ai/policies/generate
POST /api/v1/ai/policies/clarify
POST /api/v1/ai/policies/check-conflicts
POST /api/v1/ai/policies/generate-tests
POST /api/v1/ai/decisions/explain
```

### Audit and analytics

```text
GET /api/v1/audit
GET /api/v1/audit/{audit_id}

GET /api/v1/analytics/dashboard
GET /api/v1/analytics/summary
GET /api/v1/analytics/decision-distribution
GET /api/v1/analytics/decision-trend
GET /api/v1/analytics/top-policies
```

### Configuration and health

```text
GET /api/v1/config/fields
GET /api/v1/config/operators
GET /health
GET /ready
GET /docs
GET /openapi.json
```

## AI fallback behaviour

AI is non-critical to final decisioning.

When AI explanation generation fails:

- The deterministic decision remains unchanged.
- The API still returns a successful decision response.
- A deterministic explanation is returned.
- Warning `AI_EXPLANATION_UNAVAILABLE` is added.
- Audit action `DECISION_EVALUATED` is recorded.
- Audit action `AI_EXPLANATION_FAILED` is also recorded.
- Both audit records retain the request correlation ID.

For incomplete evidence or missing required fields, the system uses deterministic fallback without asking AI to infer missing facts.

## Correlation and audit

Requests may include:

```http
X-Correlation-ID: cor_example
X-User-ID: demo_user
```

The correlation ID is propagated through:

- response body
- `X-Correlation-ID` response header
- persisted evaluation
- decision audit
- AI-failure audit
- application logs

## Testing

### Backend

```bash
cd backend
source .venv/bin/activate
pytest -q
```

Expected integration baseline:

```text
140 passed
```

Selected decision tests:

```bash
pytest tests/test_decision_schemas.py -q
pytest tests/integration/test_decision_routes.py -q
pytest tests/integration/test_decision_field_mapping.py -q
```

### Frontend

```bash
cd frontend
npm install
npm run build
npm run lint
```

### Health checks

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
```

Readiness should report MySQL and the rule engine as available.

## Database migration

Current migration:

```text
1d563b0d9225_initial_schema.py
```

Useful commands:

```bash
cd backend
alembic current
alembic history
alembic upgrade head
```

## Documentation

Detailed documentation is available under `docs/`:

```text
docs/architecture/01_MASTER_ARCHITECTURE.md
docs/contracts/02_API_CONTRACT.md
docs/database/07_DATABASE_DESIGN.md
docs/demo/09_DEMO_GUIDE.md
docs/integration/06_INTEGRATION_GUIDE.md
docs/integration/08_GIT_WORKFLOW.md
docs/integration/HANDOFF_STATUS.md
docs/AI_ENGINEERING_LOG.md
```

## Branch strategy

```text
main
  Stable baseline. Merge only after review and approval.

feature/backend-rule-engine
  Backend rule-engine development history.

feature/ai-policy-studio
  AI policy-studio development history.

feature/frontend-dashboard
  Frontend development history.

feature/integration
  Current fully integrated and demo-ready release candidate.

work/decision-orchestration
  Safe checkpoint for Decision Service integration.

work/frontend-decision-integration
  Safe checkpoint for frontend Decision Center integration.
```

## Security

- Never commit `.env`.
- Never commit API keys, tokens or production credentials.
- Use the mock provider for local development and demos.
- Keep deterministic policy evaluation authoritative.
- Treat AI-generated policies as drafts until validated and activated.
- Avoid logging sensitive customer data in production.
- Restrict CORS origins outside local development.
- Rotate any credential that has accidentally been committed.

## Troubleshooting

### Backend cannot connect to MySQL

```bash
docker compose ps
docker compose logs mysql --tail=100
```

Confirm the database URL and credentials in `backend/.env`.

### Frontend cannot reach the API

Confirm:

```text
Backend: http://localhost:8000
Frontend: http://localhost:5173
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Restart Vite after changing `.env.local`.

### Policies are skipped because fields are missing

The public API uses fields such as:

```text
customer_tenure_months
payment_defaults
customer_segment
outstanding_balance
account_status
```

The Decision Service maps them to internal policy paths such as:

```text
customer.tenure_months
customer.payment_history_defaults
customer.plan_type
account.outstanding_balance
account.status
```

### AI provider is unavailable

Use:

```env
LLM_PROVIDER=mock
USE_MOCK_LLM=true
ENABLE_AI_EXPLANATION=true
```

A valid deterministic decision must never fail solely because AI is unavailable.

## Release checklist

Before merging `feature/integration` into `main`:

- [ ] `pytest -q` passes
- [ ] `npm run build` passes
- [ ] `npm run lint` passes
- [ ] MySQL readiness passes
- [ ] Approval browser flow passes
- [ ] Rejection browser flow passes
- [ ] Missing-fields browser flow passes
- [ ] AI-failure fallback passes
- [ ] Decision and AI-failure audits are present
- [ ] No HTTP 500 or unhandled traceback
- [ ] README and integration handoff are current
- [ ] Reviewer approval is received
