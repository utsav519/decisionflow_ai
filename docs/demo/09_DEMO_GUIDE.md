# DecisionFlow AI
## Final Demo, Presentation, Rehearsal, and Reviewer Q&A Guide

---

## 1. Purpose

This guide defines the final demo flow for the integrated DecisionFlow AI proof of concept.

It is designed for:

- Internal technical review
- VP-level or leadership review
- Stakeholder handoff
- Hackathon-style presentation
- Final integration approval
- Release-candidate validation before promotion to `main`

This guide reflects the actual integrated product currently available on:

```text
feature/integration
```

Current integrated release-candidate commit:

```text
f3f7820 merge: integrate frontend decision center
```

The documentation and final cleanup work is maintained on:

```text
work/final-documentation
```

---

## 2. Product Name

```text
DecisionFlow AI
```

Suggested subtitle:

```text
Governed AI-Assisted Decision Automation
```

---

## 3. One-Sentence Product Pitch

> “DecisionFlow AI helps business users author and understand policies with AI while keeping every final business decision deterministic, explainable, auditable, and governed.”

---

## 4. Problem Statement

Business decisioning systems often face four recurring problems:

1. Policy authoring is slow and requires technical support.
2. Rules become difficult to trace and explain.
3. Conflicting policies create inconsistent outcomes.
4. Pure AI-based decisioning can introduce unpredictability and governance risk.

DecisionFlow AI addresses these problems by separating AI assistance from final decision authority.

---

## 5. Solution Statement

DecisionFlow AI provides:

- AI-assisted policy generation
- Human-controlled policy activation
- Deterministic policy evaluation
- Priority-based conflict resolution
- Decision-confidence calculation
- Human-readable explanation
- Full policy and condition trace
- MySQL persistence
- Correlation-ID based traceability
- Audit records
- Analytics APIs
- Safe deterministic fallback when AI is unavailable

---

## 6. Core Product Principle

```text
AI assists.
Humans govern.
The deterministic engine decides.
```

The LLM can help create or explain policies, but it cannot override the rule engine’s final decision.

---

## 7. What the Demo Must Prove

The demo should prove that:

- The React frontend is connected to the real FastAPI backend.
- The backend evaluates active policies from MySQL.
- More than one policy can match.
- Policy priority decides the winner deterministically.
- Missing data does not cause the system to guess.
- AI explanation failure does not block the decision.
- Decision traces and warnings are visible.
- Correlation IDs make the request auditable.
- The same evaluation can be retrieved later.
- The solution is more than a chatbot.

---

## 8. Recommended Demo Duration

### Seven-minute version

```text
0:00–0:40  Product problem and principle
0:40–1:20  Architecture
1:20–2:30  Approval scenario
2:30–3:40  Rejection scenario
3:40–4:40  Missing-fields scenario
4:40–5:30  Explainability and trace
5:30–6:20  Reliability and AI fallback
6:20–7:00  Business value and closing
```

### Ten-minute version

Add:

- Swagger API view
- Policy priority discussion
- Correlation-ID trace
- Persisted evaluation retrieval
- Audit evidence
- Provider-abstraction explanation

### Twelve-minute extended version

Add:

- AI Policy Studio routes
- Policy activation governance
- Analytics endpoints
- Technical module ownership
- Limitations and roadmap
- Judge or reviewer questions

---

## 9. Speaker Roles

### Speaker 1 — Technical Architect / Integration Lead

Owns:

- Opening
- Architecture
- Integration explanation
- Decision orchestration
- Reliability
- Closing
- Reviewer Q&A

### Speaker 2 — Frontend Engineer

Owns:

- Decision Center navigation
- Input presets
- UI result explanation
- Policy trace demonstration

### Speaker 3 — AI Engineer

Owns:

- AI policy assistance
- Provider abstraction
- Explanation generation
- Safe fallback behaviour

### Speaker 4 — Backend / Rule Engine Engineer

Owns:

- Policy evaluation
- Priority resolution
- Persistence
- Audit
- API and MySQL details

One person may cover all roles for a smaller review.

---

## 10. Recommended Speaking Split

Keep the narration outcome-focused.

Avoid spending time on:

- Long code walkthroughs
- Every database table
- Every AI provider
- Every API route
- Internal implementation history
- Git conflict history

Focus on:

- What problem is solved
- Why the decision is trustworthy
- Why AI cannot override the engine
- How conflicts are resolved
- How failure is handled
- How the result is audited

---

