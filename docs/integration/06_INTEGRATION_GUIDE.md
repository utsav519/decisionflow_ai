# DecisionFlow AI
## Integration Lead and End-to-End Assembly Guide

**Document ID:** DFA-INT-006  
**Version:** 1.0  
**Status:** Hackathon POC Baseline — MySQL Edition  
**Primary Owner:** Technical Architect, Integration Lead, and Decision Service Owner  
**Supporting Owners:** Backend Engineer, AI Engineer, Frontend Engineer  
**Primary Branch:** `feature/integration`  
**Final Merge Authority:** Technical Architect and Integration Lead

---

# 1. Purpose

This document defines the complete role, implementation responsibilities, integration workflow, handoff requirements, merge sequence, verification steps, and end-to-end assembly process for the Technical Architect and Integration Lead.

The person following this guide owns the final working product.

The Integration Lead is responsible for ensuring that:

- All four team members build against one agreed architecture.
- Shared API contracts remain stable.
- Backend, AI, frontend, and persistence modules can be developed independently.
- Module handoffs are complete and verifiable.
- The final decision endpoint orchestrates all internal services correctly.
- MySQL, FastAPI, AI, rule engine, audit, analytics, and React integrate successfully.
- Failures degrade safely.
- The final repository runs from documented commands.
- The demo follows one stable end-to-end path.
- No critical module is left unintegrated until the final hour.

The Integration Lead is not only a coordinator.

This role includes coding responsibility for the central application flow.

The recommended title is:

> **Technical Architect + Integration Lead + Decision Service Owner**

---

# 2. Your Role

You are the technical owner of the complete POC.

You should introduce your responsibility to the team as:

> “I will finalize the architecture and shared contracts, own the central decision orchestration, and integrate the backend, AI, and frontend modules into one working end-to-end application.”

You are responsible for:

- Architecture decisions
- Shared API contract
- Shared project structure
- Module boundaries
- Cross-module schemas
- FastAPI application wiring
- Decision Service
- Explanation Service wrapper
- Health and readiness endpoints
- Correlation-ID flow
- Dependency wiring
- End-to-end error handling
- Integration branch
- Merge coordination
- End-to-end testing
- Docker Compose assembly
- Demo seed verification
- Final technical presentation
- Judge questions about architecture and product flow

You are not expected to personally implement every internal module.

You should not duplicate:

- Backend engineer's rule engine
- Backend engineer's repositories
- AI engineer's provider implementation
- Frontend engineer's UI components

Your responsibility is to make those modules work together through stable interfaces.

---

# 3. Product Integration Principle

All components must integrate through a single governed flow.

```text
React Frontend
    ↓ REST API
FastAPI Router
    ↓
Application Service
    ↓
Policy Service
    ↓
Rule Engine
    ↓
Priority Resolver
    ↓
Decision Confidence Calculator
    ↓
AI Explanation Service
    ↓
Evaluation Repository
    ↓
Audit Service
    ↓
Analytics Data
    ↓
Standard API Response
    ↓
React Frontend
```

The final decision is produced before AI explanation.

The correct order is:

```text
Deterministic Decision
    ↓
AI Explanation
```

The incorrect order is:

```text
AI Recommendation
    ↓
Business Decision
```

---

# 4. Final Team Ownership

## Person 1 — You

### Role

```text
Technical Architect
Integration Lead
Decision Service Owner
Final Demo Technical Lead
```

### Primary files

```text
backend/app/main.py
backend/app/api/dependencies.py
backend/app/api/v1/decisions.py
backend/app/api/v1/system.py
backend/app/services/decision_service.py
backend/app/services/explanation_service.py
backend/app/services/integration_service.py
backend/app/core/error_handlers.py
backend/app/core/lifecycle.py
backend/app/core/logging.py
backend/app/schemas/decision.py
docker-compose.yml
README.md
```

You may also own:

```text
backend/app/services/health_service.py
backend/tests/integration/
docs/integration/
```

---

## Person 2 — Backend Engineer

### Owns

```text
MySQL
SQLAlchemy
Alembic
Policy CRUD
Rule Engine
Priority Resolver
Confidence Calculator
Repositories
Audit Persistence
Analytics Queries
Seed Data
```

### Must pass to you

```python
PolicyService
RuleEngine
PriorityResolver
DecisionConfidenceCalculator
EvaluationRepository
AuditService
AnalyticsService
```

---

## Person 3 — AI Engineer

### Owns

```text
LLM Provider
Mock Provider
Policy Generator
Ambiguity Detector
Conflict Explanation
Decision Explanation
Test-Case Generator
AI Fallback Helpers
```

### Must pass to you

```python
get_llm_provider
AIPolicyGenerator
AmbiguityDetector
ConflictAssistant
DecisionExplainer
AITestCaseGenerator
build_fallback_explanation
```

---

## Person 4 — Frontend Engineer

### Owns

```text
React Application
Dashboard
AI Policy Studio
Policy Screens
Decision Center
Analytics
Audit
API Client
Mock Mode
```

### Must pass to you

```text
Working frontend branch
Exact environment variables
Real API mode
Mock API mode
Build command
Test command
Known API assumptions
```

---

# 5. Integration Lead Deliverables

You must deliver all of the following.

## 5.1 Shared architecture

Already defined in:

```text
01_MASTER_ARCHITECTURE.md
```

## 5.2 Shared API contract

Already defined in:

```text
02_API_CONTRACT.md
```

## 5.3 Decision orchestration

The central application flow.

## 5.4 Application wiring

- Router registration
- Middleware
- Dependency injection
- Error handlers
- CORS
- Lifecycle
- Health checks
- Readiness checks

## 5.5 Cross-module integration

- Backend module
- AI module
- Frontend module
- MySQL
- Docker Compose

## 5.6 End-to-end tests

At minimum:

- Policy generation
- Policy save
- Policy activation
- Customer evaluation
- Priority override
- AI explanation
- Fallback explanation
- Evaluation persistence
- Audit visibility
- Analytics update

## 5.7 Final project README

Must allow a reviewer to run the system.

## 5.8 Demo-ready configuration

- Stable seed data
- Stable sample policy
- Stable customer presets
- Mock-provider emergency mode
- Real-provider mode
- Demo reset steps

---

# 6. Your Working Branch

Use:

```text
feature/integration
```

Do not build directly on `main`.

Recommended branch model:

```text
main
├── feature/backend-rule-engine
├── feature/ai-policy-studio
├── feature/frontend-dashboard
└── feature/integration
```

Your integration branch should regularly pull approved work from all feature branches.

The final merge into `main` should happen only after end-to-end verification.

The detailed Git process will be defined in `08_GIT_WORKFLOW.md`.

---

# 7. Shared Repository Baseline

Before parallel coding begins, you should create and commit:

```text
decisionflow-ai/
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── docs/
├── backend/
└── frontend/
```

Also commit:

- Empty agreed folders
- Shared field catalogue
- Shared operator catalogue
- Shared API envelope definitions
- Basic FastAPI startup
- Basic React startup
- MySQL Docker service
- Contract documents

This baseline prevents each team member from creating incompatible structures.

---

# 8. First 30 Minutes With the Team

You should conduct one short technical alignment session.

## 8.1 Confirm the product

Use this statement:

> “We are building an AI-assisted decision automation platform demonstrated through telecom device-upgrade eligibility.”

## 8.2 Confirm the architecture

```text
React
    ↓
FastAPI
    ↓
Application Services
    ↓
Rule Engine + AI Services
    ↓
MySQL
```

## 8.3 Confirm module ownership

Assign one owner per module.

## 8.4 Confirm API contract

Every developer must have:

```text
02_API_CONTRACT.md
```

## 8.5 Confirm branch names

```text
feature/backend-rule-engine
feature/ai-policy-studio
feature/frontend-dashboard
feature/integration
```

## 8.6 Confirm handoff checkpoints

Do not wait until a module is “100% finished.”

Require staged handoffs.

## 8.7 Confirm frozen technology stack

```text
Frontend:
React + Vite + TypeScript + Tailwind + Axios + Recharts

Backend:
FastAPI + Pydantic + SQLAlchemy

Database:
MySQL 8.0 + PyMySQL + Alembic

Rule Engine:
Custom deterministic Python engine

AI:
Direct LLM SDK + provider abstraction + structured output

Packaging:
Docker Compose
```

---

# 9. What You Need Before Anyone Codes

You must provide every teammate with:

## Shared documents

```text
01_MASTER_ARCHITECTURE.md
02_API_CONTRACT.md
```

## Their individual implementation guide

```text
Backend Engineer:
03_BACKEND_MODULE_GUIDE.md

AI Engineer:
04_AI_MODULE_GUIDE.md

Frontend Engineer:
05_FRONTEND_MODULE_GUIDE.md
```

## Repository access

- Git remote
- Branch rules
- Base project structure

## Environment template

- `.env.example`
- MySQL credentials for local demo
- API URLs
- Mock mode setting

## Definition of done

Each module guide contains its own completion checklist.

---

# 10. Shared Contracts You Must Protect

You are the owner of these cross-module contracts.

## 10.1 API routes

Example:

```text
POST /api/v1/ai/policies/generate
POST /api/v1/policies
POST /api/v1/policies/{id}/activate
POST /api/v1/decisions/evaluate
GET  /api/v1/analytics/summary
GET  /api/v1/audit
```

## 10.2 JSON field names

Example:

```text
decision_confidence
winning_policy
matched_policies
correlation_id
```

## 10.3 Enumerations

```text
APPROVE
REJECT
MANUAL_REVIEW
NO_MATCH

DRAFT
PENDING_APPROVAL
ACTIVE
DISABLED
ARCHIVED
```

## 10.4 Shared field catalogue

No teammate may invent a second field catalogue.

## 10.5 Shared operator catalogue

No teammate may use an operator not present in the registry.

## 10.6 Function signatures

Example:

```python
RuleEngine.evaluate(request_data, policies)
PriorityResolver.resolve(matched_policies)
DecisionExplainer.generate(evaluation_result, style)
```

## 10.7 Error envelope

All errors must use one contract.

---

# 11. Contract Change Control

No shared contract should change silently.

When a teammate requests a change:

1. Ask what problem requires the change.
2. Identify impacted modules.
3. Decide whether it is necessary.
4. Update `02_API_CONTRACT.md`.
5. Update backend schemas.
6. Update frontend types.
7. Update mock responses.
8. Update tests.
9. Inform all owners.

Use a small change log.

Example:

```text
Contract Change 03
Field:
explanation.generated_by

Old:
string

New:
"AI" | "DETERMINISTIC_FALLBACK"

Reason:
Frontend must display fallback state.

Affected:
Backend, AI, Frontend, Tests
```

---

# 12. Your Core Code Ownership

Your primary code responsibility is the orchestration layer.

Recommended files:

```text
backend/app/services/decision_service.py
backend/app/services/explanation_service.py
backend/app/api/v1/decisions.py
backend/app/api/v1/system.py
backend/app/main.py
```

You should also own integration tests.

---

# 13. Decision Service Responsibility

The Decision Service is the central application service.

It coordinates:

```text
Validation
Policy Loading
Rule Evaluation
Resolution
Confidence
Explanation
Persistence
Audit
Response Building
```

The Decision Service must not contain:

- SQL query implementation
- Operator implementations
- Provider-specific LLM calls
- React logic

---

# 14. Decision Service Interface

## File

```text
backend/app/services/decision_service.py
```

## Required interface

```python
class DecisionService:
    async def evaluate(
        self,
        *,
        request: DecisionEvaluationRequest,
        actor_id: str,
        correlation_id: str,
    ) -> DecisionEvaluationResponse:
        ...
```

Dependencies should be injected.

```python
class DecisionService:
    def __init__(
        self,
        *,
        policy_service: PolicyService,
        rule_engine: RuleEngine,
        priority_resolver: PriorityResolver,
        confidence_calculator: DecisionConfidenceCalculator,
        explanation_service: ExplanationService,
        evaluation_repository: EvaluationRepository,
        audit_service: AuditService,
    ) -> None:
        ...
```

---

# 15. Decision Service Processing Order

The processing order must remain stable.

```text
1. Validate decision request.
2. Load active policies for domain.
3. Evaluate all active policies.
4. Resolve final outcome.
5. Calculate deterministic decision confidence.
6. Build structured explanation input.
7. Request AI explanation if enabled.
8. Use deterministic fallback if AI fails.
9. Persist evaluation.
10. Persist per-policy rule results.
11. Write audit record.
12. Build final API response.
13. Return response.
```

Do not generate explanation before resolution.

Do not persist a partial decision unless the failure state is explicitly supported.

---

# 16. Decision Service Pseudocode