## 11. Exact Demo Screen Sequence

Recommended browser and terminal order:

1. DecisionFlow AI Decision Center
2. Approval result
3. Expanded policy trace
4. Rejection result
5. Missing-fields result
6. Swagger decision endpoint
7. Health endpoint
8. Readiness endpoint
9. Optional audit API
10. Optional analytics API
11. Architecture slide or diagram
12. Closing slide

---

## 12. Demo Opening Script

> “Business policies change frequently, but traditional rule systems are difficult to author and explain, while pure AI decisioning can be unpredictable. DecisionFlow AI combines the usability of generative AI with deterministic execution, explicit governance, MySQL persistence, and complete auditability.”

Then state:

> “AI assists with authoring and explanation, but the rule engine alone produces the final decision.”

---

## 13. Architecture Explanation

Use this architecture:

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
        |                         - conflict assistance
        |                         - explanation
        |                               |
        +---------------+---------------+
                        |
                        v
             MySQL + Audit Trail
```

Recommended narration:

> “The frontend sends a structured customer request to FastAPI. The Decision Service loads active policies, maps public API fields into the internal policy catalogue, runs the deterministic engine, resolves policy conflicts by priority, calculates decision confidence, and persists the complete result. AI is called only for assistance and explanation.”

---

## 14. Decision Processing Order

Explain the sequence:

1. Validate request.
2. Load active policies.
3. Map API fields to policy paths.
4. Evaluate conditions.
5. Separate matched, unmatched, and skipped policies.
6. Resolve conflicts by priority.
7. Calculate confidence.
8. Generate explanation.
9. Fall back deterministically if AI fails.
10. Persist evaluation.
11. Write audit records.
12. Return correlation ID and metrics.

---

## 15. Policy Catalogue Used in the Demo

Five active telecom policies are used:

| Priority | Policy | Final result |
|---:|---|---|
| 300 | Fraud rejection | REJECT |
| 250 | Fraud manual review | MANUAL_REVIEW |
| 220 | Outstanding balance rejection | REJECT |
| 120 | Premium override approval | APPROVE |
| 100 | Standard upgrade approval | APPROVE |

When multiple policies match, the policy with the highest priority wins.

---

## 16. Decision Center Overview

The integrated Decision Center provides:

- Customer decision-input form
- Approval preset
- Rejection preset
- Missing-fields preset
- Live API evaluation
- Loading state
- Final decision badge
- Decision confidence
- Winning policy
- Policy count metrics
- Engine and total latency
- AI or deterministic explanation
- Expandable policy trace
- Expected and actual values
- Warnings
- Evaluation ID
- Correlation ID

---

## 17. Decision Center — Approval Scenario

Click:

```text
Approval
Run decision evaluation
```

The integrated preset contains values similar to:

```json
{
  "customer_id": "CUST-DEMO-APPROVE",
  "customer_tenure_months": 36,
  "credit_score": 790,
  "payment_defaults": 0,
  "fraud_risk_score": 0.12,
  "customer_segment": "PREMIUM",
  "outstanding_balance": 0,
  "account_status": "current"
}
```

Expected result:

```text
Decision: APPROVE
Confidence: 70%
Winning policy: Premium override approval
Matched policies: 2
Skipped policies: 0
```

Expected matched policies:

```text
Premium override approval
Standard upgrade approval
```

---

## 18. Approval Result Narration

Point out:

- Final decision
- Decision confidence
- Winning policy
- Two matched policies
- Condition trace
- Explanation source
- Engine latency
- Total latency
- Evaluation ID
- Correlation ID

Recommended narration:

> “The final outcome is APPROVE. The deterministic engine evaluated the full active policy set. Two approval policies matched, and the Premium override policy won because it has the higher priority.”

Then:

> “The explanation is generated after the decision. It describes the outcome but does not influence it.”

---

## 19. Decision Confidence Explanation

Use:

> “Decision confidence reflects how complete and internally consistent the deterministic evaluation evidence is. It is not a probability of future customer behaviour.”

Do not describe the confidence value as guaranteed accuracy.

---

## 20. AI Confidence Versus Decision Confidence

Use:

> “AI confidence describes the quality of AI interpretation or generation. Decision confidence describes deterministic evidence completeness. They are intentionally separate.”

---

## 21. Decision Center — Rejection Scenario

Click:

```text
Rejection
Run decision evaluation
```

The integrated preset uses an outstanding-balance rejection scenario.

Typical values:

```json
{
  "customer_id": "CUST-DEMO-REJECT",
  "customer_tenure_months": 36,
  "credit_score": 790,
  "payment_defaults": 0,
  "fraud_risk_score": 0.12,
  "customer_segment": "PREMIUM",
  "outstanding_balance": 1000,
  "account_status": "past_due"
}
```

Expected result:

```text
Decision: REJECT
Confidence: 60%
Winning policy: Outstanding balance rejection
Matched policies: 3
Conflicts detected: at least 1
```

The approval policies may also match, but the rejection policy has a higher priority.

---

## 22. Priority Override Narration

Recommended narration:

> “This customer satisfies some upgrade criteria, so approval policies also match. However, the outstanding-balance rejection policy has priority 220, which is higher than the approval priorities of 120 and 100. The system therefore returns REJECT deterministically.”

Then:

> “The system does not stop at the first matching rule. It evaluates the active policy set and resolves conflicts using an explicit and testable priority strategy.”

Point out:

- Multiple matched policies
- Winning policy
- Priority values
- Resolution reason
- Condition trace
- Conflict count
- Explanation

---

## 23. Optional Fraud-Risk Scenario

The current frontend does not provide a dedicated high-fraud preset.

This scenario may be demonstrated through Swagger or `curl`.

Example customer data:

```json
{
  "customer_id": "CUST-FRAUD-DEMO",
  "customer_tenure_months": 42,
  "credit_score": 785,
  "payment_defaults": 0,
  "fraud_risk_score": 0.91,
  "customer_segment": "PREMIUM",
  "outstanding_balance": 0,
  "account_status": "current"
}
```

Expected winning policy:

```text
Fraud rejection
```

Expected final decision:

```text
REJECT
```

Use this only in an extended technical review.

---

## 24. Decision Center — Missing-Fields Scenario

Click:

```text
Missing fields
Run decision evaluation
```

The preset deliberately omits important fields.

Expected result:

```text
Decision: MANUAL REVIEW
Confidence: 0%
Winning policy: No winning policy
Policies skipped: 5
Explanation source: DETERMINISTIC_FALLBACK
Warning: MISSING_REQUIRED_FIELDS
```

Expected policy statuses:

```text
SKIPPED_MISSING_FIELD
```

---

## 25. Missing-Fields Narration

Recommended narration:

> “When required evidence is unavailable, the system does not ask AI to invent the missing facts. It skips policies that cannot be evaluated and routes the case to manual review.”

Then:

> “The warning identifies the missing-field condition, and the policy trace explains exactly why each policy could not be evaluated.”

This is a key governance and safety point.

---

## 26. Policy Trace Demonstration

Expand at least one matched policy.

Show:

- Policy name
- Priority
- Result status
- Field
- Operator
- Expected value
- Actual value
- Matched or unmatched condition

Recommended narration:

> “Every decision is reproducible because the response stores the evaluated policy version and each condition’s expected and actual values.”

Do not open every policy in a short demo.

---

## 27. Explanation Demonstration

Show:

- Explanation summary
- Key factors
- Generated-by source
- Fallback indicator

Recommended narration:

> “The explanation layer converts the deterministic result into business-readable language. Even if the AI provider fails, the platform returns a deterministic fallback explanation.”

---

## 28. Reliability Demonstration

Explain the tested AI-failure path:

```text
Deterministic decision remains unchanged
API response remains successful
Fallback explanation is returned
AI_EXPLANATION_UNAVAILABLE warning is added
DECISION_EVALUATED audit is written
AI_EXPLANATION_FAILED audit is written
Correlation ID remains consistent
```

Recommended narration:

> “AI is not on the critical decision path. Provider failure degrades explanation quality but never blocks or changes the business decision.”

---

## 29. Correlation-ID Demonstration

Point to the correlation ID shown in the frontend result footer.

Explain:

> “The same correlation ID is carried through the request, response header, response body, persisted evaluation, audit records, and application logs.”

This supports operational tracing and incident investigation.

---

## 30. Persisted Evaluation Retrieval

Use the returned evaluation ID.

Endpoint:

```http
GET /api/v1/decisions/{evaluation_id}
```

Example:

```bash
curl \
  -H "X-Correlation-ID: cor_retrieve_demo" \
  http://localhost:8000/api/v1/decisions/<evaluation_id>