```python
class DecisionService:
    async def evaluate(
        self,
        *,
        request: DecisionEvaluationRequest,
        actor_id: str,
        correlation_id: str,
    ) -> DecisionEvaluationResponse:
        started_at = monotonic()

        active_policies = self.policy_service.get_active_policies(
            domain=request.domain
        )

        engine_result = self.rule_engine.evaluate(
            request_data=request.customer.model_dump(exclude_none=True),
            policies=active_policies,
        )

        resolution = self.priority_resolver.resolve(
            matched_policies=engine_result.matched_policies
        )

        confidence = self.confidence_calculator.calculate(
            request_data=request.customer.model_dump(exclude_none=True),
            engine_result=engine_result,
            resolution=resolution,
        )

        explanation = await self.explanation_service.generate(
            request=request,
            engine_result=engine_result,
            resolution=resolution,
            confidence=confidence,
            correlation_id=correlation_id,
        )

        total_latency_ms = int((monotonic() - started_at) * 1000)

        persisted = self.evaluation_repository.save_complete_evaluation(
            request=request,
            engine_result=engine_result,
            resolution=resolution,
            confidence=confidence,
            explanation=explanation,
            actor_id=actor_id,
            correlation_id=correlation_id,
            total_latency_ms=total_latency_ms,
        )

        self.audit_service.record_decision(
            evaluation=persisted,
            actor_id=actor_id,
            correlation_id=correlation_id,
        )

        return self.response_builder.build(
            persisted=persisted,
            engine_result=engine_result,
            resolution=resolution,
            confidence=confidence,
            explanation=explanation,
            total_latency_ms=total_latency_ms,
        )
```

---

# 17. Explanation Service Wrapper

## File

```text
backend/app/services/explanation_service.py
```

The wrapper protects the decision flow from AI failure.

## Required interface

```python
class ExplanationService:
    async def generate(
        self,
        *,
        request: DecisionEvaluationRequest,
        engine_result: EngineEvaluationResult,
        resolution: ResolutionResult,
        confidence: DecisionConfidenceResult,
        correlation_id: str,
    ) -> ExplanationResult:
        ...
```

## Required behavior

```text
If AI explanation is enabled:
    Try AI explanation.
    Validate output.
    Return AI explanation.

If AI is disabled or fails:
    Build deterministic fallback.
    Return fallback.
```

The wrapper should never allow an explanation error to destroy a valid deterministic decision.

---

# 18. Explanation Input Builder

Do not send raw internal objects directly to the LLM.

Create a small structured payload.

Recommended input:

```json
{
  "decision": "REJECT",
  "decision_confidence": 92,
  "winning_policy": {
    "name": "Fraud rejection",
    "priority": 300,
    "version": 1,
    "decision": "REJECT"
  },
  "matched_policies": [
    {
      "name": "Fraud rejection",
      "priority": 300,
      "decision": "REJECT",
      "condition_results": [
        {
          "field": "fraud_risk_score",
          "operator": "greater_than_or_equal",
          "expected": 0.85,
          "actual": 0.91,
          "matched": true
        }
      ]
    }
  ],
  "resolution": {
    "strategy": "HIGHEST_PRIORITY",
    "reason": "Fraud rejection priority 300 exceeded approval priority 100."
  },
  "missing_fields": [],
  "confidence_factors": []
}
```

Do not send:

- Database password
- Full audit table
- API key
- Unrelated customer data
- Hidden service configuration

---

# 19. Decision Request Schemas

## File

```text
backend/app/schemas/decision.py
```

You own the final cross-module schema.

Required models:

```text
CustomerData
DecisionContext
DecisionOptions
DecisionEvaluationRequest
DecisionEvaluationResponse
DecisionListItem
DecisionDetailResponse
ExplanationResponse
EvaluationMetrics
WarningResponse
```

These must exactly match the API contract.

---

# 20. Decision Router

## File

```text
backend/app/api/v1/decisions.py
```

Required endpoints:

```text
POST /api/v1/decisions/evaluate
GET  /api/v1/decisions
GET  /api/v1/decisions/{evaluation_id}
POST /api/v1/decisions/{evaluation_id}/explanation
```

## Router responsibility

- Parse request.
- Resolve actor.
- Resolve correlation ID.
- Build Decision Service.
- Call service.
- Return standard envelope.

No rule logic should be inside the router.

---

# 21. Dependency Wiring

## File

```text
backend/app/api/dependencies.py
```

Create builder functions.

Example:

```python
def get_policy_service(
    db: Session = Depends(get_db),
) -> PolicyService:
    ...


def get_rule_engine() -> RuleEngine:
    ...


def get_priority_resolver() -> PriorityResolver:
    ...


def get_confidence_calculator() -> DecisionConfidenceCalculator:
    ...


def get_explanation_service() -> ExplanationService:
    ...


def get_audit_service(
    db: Session = Depends(get_db),
) -> AuditService:
    ...


def get_decision_service(
    policy_service: PolicyService = Depends(get_policy_service),
    rule_engine: RuleEngine = Depends(get_rule_engine),
    priority_resolver: PriorityResolver = Depends(get_priority_resolver),
    confidence_calculator: DecisionConfidenceCalculator = Depends(
        get_confidence_calculator
    ),
    explanation_service: ExplanationService = Depends(
        get_explanation_service
    ),
    evaluation_repository: EvaluationRepository = Depends(
        get_evaluation_repository
    ),
    audit_service: AuditService = Depends(get_audit_service),
) -> DecisionService:
    ...
```

This makes modules replaceable during tests.

---

# 22. FastAPI Main Application

## File

```text
backend/app/main.py
```

You own final app assembly.

It must register:

- CORS
- Correlation middleware
- Logging
- Exception handlers
- Routers
- Startup lifecycle
- Shutdown lifecycle

Recommended router groups:

```text
Configuration
Policies
AI Policy Studio
Decisions
Analytics
Audit
System
```

---

# 23. Router Registration

```python
app.include_router(
    config_router,
    prefix="/api/v1/config",
    tags=["Configuration"],
)

app.include_router(
    policy_router,
    prefix="/api/v1/policies",
    tags=["Policies"],
)

app.include_router(
    ai_router,
    prefix="/api/v1/ai",
    tags=["AI Policy Studio"],
)

app.include_router(
    decision_router,
    prefix="/api/v1/decisions",
    tags=["Decisions"],
)

app.include_router(
    analytics_router,
    prefix="/api/v1/analytics",
    tags=["Analytics"],
)

app.include_router(
    audit_router,
    prefix="/api/v1/audit",
    tags=["Audit"],
)

app.include_router(
    system_router,
    tags=["System"],
)
```

Avoid duplicated prefixes.

---

# 24. CORS Configuration

Allow:

```text
http://localhost:5173
```

Recommended configuration:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Correlation-ID"],
)
```

For a demo-only environment, a permissive setting may be used temporarily, but it should be documented.

---

# 25. Correlation-ID Middleware

Every request must have a correlation ID.

Required behavior:

1. Read request header.
2. Generate if absent.
3. Store in request state.
4. Add to logs.
5. Add to response header.
6. Include in API envelope.

Example:

```python
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    correlation_id = (
        request.headers.get("X-Correlation-ID")
        or new_id("cor")
    )

    request.state.correlation_id = correlation_id

    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id

    return response
```

---

# 26. Health Endpoint

## Endpoint

```text
GET /health
```

This endpoint should confirm application process health.

Example:

```json
{
  "status": "healthy",
  "service": "decisionflow-api",
  "version": "1.0.0",
  "timestamp": "2026-07-24T09:45:00.000Z"
}
```

It should not require AI or MySQL to be healthy.

---

# 27. Readiness Endpoint

## Endpoint

```text
GET /ready
```

Check:

- MySQL
- Rule engine
- AI provider configuration

Possible result:

```json
{
  "status": "ready",
  "dependencies": {
    "database": "available",
    "database_type": "mysql",
    "rule_engine": "available",
    "ai_provider": "available"
  },
  "capabilities": {
    "decision_evaluation": true,
    "ai_policy_generation": true,
    "ai_explanation": true
  }
}
```

Degraded example:

```json
{
  "status": "degraded",
  "dependencies": {
    "database": "available",
    "database_type": "mysql",
    "rule_engine": "available",
    "ai_provider": "unavailable"
  },
  "capabilities": {
    "decision_evaluation": true,
    "ai_policy_generation": false,
    "ai_explanation": false
  }
}
```

---

# 28. Application Lifecycle

## File

```text
backend/app/core/lifecycle.py
```

On startup:

1. Load settings.
2. Configure logging.
3. Verify MySQL connectivity.
4. Verify migrations are current if practical.
5. Initialize AI provider lazily or safely.
6. Log application-ready event.

Do not automatically run destructive schema changes.

Migrations should run through deployment or entrypoint.

---

# 29. MySQL Integration

The Integration Lead does not implement repository internals, but must verify:

- MySQL container is healthy.
- Backend uses MySQL URL.
- Migrations run.
- Seed runs.
- Evaluation writes are visible.
- Audit writes are visible.
- Analytics read from MySQL.
- No SQLite file appears.
- No in-memory fallback is active.

Expected connection string in Docker:

```text
mysql+pymysql://decisionflow:decisionflow@mysql:3306/decisionflow
```

Expected local connection string:

```text
mysql+pymysql://decisionflow:decisionflow@localhost:3306/decisionflow
```

---

# 30. Docker Compose Ownership

You own final `docker-compose.yml`.

Required services:

```text
mysql
backend
frontend
```

Recommended structure:

```yaml
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: decisionflow
      MYSQL_USER: decisionflow
      MYSQL_PASSWORD: decisionflow
      MYSQL_ROOT_PASSWORD: root
    ports:
      - "3306:3306"
    volumes:
      - decisionflow_mysql_data:/var/lib/mysql
    healthcheck:
      test:
        [
          "CMD",
          "mysqladmin",
          "ping",
          "-h",
          "localhost",
          "-uroot",
          "-proot"
        ]
      interval: 5s
      timeout: 5s
      retries: 20

  backend:
    build:
      context: ./backend
    environment:
      DATABASE_URL:
        mysql+pymysql://decisionflow:decisionflow@mysql:3306/decisionflow
      LLM_PROVIDER: ${LLM_PROVIDER:-mock}
      LLM_MODEL: ${LLM_MODEL:-mock-model}
      LLM_API_KEY: ${LLM_API_KEY:-}
      USE_MOCK_LLM: ${USE_MOCK_LLM:-true}
    ports:
      - "8000:8000"
    depends_on:
      mysql:
        condition: service_healthy

  frontend:
    build:
      context: ./frontend
    environment:
      VITE_API_BASE_URL: http://localhost:8000/api/v1
      VITE_BACKEND_BASE_URL: http://localhost:8000
      VITE_USE_MOCK_API: "false"
    ports:
      - "5173:5173"
    depends_on:
      - backend

volumes:
  decisionflow_mysql_data:
```

---

# 31. Environment Files

## Root `.env.example`

```text
LLM_PROVIDER=mock
LLM_MODEL=mock-model
LLM_API_KEY=
USE_MOCK_LLM=true
```

## Backend `.env.example`

```text
APP_NAME=DecisionFlow AI
APP_ENV=development
API_V1_PREFIX=/api/v1
LOG_LEVEL=INFO

DATABASE_URL=mysql+pymysql://decisionflow:decisionflow@localhost:3306/decisionflow

LLM_PROVIDER=mock
LLM_MODEL=mock-model
LLM_API_KEY=
USE_MOCK_LLM=true
ENABLE_AI_POLICY_GENERATION=true
ENABLE_AI_EXPLANATION=true