```

Explain:

> “The decision can be retrieved later with the same winning policy, trace, explanation, metrics, warnings, and evaluation timestamp.”

---

## 31. Swagger Backup Flow

Open:

```text
http://localhost:8000/docs
```

Use:

```http
POST /api/v1/decisions/evaluate
```

Example request:

```json
{
  "request_id": "req_swagger_demo",
  "domain": "telecom",
  "customer": {
    "customer_id": "CUST-SWAGGER-001",
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
}
```

Swagger is the backup when the frontend is unavailable.

---

## 32. Audit Demonstration

Available routes:

```text
GET /api/v1/audit
GET /api/v1/audit/{audit_id}
```

Show, when available:

- Action
- Entity type
- Entity ID
- Correlation ID
- User ID
- Timestamp
- Decision evaluation action
- AI explanation failure action

Narration:

> “The platform records what happened, which object was affected, and which request caused it.”

---

## 33. Analytics Demonstration

Available routes:

```text
GET /api/v1/analytics/dashboard
GET /api/v1/analytics/summary
GET /api/v1/analytics/decision-distribution
GET /api/v1/analytics/decision-trend
GET /api/v1/analytics/top-policies
```

The current integrated frontend does not include full analytics screens.

Use Swagger or API output during an extended technical review.

---

## 34. AI Policy Studio Demonstration

Available backend routes:

```text
POST /api/v1/ai/policies/generate
POST /api/v1/ai/policies/clarify
POST /api/v1/ai/policies/check-conflicts
POST /api/v1/ai/policies/generate-tests
POST /api/v1/ai/decisions/explain
```

The current integrated frontend focuses on the Decision Center.

Present AI Policy Studio through Swagger only when time permits.

---

## 35. Human Governance Narration

Use:

> “AI-generated policies remain drafts. Human review and activation are required before a policy becomes part of the active decision set.”

Explain:

- AI can propose policy structure.
- Validation checks the structure.
- Conflict checks help reviewers.
- A human controls activation.
- Only active policies are evaluated.

---

## 36. Environment Startup

The current project exposes MySQL and backend services through Docker Compose.

The frontend runs separately using Vite.

### Terminal 1 — MySQL

```bash
cd ~/Desktop/decisionflow_ai

git switch feature/integration
git pull --ff-only origin feature/integration

docker compose up -d mysql
docker compose ps
```

Wait until MySQL is healthy.

### Terminal 2 — Backend

```bash
cd ~/Desktop/decisionflow_ai/backend
source .venv/bin/activate

alembic upgrade head

export LLM_PROVIDER=mock
export USE_MOCK_LLM=true
export ENABLE_AI_EXPLANATION=true

uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000
```

### Terminal 3 — Frontend

```bash
cd ~/Desktop/decisionflow_ai/frontend

npm install
npm run build
npm run lint
npm run dev
```

Open:

```text
http://localhost:5173
```

Use `localhost`, not `127.0.0.1`, because the local backend CORS configuration permits `http://localhost:5173`.

---

## 37. Local URLs

```text
Frontend:
http://localhost:5173

Backend:
http://localhost:8000

Swagger:
http://localhost:8000/docs

OpenAPI:
http://localhost:8000/openapi.json

Health:
http://localhost:8000/health

Readiness:
http://localhost:8000/ready
```

---

## 38. Startup Verification Commands

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl "http://localhost:8000/api/v1/policies?status=ACTIVE"
curl http://localhost:8000/api/v1/analytics/summary
```

Expected:

- Health returns `healthy`.
- Readiness returns `ready`.
- Database is available.
- Database type is MySQL.
- Rule engine is available.
- Five active seed policies are available.
- Analytics response is valid.

---

## 39. Backend Validation Before Demo

```bash
cd ~/Desktop/decisionflow_ai/backend
source .venv/bin/activate
pytest -q
```

Expected baseline:

```text
140 passed
```

Verify decision routes:

```bash
python - <<'PY'
from app.main import app

paths = {route.path for route in app.routes}

assert "/api/v1/decisions/evaluate" in paths
assert "/api/v1/decisions/{evaluation_id}" in paths
assert "/health" in paths
assert "/ready" in paths

print("BACKEND_ROUTES_OK")
PY
```

---

## 40. Frontend Validation Before Demo

```bash
cd ~/Desktop/decisionflow_ai/frontend

npm run build
npm run lint
```

Expected:

```text
Production build passed
ESLint passed
```

---

## 41. Demo Reset Procedure

Avoid destructive database resets immediately before the demo.

Preferred reset:

1. Stop backend and frontend.
2. Keep the existing MySQL volume.
3. Restart MySQL.
4. Apply migrations.
5. Re-run seed only when the seed implementation is idempotent.
6. Verify active policy count.
7. Run all three frontend presets once.

Commands:

```bash
cd ~/Desktop/decisionflow_ai

docker compose stop mysql
docker compose start mysql
docker compose ps

cd backend
source .venv/bin/activate
alembic upgrade head
```

Use a full volume reset only when the database is corrupted or test data cannot be safely cleaned.

Inspect volume names with:

```bash
docker volume ls
```

---

## 42. Stable Demo State

The safest demo preparation is:

1. Start services several hours before the review.
2. Confirm MySQL health.
3. Apply migrations.
4. Confirm five active policies.
5. Run backend tests.
6. Run frontend build and lint.
7. Run Approval.
8. Run Rejection.
9. Run Missing Fields.
10. Confirm policy traces.
11. Confirm warnings.
12. Confirm correlation IDs.
13. Leave services running.
14. Disable notifications.
15. Avoid package upgrades.
16. Avoid branch switching.
17. Avoid destructive resets.

---

## 43. Real AI Versus Mock AI

### Use real AI when

- API key is valid.
- Network is stable.
- Output structure is verified.
- Provider latency is acceptable.
- Cost is approved.
- A fallback has already been tested.

### Use mock AI when

- Network reliability is uncertain.
- Provider limits are uncertain.
- Demo timing must be predictable.
- Structured output variability creates risk.
- Credentials must not be exposed.
- Cost control is required.

Recommended explanation:

> “The platform uses a provider abstraction. For demo reliability we use a deterministic mock provider, while the React frontend, FastAPI API, MySQL persistence, rule engine, priority resolution, audit trail, and decision trace remain fully real.”

---

## 44. What Must Remain Real

These components should remain real during the demo:

```text
React frontend
FastAPI backend
MySQL persistence
Active policy loading
Rule evaluation
Priority resolution
Decision confidence
Evaluation persistence
Policy trace
Warnings
Correlation ID
Audit records
```

Mock AI must not turn the full demo into a static simulation.

---

## 45. Demo Failure Matrix

| Failure | Immediate response |
|---|---|
| Frontend does not load | Use Swagger |
| Backend does not start | Check MySQL and `.env` |
| MySQL unavailable | Check `docker compose ps` and logs |
| AI provider fails | Use mock provider or deterministic fallback |
| Approval result differs | Verify seed policies and input fields |
| Rejection result differs | Verify outstanding balance and policy priorities |
| Missing-fields result differs | Confirm omitted fields are actually empty |
| CORS error | Use `http://localhost:5173` |
| Browser cache issue | Hard refresh or restart Vite |
| Demo latency is high | Use mock AI |
| Analytics is empty | Keep focus on decision trace and audit |
| Frontend fails late | Continue from Swagger |
| Evaluation cannot be retrieved | Use the original response and logs |

---

## 46. Emergency Swagger Demo

When the frontend is unavailable:

1. Open Swagger.
2. Run Approval request.
3. Show final decision and winning policy.
4. Run Rejection request.
5. Show multiple matches and priority resolution.
6. Run Missing Fields request.
7. Show skipped policies and warning.
8. Retrieve one evaluation.
9. Show health and readiness.
10. Close with reliability explanation.

---

## 47. Static Backup Materials

Keep ready:

- Approval screenshot
- Rejection screenshot
- Missing-fields screenshot
- Architecture diagram
- Example response JSON
- Test result screenshot
- Health/readiness screenshot
- Handoff status document
- Updated README

Do not depend on static screenshots as the primary demo.

---

## 48. Browser Preparation

Before the review:

- Set zoom between 80% and 100%.
- Close unrelated tabs.
- Disable browser notifications.
- Open Decision Center.
- Open Swagger in a second tab.
- Open health in a third tab.
- Open readiness in a fourth tab.
- Keep no credentials visible.
- Keep developer tools closed unless needed.
- Confirm the frontend fits without horizontal scrolling.

---

## 49. Terminal Preparation

Prepare three terminals:

### Terminal 1

MySQL status and logs.

### Terminal 2

Backend server and logs.

### Terminal 3

Frontend Vite server.

Optional fourth terminal:

- `curl` requests
- Git status
- Test commands

Increase terminal font size for screen sharing.

---

## 50. Rehearsal Plan

### Rehearsal 1 — Functional

Confirm every action works without timing pressure.

### Rehearsal 2 — Timed

Run the seven-minute script.

### Rehearsal 3 — Failure simulation

Test:

- Frontend unavailable
- AI provider unavailable
- Missing fields
- Swagger backup
- Backend restart
- Browser refresh

### Rehearsal 4 — Reviewer Q&A

Practice architecture, governance, reliability, and scaling answers.

---

## 51. Rehearsal Scorecard

Score each item from 1 to 5:

| Area | Score |
|---|---:|
| Opening clarity | |
| Architecture clarity | |
| Approval flow | |
| Rejection flow | |
| Missing-fields flow | |
| Priority explanation | |
| AI governance explanation | |
| Reliability explanation | |
| Technical confidence | |
| Time control | |
| Closing strength | |

Do not present until all critical areas score at least 4.

---

## 52. Demo Narration Rules

Use these terms consistently:

```text
AI-assisted policy authoring
Human-governed activation
Deterministic evaluation
Priority-based conflict resolution
Decision confidence
Condition trace
Correlation ID
Audit trail
Deterministic fallback
Provider abstraction
```

Avoid:

```text
The AI decides
The model approved the customer
The LLM rejected the request
The result is guaranteed
The confidence is a probability
The system is fully production-ready
```

---

## 53. Key Differentiators

### Governed AI

AI assists but does not activate or decide.

### Deterministic outcomes

The same facts and policy versions produce the same result.

### Explainability

The platform shows why a policy matched and why it won.

### Auditability

Requests, decisions, failures, and correlation IDs are traceable.

### Reliability

AI failure does not block decisioning.

### Configurability

Policies are externalized and managed rather than hard-coded.

### Extensibility

The architecture can support telecom, lending, insurance, fraud, onboarding, and other domains.

---

## 54. Business Value

DecisionFlow AI can reduce:

- Policy implementation time
- Manual coding effort
- Decision inconsistency
- Review effort
- Audit preparation effort
- Operational dependency on AI availability

It can improve:

- Governance
- Policy transparency
- Release speed
- Decision reproducibility
- Business-user participation
- Root-cause analysis

---

## 55. Technical Value

The POC demonstrates:

- Modular FastAPI design
- SQLAlchemy repository pattern
- Alembic migration control
- MySQL persistence
- Deterministic rule evaluation
- Priority resolution
- AI-provider abstraction
- Typed React integration
- Resilient fallback behaviour
- Correlation-ID middleware
- Audit records
- End-to-end testing

---

## 56. Why MySQL?

Use:

> “MySQL provides durable relational storage, transactional behaviour, indexing, version history, audit support, and a realistic production-oriented persistence layer.”

---

## 57. Why Not SQLite?

Use:

> “SQLite is useful for lightweight local prototypes, but the project intentionally validates MySQL integration, transaction handling, migrations, and multi-user database behaviour.”

---

## 58. Why a Custom Rule Engine?

Use:

> “The POC requires transparent condition evaluation, explicit priority resolution, policy traces, missing-field handling, and tight control over deterministic behaviour. A focused rule engine made those behaviours easy to test and explain.”

---

## 59. Why One FastAPI Application?

Use:

> “A modular monolith keeps the POC operationally simple while preserving clear internal boundaries between policy management, AI services, decision orchestration, persistence, audit, and analytics.”

---

## 60. Why AI Does Not Decide

Use:

> “Business decisions require reproducibility and governance. LLM output can vary, so AI is used for assistance and explanation while the deterministic engine remains authoritative.”

---

## 61. How Hallucination Is Controlled

Explain:

- AI output is structured.
- Policy fields and operators come from catalogues.
- Generated policies require validation.
- Human activation is required.
- AI cannot invent missing customer facts.
- The engine executes only structured active policies.
- Fallback explanation is deterministic.

---

## 62. How Missing Data Is Handled

Use:

> “A policy that requires missing data is marked as skipped rather than treated as matched or silently failed. When evidence is insufficient, the final result can be manual review.”

---

## 63. How Policy Conflict Is Resolved

Use:

> “All active policies are evaluated. When multiple policies match, the highest-priority policy wins. The response still retains the competing matches and resolution reason.”

---

## 64. What Happens if Two Rules Have the Same Priority?

Use:

> “The resolver applies the configured deterministic tie-break strategy and records that the tie-breaker was used. Production governance should also prevent accidental equal-priority conflicts.”

---

## 65. How Versioning Works

Use:

> “The winning policy ID and version are stored with the evaluation, allowing the decision to be reproduced against the policy state used at that time.”

---

## 66. How Auditability Works

Use:

> “The system stores evaluation details, decision outcome, policy trace, warnings, explanation information, timestamps, user context, and correlation IDs. AI explanation failure creates an additional audit event.”

---

## 67. How the Engine Is Generic

Use:

> “The telecom use case is demo data. The engine evaluates structured fields, operators, conditions, priorities, and outcomes, so the same core design can support other domains with a different field catalogue and policies.”

---

## 68. Where Is Agentic AI?

Use:

> “The current POC is governed AI-assisted automation rather than an autonomous multi-agent system. The design intentionally limits AI authority because policy activation and final business decisions require deterministic control.”

---

## 69. Security and Privacy

Current POC controls:

- Environment-based credentials
- No committed API keys
- Human-controlled policy activation
- Deterministic decision authority
- Correlation-based traceability
- Configured local CORS
- Structured request validation

Production additions would include:

- Authentication
- Role-based authorization
- Secret management
- Encryption policy
- PII masking
- Rate limiting
- Input abuse controls
- Production logging policy
- Network controls
- Provider data-governance review

---

## 70. Known Limitations

Be transparent:

- The integrated frontend focuses on Decision Center.
- Policy-management UI is not integrated.
- Audit UI is not integrated.
- Analytics UI is not integrated.
- Frontend automated browser tests are not included.
- Frontend is not included as a Docker Compose service.
- Authentication and RBAC are outside the POC.
- Production observability is outside the POC.
- Real LLM providers require credentials and network access.
- Seed policies are telecom-specific.
- Confidence values are rule-based, not statistically calibrated probabilities.

---

## 71. Future Enhancements

### Phase 1

- Policy-management UI
- Audit UI
- Analytics dashboard
- Browser automation tests
- Frontend Docker service
- Improved demo reset command

### Phase 2

- RBAC
- Policy approval workflow
- Policy simulation
- Bulk evaluation
- Version comparison
- Better operational metrics
- Provider cost monitoring

### Phase 3

- Multi-domain field catalogues
- Event-driven evaluation
- Horizontal scaling
- Model gateway
- Advanced policy conflict detection
- Enterprise observability
- Policy deployment environments

---

## 72. Reviewer Question — What Is Novel?

Use:

> “The novelty is not simply calling an LLM. The value comes from combining AI-assisted policy work with human governance, deterministic execution, explicit conflict resolution, condition-level explanation, persistence, and safe failure behaviour.”

---

## 73. Reviewer Question — Can AI Activate a Policy?

Use:

> “No. AI can propose a draft, but activation is a governed human-controlled operation.”

---

## 74. Reviewer Question — Can the LLM Change the Decision?

Use:

> “No. The explanation service receives the already-finalized deterministic outcome. It cannot modify the decision.”

---

## 75. Reviewer Question — What Happens When AI Is Down?

Use:

> “The deterministic decision still completes. A deterministic explanation is returned, a warning is added, and AI failure is audited.”

---

## 76. Reviewer Question — How Do You Prevent Contradictory Policies?

Use:

> “The system can identify conflicts during policy review, and runtime resolution uses explicit policy priorities. The complete match set and winning-policy reason remain visible.”

---

## 77. Reviewer Question — Is Confidence Calibrated?

Use:

> “The current decision confidence is a deterministic evidence-quality indicator, not a statistically calibrated probability. Production calibration could be added using historical outcome data.”

---

## 78. Reviewer Question — How Would This Scale?

Use:

> “The application can be containerized, the API scaled horizontally, MySQL tuned or managed, evaluation workers separated for bulk processing, and AI calls isolated through a provider gateway. The modular boundaries already support that evolution.”

---

## 79. Reviewer Question — Why Is This More Than a Chatbot?

Use:

> “The chatbot-like AI layer is only one component. The product includes policy management, deterministic rule execution, conflict resolution, persistence, audit, analytics APIs, traceability, and a live operational frontend.”

---

## 80. Seven-Minute Demo Script

### 0:00–0:40 — Opening

State the problem and core principle.

### 0:40–1:20 — Architecture

Show React, FastAPI, Decision Service, rule engine, AI services, MySQL and audit.

### 1:20–2:30 — Approval

Run Approval preset and show two matching policies.

### 2:30–3:40 — Rejection

Run Rejection preset and explain priority override.

### 3:40–4:40 — Missing Fields

Run Missing Fields and explain deterministic manual review.

### 4:40–5:30 — Traceability

Expand one policy and show evaluation ID and correlation ID.

### 5:30–6:20 — Reliability

Explain AI-failure fallback and audit records.

### 6:20–7:00 — Closing

Summarize business value and deterministic governance.

---

## 81. Five-Minute Emergency Demo

### 0:00–0:30

Product problem and principle.

### 0:30–1:00

Architecture.

### 1:00–2:00

Approval scenario.

### 2:00–3:00

Rejection scenario.

### 3:00–3:45

Missing-fields scenario.

### 3:45–4:30

AI fallback and audit.

### 4:30–5:00

Closing.

---

## 82. Twelve-Minute Extended Demo

Add:

- Swagger decision endpoint
- Optional fraud-risk request
- Persisted evaluation retrieval
- Audit endpoint
- Analytics endpoint
- AI Policy Studio routes
- Technical limitations
- Roadmap

---

## 83. Final Rehearsal Checklist

```text
[ ] Opening is under 45 seconds
[ ] Architecture is under 60 seconds
[ ] Approval preset returns APPROVE
[ ] Approval winner is Premium override approval
[ ] Approval shows two matched policies
[ ] Rejection preset returns REJECT
[ ] Rejection winner is Outstanding balance rejection
[ ] Rejection shows three matched policies
[ ] Priority reason is visible
[ ] Missing Fields returns MANUAL REVIEW
[ ] Missing Fields shows no winning policy
[ ] Missing Fields uses deterministic fallback
[ ] Missing-field warning is visible
[ ] Policy trace expands
[ ] Correlation ID is visible
[ ] No HTTP 500 occurs
[ ] Swagger backup is ready
[ ] Closing is under 30 seconds
[ ] Total time is within limit
```

---

## 84. Final Technical Checklist

```text
[ ] feature/integration checked out
[ ] release-candidate commit verified
[ ] no uncommitted changes
[ ] MySQL service healthy
[ ] migration head current
[ ] five active policies available
[ ] backend tests pass
[ ] frontend production build passes
[ ] frontend lint passes
[ ] frontend uses real API mode
[ ] mock AI configured for predictable demo
[ ] real AI tested separately if used
[ ] health endpoint works
[ ] readiness endpoint works
[ ] only one /health route is registered
[ ] only one /ready route is registered
[ ] CORS works for http://localhost:5173
[ ] correlation IDs are visible
[ ] no secrets are visible
[ ] approval browser flow passes
[ ] rejection browser flow passes
[ ] missing-fields browser flow passes
[ ] AI-failure fallback passes
[ ] audit evidence is available
```

---

## 85. Final Presentation Checklist

```text
[ ] Product name is consistent
[ ] Speaker order is agreed
[ ] Demo owner is agreed
[ ] Mouse and keyboard owner is agreed
[ ] Browser tabs are ordered
[ ] Terminal fonts are readable
[ ] Notifications are disabled
[ ] Backup screenshots are ready
[ ] Swagger backup is ready
[ ] Architecture diagram is ready
[ ] Failure fallback is understood
[ ] Reviewer answers are rehearsed
[ ] Timekeeper is assigned
[ ] No credentials are visible
```

---

## 86. Final Demo Readiness Decision

Declare the build demo-ready only when:

```text
Frontend loads
Backend is healthy
Readiness confirms MySQL
Approval returns APPROVE
Rejection returns REJECT
Missing Fields returns MANUAL REVIEW
Policy trace is visible
Winning policy is visible
Warnings are visible
Correlation ID is visible
Evaluation persists
AI failure fallback works
No HTTP 500 occurs
```

---

## 87. Final Demo Message

Keep the product story:

```text
Natural-language policy assistance
        ↓
Structured and validated policy
        ↓
Human-governed activation
        ↓
Deterministic execution
        ↓
Explainable outcome
        ↓
Persistence, audit, and analytics
```

---

## 88. Strong Final One-Liner

> “DecisionFlow AI makes business policy easier to manage without giving up deterministic control, explainability, resilience, or auditability.”

---

## 89. Final Closing Script

> “This POC demonstrates that generative AI can improve how policies are created and understood without becoming the final decision-maker. DecisionFlow AI keeps business outcomes deterministic, priority-driven, explainable, persisted, and auditable—even when the AI provider is unavailable.”

---

## 90. Final Status

```text
Technical integration: COMPLETE
Demo readiness: READY
Documentation: UPDATED
Reviewer approval: PENDING
Promotion to main: PENDING
```

Do not merge `feature/integration` into `main` before final reviewer approval.