ALLOWED_ORIGINS=http://localhost:5173
```

## Frontend `.env.example`

```text
VITE_APP_NAME=DecisionFlow AI
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_BACKEND_BASE_URL=http://localhost:8000
VITE_USE_MOCK_API=false
VITE_API_TIMEOUT_MS=20000
```

---

# 32. Module Handoff Model

Every teammate must hand work over in stages.

You should never accept only:

```text
“It is done.”
```

Require:

- Branch
- Commit hash
- Setup commands
- Test result
- Function imports
- Known limitations
- API deviations
- Example output

---

# 33. Backend Handoff — What You Must Receive

## First backend handoff

Required:

```python
PolicyCreate
PolicyResponse
RuleEngine.evaluate
PriorityResolver.resolve
DecisionConfidenceCalculator.calculate
```

Required proof:

- Operator tests pass.
- Rule-engine tests pass.
- Example approval result.
- Example rejection result.
- Missing-field result.

## Second backend handoff

Required:

```python
PolicyService.get_active_policies
Policy CRUD routes
MySQL models
Alembic migrations
Seed script
```

Required proof:

- MySQL starts.
- Migration runs.
- Seed runs twice safely.
- Policy list works.
- Active policy retrieval works.

## Final backend handoff

Required:

```python
EvaluationRepository
AuditService
AnalyticsService
```

Required proof:

- Evaluation persists.
- Rule traces persist.
- Audit appears.
- Analytics summary updates.

---

# 34. AI Handoff — What You Must Receive

## First AI handoff

Required:

```python
get_llm_provider
AIPolicyGenerator.generate
DecisionExplainer.generate
build_fallback_explanation
MockLLMProvider
```

Required proof:

- Valid policy generation.
- Ambiguous policy response.
- Explanation response.
- Fallback response.

## Final AI handoff

Required:

```python
AmbiguityDetector.detect
ConflictAssistant.explain
AITestCaseGenerator.generate
AIPolicyConfidenceCalculator.calculate
```

Required proof:

- Tests pass.
- Provider timeout handled.
- Invalid JSON handled.
- Unsupported field blocked.
- Prompt versions documented.

---

# 35. Frontend Handoff — What You Must Receive

## First frontend handoff

Required:

- Application shell
- Mock mode
- API client
- Shared TypeScript types
- Policy Studio mock flow
- Decision Center mock flow

Required proof:

```bash
npm run dev
npm run typecheck
```

## Final frontend handoff

Required:

- Real API mode
- Policy generation integration
- Policy save and activation
- Decision evaluation
- Analytics
- Audit
- Build and tests

Required proof:

```bash
npm run test:run
npm run typecheck
npm run build
```

---

# 36. Handoff Acceptance Checklist

Do not merge a module only because code exists.

Accept handoff only when:

- Branch is current.
- Commit hash provided.
- Setup instructions work.
- Tests pass.
- Imports are stable.
- API contract is followed.
- No secrets are committed.
- Known limitations are documented.
- Example input and output are provided.
- Merge conflicts are manageable.

---

# 37. Integration Sequence

Use this sequence.

## Stage 1 — Backend foundation

Integrate:

- Settings
- MySQL
- Models
- Migrations
- Field catalogue
- Operator catalogue
- Rule engine
- Policy service

## Stage 2 — AI module

Integrate:

- Provider factory
- Mock provider
- Policy generator
- Explanation
- Fallback

## Stage 3 — Decision Service

Wire:

- Active policy loading
- Rule engine
- Resolver
- Confidence
- Explanation
- Persistence
- Audit

## Stage 4 — API routes

Integrate:

- Policies
- AI
- Decisions
- Analytics
- Audit
- Health

## Stage 5 — Frontend

Connect real APIs.

## Stage 6 — Full Docker stack

Run MySQL, backend, frontend together.

## Stage 7 — End-to-end tests

Run complete business flows.

---

# 38. Recommended Merge Order

Recommended merge order into your integration branch:

```text
1. backend foundation
2. rule engine
3. policy CRUD
4. AI provider abstraction and mock provider
5. AI policy generation
6. explanation and fallback
7. decision orchestration
8. evaluation persistence
9. audit and analytics
10. frontend shell and API client
11. frontend feature pages
12. Docker Compose and README
```

Avoid merging the complete frontend before API types are stable.

---

# 39. Integration Branch Workflow

Example:

```bash
git checkout feature/integration
git pull origin feature/integration

git merge origin/feature/backend-rule-engine
# resolve and test

git merge origin/feature/ai-policy-studio
# resolve and test

git merge origin/feature/frontend-dashboard
# resolve and test
```

After every major merge:

```bash
pytest -q
npm run typecheck
npm run build
```

Do not wait until all three branches are merged to run tests.

---

# 40. Merge Conflict Ownership

When conflict occurs:

## Shared API schema conflict

You decide based on API contract.

## Backend repository conflict

Backend engineer assists.

## AI provider conflict

AI engineer assists.

## Frontend component conflict

Frontend engineer assists.

## Main app or Docker conflict

You own resolution.

Never choose “ours” or “theirs” blindly in shared files.

---

# 41. Shared Files With High Conflict Risk

These files should have one owner.

```text
backend/app/main.py
backend/app/api/dependencies.py
backend/app/core/config.py
backend/app/schemas/common.py
backend/app/schemas/decision.py
docker-compose.yml
README.md
frontend/src/types/api.ts
frontend/src/services/apiClient.ts
```

Recommended ownership:

```text
main.py                    → You
dependencies.py            → You
config.py                  → You with backend input
common.py                  → You
decision.py                → You
docker-compose.yml         → You
README.md                  → You
frontend API types         → Frontend owner with your approval
frontend API client        → Frontend owner
```

---

# 42. Shared Import Stability

Before merging, verify import paths.

Required examples:

```python
from app.services.policy_service import PolicyService
from app.engine.evaluator import RuleEngine
from app.engine.resolver import PriorityResolver
from app.engine.confidence import DecisionConfidenceCalculator
from app.ai.providers.factory import get_llm_provider
from app.ai.policy_generator import AIPolicyGenerator
from app.ai.explainer import DecisionExplainer
from app.ai.fallback import build_fallback_explanation
from app.repositories.evaluation_repository import EvaluationRepository
from app.services.audit_service import AuditService
```

Do not leave duplicate versions such as:

```text
rule_engine.py
engine.py
rules_engine.py
```

Choose one canonical import path.

---

# 43. Policy Creation Integration

The complete flow must be:

```text
Frontend sends natural-language text
    ↓
AI policy endpoint
    ↓
AI policy generator
    ↓
Local AI validation
    ↓
Backend policy validation
    ↓
Conflict check
    ↓
Response to frontend
    ↓
User reviews
    ↓
Frontend creates draft
    ↓
Policy Service writes to MySQL
    ↓
Audit record created
```

AI generation itself must not write to MySQL.

---

# 44. Policy Activation Integration

Complete flow:

```text
Frontend clicks Activate
    ↓
Activation confirmation
    ↓
POST /policies/{id}/activate
    ↓
Policy Service loads draft
    ↓
Validation reruns
    ↓
Conflict scan reruns
    ↓
Version snapshot created
    ↓
Policy set ACTIVE
    ↓
Audit written
    ↓
Transaction committed
    ↓
Frontend refreshes policy
```

Activation and version snapshot should be atomic.

---

# 45. Decision Evaluation Integration

Complete flow:

```text
Frontend submits customer
    ↓
Decision router validates request
    ↓
Decision Service loads active policies
    ↓
Rule Engine evaluates conditions
    ↓
Priority Resolver selects final result
    ↓
Confidence Calculator scores result
    ↓
Explanation Service generates explanation
    ↓
Evaluation and traces stored
    ↓
Audit written
    ↓
Response returned
    ↓
Frontend renders decision and evidence
```

---

# 46. Analytics Integration

Analytics should read persisted data.

Do not calculate official analytics only in the frontend.

Flow:

```text
MySQL evaluations
    ↓
Analytics repository aggregate query
    ↓
Analytics service
    ↓
FastAPI endpoint
    ↓
React charts
```

After a decision evaluation, refreshing analytics should reflect the new decision.

---

# 47. Audit Integration

Audit events should be created for:

```text
POLICY_CREATED
POLICY_UPDATED
POLICY_ACTIVATED
POLICY_DISABLED
POLICY_DELETED
POLICY_GENERATED_BY_AI
DECISION_EVALUATED
AI_EXPLANATION_GENERATED
AI_EXPLANATION_FAILED
```

At minimum for the demo:

```text
POLICY_CREATED
POLICY_ACTIVATED
POLICY_DISABLED
DECISION_EVALUATED
AI_EXPLANATION_FAILED
```

---

# 48. Error Integration

Each internal error must map to an API error.

Examples:

```text
PolicyNotFoundError
    ↓
404 POLICY_NOT_FOUND

DuplicatePolicyNameError
    ↓
409 DUPLICATE_POLICY_NAME

PolicyActivationBlockedError
    ↓
409 POLICY_ACTIVATION_BLOCKED

AIProviderUnavailableError
    ↓
503 AI_PROVIDER_UNAVAILABLE

DatabaseUnavailableError
    ↓
503 DATABASE_UNAVAILABLE
```

The frontend must receive a stable standard error envelope.

---

# 49. AI Failure Degradation

## Policy generation failure

Expected:

- Endpoint fails safely.
- Frontend offers retry.
- Manual creation remains possible.
- No policy is saved.

## Decision explanation failure

Expected:

- Decision remains successful.
- Fallback explanation returned.
- Warning included.
- Audit records AI explanation failure.
- Frontend shows fallback notice.

## AI provider unavailable at startup

Expected:

- `/ready` returns degraded.
- Decision evaluation remains available.
- AI generation disabled or returns 503.

---

# 50. Database Failure Behavior

If MySQL is unavailable:

- `/health` may remain healthy.
- `/ready` must report unavailable.
- Persistence-dependent endpoints return 503.
- No silent fallback to SQLite.
- No silent fallback to memory.
- Frontend shows backend/database error.
- Correlation ID is present.

---

# 51. Transaction Boundaries

You must verify these transaction expectations.

## Policy creation

```text
Policy insert
Audit insert
Commit
```

## Policy activation

```text
Version snapshot
Policy status update
Audit insert
Commit
```

## Decision evaluation

Recommended:

```text
Evaluation insert
Rule-result inserts
Audit insert
Commit
```

If audit is designed as best-effort for POC, document the choice explicitly.

---

# 52. Integration Test Structure

Recommended:

```text
backend/tests/integration/
├── conftest.py
├── test_policy_lifecycle.py
├── test_ai_policy_flow.py
├── test_decision_flow.py
├── test_priority_override.py
├── test_explanation_fallback.py
├── test_audit_flow.py
├── test_analytics_flow.py
└── test_readiness.py
```

Use MySQL test database.

Do not substitute SQLite.

---

# 53. End-to-End Test — Policy Lifecycle

Test:

```text
Create draft
    ↓
Retrieve draft
    ↓
Activate draft
    ↓
Retrieve active policy
    ↓
Disable policy
    ↓
Verify audit entries
```

Assertions:

- Correct statuses
- Version created
- Approver stored
- Audit stored
- Active query changes after disable

---

# 54. End-to-End Test — AI Policy Flow

Test:

```text
Generate policy from text
    ↓
Validate output
    ↓
Save draft
    ↓
Activate
```

Assertions:

- Only supported fields
- Draft status
- AI confidence present
- Assumptions present
- Persistence succeeds
- Activation succeeds

Use mock provider in default test suite.

---

# 55. End-to-End Test — Approval Decision

Seed:

```text
Standard upgrade approval
```

Request:

```json
{
  "customer_id": "CUST-1001",
  "customer_tenure_months": 36,
  "credit_score": 790,
  "payment_defaults": 0,
  "fraud_risk_score": 0.12,
  "customer_segment": "PREMIUM",
  "outstanding_balance": 0
}
```

Assert:

```text
decision = APPROVE
winning policy exists
confidence present
evaluation persisted
audit persisted
```

---

# 56. End-to-End Test — Priority Override

Seed:

```text
Fraud rejection priority 300
Standard approval priority 100
```

Request matches both.

Assert:

```text
decision = REJECT
winning policy = Fraud rejection
resolution strategy = HIGHEST_PRIORITY
matched policies includes both
explanation mentions override
```

---

# 57. End-to-End Test — Missing Fields

Request omits:

```text
credit_score
fraud_risk_score
```

Assert:

```text
decision = MANUAL_REVIEW
skipped policies present
missing fields present
fallback or normal explanation present
```

---

# 58. End-to-End Test — AI Explanation Failure

Configure mock provider to fail explanation.

Assert:

```text
decision still returned
generated_by = DETERMINISTIC_FALLBACK
fallback_used = true
warning present
audit contains AI_EXPLANATION_FAILED
```

---

# 59. End-to-End Test — Analytics

1. Record approval.
2. Record rejection.
3. Request analytics summary.

Assert:

- Total increased.
- Approval count increased.
- Rejection count increased.
- Percentages valid.
- Top policy visible.

---

# 60. API-to-Frontend Verification

For each API:

1. Run backend endpoint.
2. Capture actual JSON.
3. Compare with API contract.
4. Compare with frontend TypeScript type.
5. Compare with mock fixture.
6. Render in frontend.
7. Verify empty/error/loading state.

This prevents “backend works” and “frontend works” while integration fails.

---

# 61. Contract Smoke Script

Create a small script or Postman collection.

Recommended commands:

```text
GET  /health
GET  /ready
GET  /api/v1/config/fields
GET  /api/v1/config/operators
GET  /api/v1/policies
POST /api/v1/ai/policies/generate
POST /api/v1/policies
POST /api/v1/policies/{id}/activate
POST /api/v1/decisions/evaluate
GET  /api/v1/analytics/summary
GET  /api/v1/audit
```

Store examples under:

```text
docs/integration/api-smoke/
```

---

# 62. Local End-to-End Startup

## Docker method

```bash
cp .env.example .env
docker compose up --build
```

Then verify:

```text
Frontend:
http://localhost:5173

Backend:
http://localhost:8000

Swagger:
http://localhost:8000/docs

Health:
http://localhost:8000/health

Readiness:
http://localhost:8000/ready
```

## Non-Docker method

### MySQL

```bash
docker compose up -d mysql
```

### Backend

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# 63. Seed Verification

Before integrating frontend, verify seed policies.

Expected active policies:

```text
Fraud rejection
Fraud manual review
Outstanding balance rejection
Standard upgrade approval
Premium override approval
```

Query:

```text
GET /api/v1/policies?status=ACTIVE
```

Expected count:

```text
5
```

If the AI-created demo policy is added, count changes accordingly.

---

# 64. Demo Reset Procedure

Create a safe reset method.

Recommended:

```bash
docker compose down
docker volume rm decisionflow-ai_decisionflow_mysql_data
docker compose up --build
```

Then:

```bash
alembic upgrade head
python -m app.db.seed
```

A more convenient reset script may be added:

```text
scripts/reset_demo.sh
```

The script must be clearly marked destructive.

---

# 65. README Ownership

You own final `README.md`.

It must include:

- Product summary
- Architecture
- Tech stack
- Module ownership
- Prerequisites
- Environment setup
- Docker run
- Manual run
- MySQL setup
- Migration
- Seed
- Test commands
- API docs
- Demo flow
- Troubleshooting
- Known limitations

---

# 66. README Quick Start

Recommended quick start:

```bash
git clone <repository>
cd decisionflow-ai
cp .env.example .env
docker compose up --build
```

Then open:

```text
http://localhost:5173
```

---

# 67. Integration Status Board

Maintain a simple table.

| Module | Owner | Mock Ready | Real Ready | Tests | Integrated | Blockers |
|---|---|---:|---:|---:|---:|---|
| Backend | Person 2 | Yes | No | Partial | No | MySQL migration |
| AI | Person 3 | Yes | No | Yes | Partial | Provider key |
| Frontend | Person 4 | Yes | No | Partial | No | Decision API |
| Integration | You | Yes | Partial | Partial | Partial | Audit flow |

Update it frequently.

This is more useful than repeatedly asking, “How much is done?”

---

# 68. Integration Checkpoints

## Checkpoint 1

Must exist:

- Repository
- FastAPI runs
- React runs
- MySQL runs
- Contract frozen
- Branches created

## Checkpoint 2

Must exist:

- Rule engine passes unit tests
- Policy CRUD works
- AI mock generation works
- Frontend mock screens work

## Checkpoint 3

Must exist:

- AI policy endpoint works
- Draft saves
- Activation works
- Active policies load

## Checkpoint 4

Must exist:

- Decision endpoint works
- Explanation works
- Evaluation persists
- Audit persists

## Checkpoint 5

Must exist:

- Frontend connected
- Analytics updates
- Docker stack works
- Demo rehearsed

---

# 69. Time-Limited Prioritization

If time becomes limited, prioritize:

## Must have

```text
MySQL
Policy generation
Save draft
Activate policy
Decision evaluation
Priority resolution
Explanation
Audit
Basic dashboard
```

## Should have

```text
Analytics charts
Policy edit
Decision history
Conflict explanation
Generated test cases
```

## Nice to have

```text
Advanced settings
Version-history UI
Complex visual rule editor
Multiple explanation styles
Full responsive polish
```

Never sacrifice the complete end-to-end flow for optional UI polish.

---

# 70. Emergency Fallback Plan

## AI provider unavailable

Set:

```text
LLM_PROVIDER=mock
USE_MOCK_LLM=true
```

## Frontend real API fails late

Frontend can run mock mode for visual demo, but the team should still demonstrate backend APIs separately.

Preferred emergency path:

- Frontend real mode for policy and decision APIs
- Mock provider behind backend
- MySQL remains real
- Rule engine remains real

This preserves architectural credibility.

## Analytics incomplete

Show basic summary counts from MySQL.

## Audit UI incomplete

Use Swagger or database-backed API response.

---

# 71. What Must Always Remain Real

For the final demo, these should remain real whenever possible:

```text
MySQL persistence
Policy save
Policy activation
Rule engine
Priority resolution
Decision confidence
Evaluation persistence
Audit persistence
```

The LLM provider may use mock mode if network or keys fail.

The frontend may use prefilled data, but should call real APIs.

---

# 72. Bug Triage

Classify bugs.

## P0 — Demo blocker

Examples:

- App does not start.
- MySQL unavailable.
- Policy cannot activate.
- Decision endpoint crashes.
- Frontend cannot call backend.

Fix immediately.

## P1 — Critical workflow issue

Examples:

- Wrong priority result.
- Audit missing.
- AI failure blocks decision.
- Response contract mismatch.

Fix before polish.

## P2 — Important but non-blocking

Examples:

- Chart error.
- Filter issue.
- Layout overflow.

Fix after complete flow.

## P3 — Cosmetic

Examples:

- Spacing
- Icon size
- Minor label

Fix last.

---

# 73. Logging During Integration

Use logs to trace:

```text
correlation_id
endpoint
policy_id
evaluation_id
provider
latency
decision
error_code
```

A single correlation ID should allow tracing:

```text
Frontend request
    ↓
FastAPI
    ↓
Rule engine
    ↓
AI explanation
    ↓
MySQL
    ↓
Audit
```

---

# 74. Integration Debugging Order

When a flow fails:

1. Check browser network request.
2. Check status code.
3. Check correlation ID.
4. Check backend log.
5. Check request schema.
6. Check service dependency.
7. Check MySQL transaction.
8. Check AI provider only if AI step failed.
9. Check frontend rendering after API is valid.

Do not start by changing multiple modules.

---

# 75. Common Integration Failures

## Different field naming

Example:

```text
Frontend sends customerTenureMonths
Backend expects customer_tenure_months
```

Fix frontend payload to contract.

## Different enum

Example:

```text
MANUAL REVIEW
MANUAL_REVIEW
```

Use contract value.

## Different response envelope

Example:

```text
Backend returns raw data
Frontend expects data.data
```

Fix backend envelope.

## Duplicate route prefix

Example:

```text
/api/v1/policies/policies
```

Fix router registration.

## Docker URL issue

Browser cannot resolve Docker hostname `backend`.

Use:

```text
http://localhost:8000
```

in frontend browser-facing configuration.

## AI timeout blocks decision

Fix Explanation Service wrapper.

## MySQL startup race

Use health check and dependency condition.

---

# 76. End-to-End Manual Verification

Run these manually.

## Policy generation

Input:

```text
Approve premium device upgrades for customers with at least
24 months tenure, no payment defaults, credit score at least 750,
and fraud risk below 0.6.
```

Expected:

- Valid generated policy
- Confidence
- Assumption
- No blocking ambiguity

## Ambiguity

Input:

```text
Approve loyal customers for expensive devices.
```

Expected:

- Clarification required
- No activatable policy

## Approval

Use eligible customer preset.

Expected:

```text
APPROVE
```

## Fraud rejection

Use high-risk preset.

Expected:

```text
REJECT
```

## Missing fields

Use minimal customer preset.

Expected:

```text
MANUAL_REVIEW
```

## Audit

Expected:

- Policy creation
- Policy activation
- Decision evaluation

## Analytics

Expected:

- Counts updated

---

# 77. Demo Flow Ownership

You should lead the technical demo.

Recommended speaker split:

## You

- Business problem
- Architecture
- End-to-end flow
- Decision engine
- Integration
- Governance
- Technical Q&A

## Frontend Engineer

- Brief UI walkthrough if needed

## AI Engineer

- AI prompt, validation, ambiguity, fallback

## Backend Engineer

- Rule engine, priority, persistence, audit

You remain the person who connects all explanations.

---

# 78. Your Demo Script

## Opening

> “DecisionFlow AI helps business teams convert natural-language policies into governed, executable decision rules without changing core application code.”

## Architecture

> “AI interprets and explains policy language, while a deterministic rule engine makes the final decision. Human approval remains mandatory before activation.”

## Policy Studio

> “The user describes a telecom eligibility policy. AI maps it only to supported fields and operators, returns assumptions and confidence, and the backend validates it before saving.”

## Activation

> “The policy remains a draft until a human activates it. Activation creates a version and audit event.”

## Evaluation

> “The customer request is evaluated against all active policies. The highest-priority matching policy determines the outcome.”

## Explainability

> “We show the winning rule, every matched condition, the actual and expected values, priority resolution, confidence, and a human-readable explanation.”

## Reliability

> “If the AI provider fails, decision execution continues and the system uses a deterministic explanation fallback.”

## Close

> “The same platform can be configured for lending, insurance, fraud, promotions, compliance, or operational decisioning without rewriting the core engine.”

---

# 79. Architecture Questions You Must Be Ready For

## Why one FastAPI application instead of microservices?

The POC needs clear boundaries without deployment complexity. Internal service modules can later be separated if scale requires it.

## Why MySQL?

It provides realistic relational persistence, transactions, indexes, JSON support, and a straightforward enterprise migration path.

## Why custom rule engine?

The MVP needs a small deterministic operator set and transparent evaluation traces. A custom engine is easier to understand, test, and demonstrate.

## Why direct LLM SDK?

The workflow is structured generation and explanation. A multi-agent framework would add unnecessary complexity.

## Why AI confidence and decision confidence separately?

AI confidence reflects policy interpretation quality. Decision confidence reflects deterministic evidence completeness and conflicts.

## Why human activation?

AI-generated configuration must be reviewed before affecting business decisions.

---

# 80. Integration Definition of Done

Your role is complete only when all of the following are true.

## Architecture

- Module boundaries are followed.
- API contract is stable.
- Shared schemas are aligned.

## Backend

- MySQL runs.
- Migrations run.
- Seed runs.
- Rule engine works.
- Policy CRUD works.
- Audit and analytics work.

## AI

- Mock provider works.
- One real provider works if available.
- Policy generation works.
- Ambiguity works.
- Explanation works.
- Fallback works.

## Decision orchestration

- Decision Service works.
- Priority resolution works.
- Confidence works.
- Explanation failure does not block.
- Evaluation persists.
- Audit persists.

## Frontend

- Real API mode works.
- Policy flow works.
- Decision flow works.
- Analytics render.
- Audit renders.

## Packaging

- Docker Compose works.
- README works.
- No secrets committed.
- Health and readiness work.

## Quality

- Backend tests pass.
- AI tests pass.
- Integration tests pass.
- Frontend type check passes.
- Frontend build passes.
- Demo rehearsal succeeds.

---

# 81. Final Handoff to Main

Before merging into `main`, record:

```text
Integration branch:
feature/integration

Backend commit:
<hash>

AI commit:
<hash>

Frontend commit:
<hash>

Integration commit:
<hash>

Backend tests:
<result>

AI tests:
<result>

Integration tests:
<result>

Frontend tests:
<result>

Frontend type check:
<result>

Frontend build:
<result>

Docker Compose:
<result>

Known limitations:
<list>
```

---

# 82. Final Merge Checklist

Before final merge:

- Pull latest `main`.
- Resolve conflicts.
- Run backend tests.
- Run AI tests.
- Run integration tests.
- Run frontend type check.
- Run frontend tests.
- Run frontend build.
- Start Docker stack.
- Run smoke flow.
- Review `.env.example`.
- Review `.gitignore`.
- Search repository for secrets.
- Verify README.
- Tag stable commit if useful.

---

# 83. Final Integration Handoff Message

```text
DecisionFlow AI integration complete

Branch:
feature/integration

Latest commit:
<commit hash>

Integrated modules:
- MySQL persistence
- Policy CRUD
- Rule engine
- Priority resolver
- Decision confidence
- AI policy generation
- Ambiguity detection
- Decision explanation
- Deterministic fallback
- Evaluation persistence
- Audit
- Analytics
- React frontend

Run:
1. cp .env.example .env
2. docker compose up --build
3. open http://localhost:5173

Swagger:
http://localhost:8000/docs

Health:
http://localhost:8000/health

Readiness:
http://localhost:8000/ready

Test results:
- Backend: <result>
- AI: <result>
- Integration: <result>
- Frontend: <result>
- Type check: <result>
- Build: <result>

Demo flows verified:
- AI policy generation
- Ambiguity detection
- Policy activation
- Approval
- Fraud rejection
- Missing-field manual review
- AI explanation fallback
- Audit
- Analytics

Known limitations:
- <list>

API contract deviations:
- None
```

---

# 84. Final Instruction to You

Your role is not to write all the code.

Your role is to make sure all code becomes one product.

Focus on:

- Stable contracts
- Early handoffs
- Clear imports
- Deterministic orchestration
- Safe AI fallbacks
- MySQL reliability
- Frequent integration
- End-to-end verification
- Demo readiness

Do not allow teammates to work for hours without producing an integration-ready checkpoint.

Do not postpone integration until all modules are “complete.”

Integrate the smallest working version first, then improve each module.

The final standard is:

```text
Business user can create a policy
    ↓
Human can activate it
    ↓
Customer can be evaluated
    ↓
Decision is deterministic
    ↓
Explanation is understandable
    ↓
Audit is traceable
    ↓
Analytics are measurable
```

When that complete flow works reliably, DecisionFlow AI is ready for the hackathon demo.
