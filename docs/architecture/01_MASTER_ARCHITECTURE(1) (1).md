# DecisionFlow AI
## Master Architecture and Product Blueprint

**Document ID:** DFA-ARCH-001  
**Version:** 1.1  
**Status:** Hackathon POC Baseline — MySQL Edition  
**Primary Owner:** Technical Architect and Integration Lead  
**Target Domain:** Telecom customer eligibility and risk decisioning  
**Underlying Product Type:** Domain-independent configurable decision automation platform

---

## 1. Executive Summary

DecisionFlow AI is an AI-assisted, configurable decision automation platform that helps business teams translate natural-language policies into validated, executable rules without requiring frequent application code changes.

The proof of concept is demonstrated using a telecom use case:

> Device-upgrade and premium-plan eligibility decisions for telecom customers.

A business user describes a policy in plain English. The AI converts that policy into a structured rule candidate. The platform validates the generated rule, identifies ambiguity or conflicts, and requires human approval before activation. Once active, a deterministic rule engine evaluates customer requests and returns an approval, rejection, or manual-review decision. Every decision includes matched rules, evidence, confidence indicators, latency, and an audit trail.

The key architectural principle is:

> AI assists with understanding, authoring, validation, and explanation. Deterministic software makes the final business decision.

---

## 2. Business Context

Large enterprises operate using policies that influence daily decisions across product, fraud, risk, operations, compliance, customer support, pricing, and eligibility.

Typical telecom decisions include:

- Is a customer eligible for a device upgrade?
- Can a customer move to a premium plan?
- Should a handset-financing request be approved?
- Should an application be rejected because of fraud risk?
- Should a borderline case be sent for manual review?
- Does a customer qualify for a promotional benefit?
- Should an exception policy override a standard rule?

These decisions are usually based on multiple business conditions such as:

- Customer tenure
- Payment history
- Credit score
- Fraud-risk score
- Monthly bill amount
- Customer segment
- Requested device price
- Existing plan
- Outstanding balance
- Number of previous defaults

---

## 3. Problem Today

In many organizations, policy logic is hardcoded inside applications or distributed across multiple systems and teams.

A typical policy-change workflow looks like:

```text
Business Team
    ↓
Requirement Email or Document
    ↓
Business Analyst Interpretation
    ↓
Developer Implementation
    ↓
Testing
    ↓
Deployment
    ↓
Production Release
```

This creates several problems.

### 3.1 Slow policy changes

Even a small threshold change can require a development and deployment cycle.

Example:

```text
Old policy:
Approve when tenure >= 24 months.

New policy:
Approve when tenure >= 18 months for premium customers.
```

A simple business change may take days or weeks to reach production.

### 3.2 Engineering dependency

Business users cannot configure policies independently because they do not know:

- JSON schemas
- Internal field names
- Supported operators
- Data types
- Application code
- Deployment procedures

### 3.3 Scattered and inconsistent rules

Rules may exist across:

- Backend services
- SQL queries
- Stored procedures
- Configuration files
- Spreadsheets
- Manual operational procedures

This makes policy ownership unclear.

### 3.4 Limited explainability

A system may return `REJECT`, but the user may not know:

- Which rule caused the rejection
- Which customer values were used
- Whether another rule also matched
- Which rule had higher priority
- Which policy version was active

### 3.5 Weak auditability

Without a structured audit layer, it is difficult to prove:

- Which rules were evaluated
- Which version was used
- Why a final outcome was selected
- Who created or approved the policy
- Whether AI was involved
- How long the evaluation took

### 3.6 Rule conflicts and ambiguity

Policies written in natural language may overlap or contradict each other.

Example:

```text
Rule A:
Approve customers with credit score >= 700.

Rule B:
Reject customers with credit score < 750.
```

Scores from 700 to 749 satisfy both rules.

Without conflict detection and deterministic priority handling, outcomes become unreliable.

---

## 4. Problem Statement

Telecom product and risk teams need to update eligibility and risk policies frequently, but existing decision logic is often hardcoded, difficult to audit, difficult to explain, and dependent on engineering teams.

They need a configurable platform that:

1. Converts business-language policies into structured rule candidates.
2. Validates policy fields, operators, and values.
3. Identifies ambiguity and conflicting rules.
4. Requires human review before rule activation.
5. Evaluates customer requests deterministically.
6. Produces explainable decisions.
7. Maintains a complete audit trail.
8. Provides analytics and evaluation metrics.
9. Allows policy changes without modifying core application code.

---

## 5. Proposed Solution

DecisionFlow AI provides the following end-to-end lifecycle:

```text
Natural-Language Policy
    ↓
AI Rule Generation
    ↓
Schema and Semantic Validation
    ↓
Ambiguity and Conflict Detection
    ↓
Human Review and Approval
    ↓
Policy Activation
    ↓
Customer Request Evaluation
    ↓
Deterministic Rule Engine
    ↓
Decision and Evidence
    ↓
AI-Assisted Explanation
    ↓
Audit and Analytics
```

---

## 6. Product Positioning

### 6.1 Demonstration domain

The POC uses telecom customer eligibility and risk decisioning.

Primary demo scenario:

> Device-upgrade eligibility for an existing telecom customer.

### 6.2 Platform positioning

The architecture remains generic.

The same engine can later support:

- Loan eligibility
- Insurance underwriting
- Fraud screening
- E-commerce promotions
- Healthcare pre-authorization
- Employee-policy validation
- Customer-support escalation
- Compliance checks

### 6.3 One-line product pitch

> DecisionFlow AI converts natural-language business policies into validated rule candidates and executes transparent, deterministic decisions through a configurable decision engine.

### 6.4 Leadership pitch

> Today, business policy changes often require analyst interpretation, developer implementation, testing, and deployment. DecisionFlow AI reduces the gap between business intent and executable logic. Business users describe policies in natural language, AI converts them into validated rule candidates, humans approve them, and a deterministic engine executes customer decisions with complete explainability and auditability.

---

## 7. MVP Scope

The MVP must demonstrate a complete business workflow rather than isolated technical components.

### 7.1 Included

- Admin dashboard
- Policy list
- AI Policy Studio
- Manual policy creation
- Natural-language policy generation
- Policy validation
- Ambiguity detection
- Basic conflict detection
- Human approval and activation
- Policy enable/disable
- Decision evaluation screen
- Deterministic rule evaluation
- Priority-based resolution
- Decision explanation
- Decision confidence indicators
- Rule-generation confidence indicators
- Evaluation metrics
- Audit logs
- Dashboard analytics
- FastAPI backend
- MySQL 8.0+ persistence
- LLM provider integration
- Docker support if time permits
- Unit tests for critical flows

### 7.2 Explicitly out of scope

To keep the POC achievable:

- Enterprise authentication and RBAC
- Production-grade multi-tenancy
- Kubernetes deployment
- Complex workflow orchestration
- Real-time streaming infrastructure
- Full no-code drag-and-drop rule builder
- Distributed rule execution
- Large-scale model training
- Full regulatory compliance implementation
- Advanced policy simulation over millions of records
- Enterprise-grade observability stack

---

## 8. User Personas

### 8.1 Business Policy Manager

Creates or updates policies using natural language.

Needs:

- Simple policy authoring
- Clear validation
- Human-readable conditions
- Approval controls
- Conflict warnings

### 8.2 Risk or Fraud Analyst

Defines rejection and manual-review policies.

Needs:

- Priority controls
- Risk thresholds
- Conflict visibility
- Decision evidence
- Audit history

### 8.3 Operations User

Evaluates individual customer cases and reviews outcomes.

Needs:

- Input form
- Final decision
- Confidence
- Explanation
- Matched rules
- Latency and evaluation metrics

### 8.4 Technical Administrator

Maintains fields, operators, policies, and platform configuration.

Needs:

- Policy CRUD
- Policy status
- Audit logs
- Rule version visibility
- System metrics

### 8.5 Leadership or Reviewer

Needs:

- Business value
- Adoption metrics
- Decision distribution
- Policy-change speed
- Explainability
- Governance controls

---

## 9. Core Use Cases

### UC-01: Create policy using natural language

A user writes:

```text
Approve a device upgrade when customer tenure is at least 24 months,
payment defaults are zero, and credit score is at least 750,
unless fraud risk is above 0.6.
```

The AI generates a structured policy candidate.

### UC-02: Validate AI-generated policy

The platform verifies:

- Fields exist
- Operators are supported
- Value types are valid
- Required fields are present
- Logical structure is valid
- No unsupported conditions were invented

### UC-03: Detect ambiguity

Input:

```text
Approve loyal customers.
```

Expected behavior:

```text
The term "loyal" is ambiguous.
Please define loyalty using tenure, spend, segment, payment history,
or another supported field.
```

### UC-04: Detect policy conflicts

The system compares the candidate policy with active policies and flags potential overlaps.

### UC-05: Approve and activate policy

The user reviews the generated rule, edits if necessary, and explicitly activates it.

### UC-06: Evaluate a customer request

The user submits customer attributes. The engine evaluates all active policies.

### UC-07: Resolve competing outcomes

If multiple rules match, the engine uses deterministic priority and severity logic.

### UC-08: Explain decision

The user sees:

- Final decision
- Matched rules
- Failed conditions
- Winning rule
- Evidence
- Human-readable explanation

### UC-09: Review audit history

The user can view request, rule versions, timestamps, outcome, confidence, and latency.

### UC-10: View analytics

The dashboard displays decision volume, outcome distribution, average latency, and top-triggered policies.

---

## 10. Functional Modules

### 10.1 Admin Dashboard

Displays:

- Total policies
- Active policies
- Draft policies
- Pending approvals
- Disabled policies
- Total evaluations
- Approval rate
- Rejection rate
- Manual-review rate
- Average decision confidence
- Average latency
- Recent policy activity
- Recent decision activity

### 10.2 AI Policy Studio

Allows a business user to:

- Enter policy text
- Select domain fields
- Generate structured rule
- Review generated conditions
- Review AI confidence
- Review warnings
- View conflicts
- Edit the generated rule
- Save as draft
- Approve and activate

### 10.3 Policy Management

Supports:

- Create
- Read
- Update
- Delete
- Enable
- Disable
- View details
- Filter by status
- Filter by decision type
- View priority
- View version
- View creation source

### 10.4 Decision Center

Allows the user to:

- Enter customer attributes
- Evaluate request
- View decision
- View confidence
- View matched policies
- View unmatched conditions
- View explanation
- View latency
- View rules evaluated
- View warnings and conflicts

### 10.5 Analytics

Displays:

- Decisions by outcome
- Decisions over time
- Average latency
- Average confidence
- Most-triggered rules
- Approval/rejection/manual-review distribution
- Number of policies created with AI
- Validation error count

### 10.6 Audit Logs

Displays:

- Evaluation ID
- Timestamp
- Request payload
- Final decision
- Rule IDs and versions
- Matched rules
- Priority resolution
- Confidence
- Latency
- AI explanation status
- User or source

### 10.7 Settings

POC-level settings may include:

- LLM provider
- Model name
- Temperature
- Explanation enabled
- Default rule priority
- Supported domain
- Supported operators

---

## 11. High-Level Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    React Admin Dashboard                    │
│                                                             │
│ Dashboard | AI Policy Studio | Policies | Decision Center   │
│ Analytics | Audit Logs | Settings                           │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTPS / REST / JSON
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       FastAPI Backend                       │
│                                                             │
│  API Routers                                                │
│  ├── Policy Router                                          │
│  ├── AI Policy Router                                       │
│  ├── Decision Router                                        │
│  ├── Analytics Router                                       │
│  └── Audit Router                                           │
│                                                             │
│  Application Services                                       │
│  ├── Policy Service                                         │
│  ├── Decision Service                                       │
│  ├── Validation Service                                     │
│  ├── Conflict Service                                       │
│  ├── Explanation Service                                    │
│  ├── Analytics Service                                      │
│  └── Audit Service                                          │
│                                                             │
│  Core Engine                                                │
│  ├── Rule Evaluator                                         │
│  ├── Operator Registry                                      │
│  ├── Priority Resolver                                      │
│  └── Confidence Calculator                                  │
│                                                             │
│  AI Layer                                                   │
│  ├── LLM Provider                                           │
│  ├── Policy Generator                                       │
│  ├── Ambiguity Detector                                     │
│  ├── Conflict Assistant                                     │
│  ├── Decision Explainer                                     │
│  └── Test Case Generator                                    │
│                                                             │
│  Persistence                                                │
│  ├── Policy Repository                                      │
│  ├── Decision Repository                                    │
│  ├── Audit Repository                                       │
│  └── Analytics Queries                                      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                        MySQL Database                       │
│                                                             │
│ policies | policy_versions | evaluations | audit_logs       │
└─────────────────────────────────────────────────────────────┘
```

---

## 12. Architectural Principles

### 12.1 Deterministic decision execution

The final decision must be produced by the rule engine, not the LLM.

Reasons:

- Repeatability
- Auditability
- Testability
- Predictability
- Regulatory defensibility

### 12.2 AI-assisted authoring

AI is used where language understanding creates value:

- Natural language to structured rule
- Ambiguity detection
- Conflict explanation
- Decision explanation
- Test-case suggestions

### 12.3 Human approval before activation

No AI-generated policy becomes active automatically.

### 12.4 API-first design

Frontend, AI, engine, and persistence modules communicate through defined interfaces.

### 12.5 Domain-specific demo, generic engine

Telecom fields are used in the POC, but the rule engine remains field-agnostic.

### 12.6 Observable execution

Every decision records:

- Rules evaluated
- Matched conditions
- Winning rule
- Latency
- Confidence
- Policy version

### 12.7 Fail-safe behavior

When required information is missing or ambiguous, the system should return manual review or validation error rather than silently guessing.

---

## 13. Technology Stack

### Frontend

- React
- Vite
- TypeScript or JavaScript
- Tailwind CSS or a component library
- Axios or Fetch API
- Recharts or Chart.js

### Backend

- Python 3.11+
- FastAPI
- Pydantic
- SQLAlchemy
- Uvicorn
- MySQL 8.0+
- PyMySQL or mysql-connector-python
- Alembic for schema migrations

### Database

- MySQL 8.0+
- SQLAlchemy 2.x ORM
- PyMySQL as the default Python driver
- Alembic for repeatable schema migrations
- Connection pooling configured through SQLAlchemy
- UTC timestamps
- JSON columns for condition trees, request snapshots, result snapshots, and AI metadata
- Unique constraints and indexes defined in the database design document

Recommended local connection string:

```text
mysql+pymysql://decisionflow:decisionflow@localhost:3306/decisionflow
```

Recommended Docker Compose service name:

```text
mysql
```

The backend must not use SQLite-specific syntax or file paths. All persistence code must work against MySQL from the first implementation.

### AI

- OpenAI, Gemini, Claude, or available enterprise LLM
- Structured JSON output
- Prompt templates
- Provider abstraction

### Testing

- Pytest
- FastAPI TestClient
- Frontend smoke testing

### Packaging

- Git
- `.env`
- Docker and Docker Compose, including a MySQL service

---

## 13.1 MySQL Integration Baseline

The team will use MySQL rather than SQLite for all development, integration, testing, and demo persistence.

### Required environment variables

```text
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=decisionflow
MYSQL_USER=decisionflow
MYSQL_PASSWORD=decisionflow
DATABASE_URL=mysql+pymysql://decisionflow:decisionflow@localhost:3306/decisionflow
```

### Required Docker Compose behavior

The MySQL container should:

- Use MySQL 8.0 or newer.
- Expose port `3306`.
- Create the `decisionflow` database.
- Use a named volume so demo data survives container restarts.
- Include a health check.
- Start the backend only after MySQL is healthy.

### Required backend behavior

- Create SQLAlchemy sessions through one shared session factory.
- Use `pool_pre_ping=True`.
- Roll back failed transactions.
- Close sessions after each request.
- Never store database credentials in source control.
- Run Alembic migrations before seeding demo data.
- Seed data idempotently so the command can be executed more than once.

---

## 14. Repository Structure

```text
decisionflow-ai/
│
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── docs/
│   ├── 01_MASTER_ARCHITECTURE.md
│   ├── 02_API_CONTRACT.md
│   ├── 03_BACKEND_MODULE_GUIDE.md
│   ├── 04_AI_MODULE_GUIDE.md
│   ├── 05_FRONTEND_MODULE_GUIDE.md
│   ├── 06_INTEGRATION_GUIDE.md
│   ├── 07_DATABASE_DESIGN.md
│   ├── 08_GIT_WORKFLOW.md
│   └── 09_DEMO_GUIDE.md
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── v1/
│   │   │       ├── policies.py
│   │   │       ├── ai.py
│   │   │       ├── decisions.py
│   │   │       ├── analytics.py
│   │   │       └── audit.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── exceptions.py
│   │   │   └── logging.py
│   │   ├── schemas/
│   │   │   ├── policy.py
│   │   │   ├── decision.py
│   │   │   ├── analytics.py
│   │   │   └── common.py
│   │   ├── models/
│   │   │   ├── policy.py
│   │   │   ├── evaluation.py
│   │   │   └── audit.py
│   │   ├── repositories/
│   │   │   ├── policy_repository.py
│   │   │   ├── evaluation_repository.py
│   │   │   └── audit_repository.py
│   │   ├── services/
│   │   │   ├── policy_service.py
│   │   │   ├── decision_service.py
│   │   │   ├── validation_service.py
│   │   │   ├── conflict_service.py
│   │   │   ├── explanation_service.py
│   │   │   ├── analytics_service.py
│   │   │   └── audit_service.py
│   │   ├── engine/
│   │   │   ├── evaluator.py
│   │   │   ├── operators.py
│   │   │   ├── resolver.py
│   │   │   └── confidence.py
│   │   ├── ai/
│   │   │   ├── provider.py
│   │   │   ├── prompts.py
│   │   │   ├── policy_generator.py
│   │   │   ├── ambiguity_detector.py
│   │   │   ├── conflict_assistant.py
│   │   │   ├── explainer.py
│   │   │   └── test_case_generator.py
│   │   └── db/
│   │       ├── session.py
│   │       ├── base.py
│   │       └── seed.py
│   ├── tests/
│   │   ├── test_operators.py
│   │   ├── test_evaluator.py
│   │   ├── test_policy_api.py
│   │   └── test_decision_api.py
│   ├── requirements.txt
│   └── Dockerfile
│
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   ├── hooks/
    │   ├── types/
    │   ├── utils/
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    └── Dockerfile
```

---

## 15. Domain Field Catalogue

The POC should use a predefined allow-list of telecom fields.

| Field | Type | Description |
|---|---|---|
| customer_id | string | Unique customer identifier |
| customer_tenure_months | integer | Number of months with telecom provider |
| credit_score | integer | Customer credit score |
| payment_defaults | integer | Number of previous defaults |
| fraud_risk_score | number | Risk value from 0 to 1 |
| monthly_bill_amount | number | Monthly bill value |
| requested_device_price | number | Price of requested device |
| customer_segment | string | STANDARD, PREMIUM, BUSINESS |
| current_plan | string | Existing plan name |
| outstanding_balance | number | Current unpaid amount |
| is_existing_customer | boolean | Existing customer flag |
| previous_upgrade_months_ago | integer | Months since previous upgrade |

The LLM must not invent fields outside this catalogue.

---

## 16. Supported Operators

The initial engine should support:

- `equals`
- `not_equals`
- `greater_than`
- `greater_than_or_equal`
- `less_than`
- `less_than_or_equal`
- `contains`
- `in`
- `not_in`
- `is_empty`
- `is_not_empty`

Operator validation must ensure type compatibility.

Examples:

- `contains` is valid for strings or arrays.
- `greater_than` is valid for numeric fields.
- `is_empty` does not require a value.
- `in` requires a list value.

---

## 17. Policy Schema

A structured policy should follow this conceptual structure:

```json
{
  "name": "Premium device upgrade eligibility",
  "description": "Approves low-risk customers for premium device upgrades.",
  "domain": "telecom",
  "status": "DRAFT",
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
  "reason": "Customer satisfies tenure, payment, credit, and risk requirements.",
  "source": "AI_GENERATED",
  "version": 1
}
```

Nested groups may support:

```json
{
  "all": [
    {
      "field": "customer_tenure_months",
      "operator": "greater_than_or_equal",
      "value": 24
    },
    {
      "any": [
        {
          "field": "customer_segment",
          "operator": "equals",
          "value": "PREMIUM"
        },
        {
          "field": "monthly_bill_amount",
          "operator": "greater_than",
          "value": 3000
        }
      ]
    }
  ]
}
```

For the MVP, one level of nested `all` and `any` is sufficient.

---

## 18. Decision Outcomes

Supported outcomes:

- `APPROVE`
- `REJECT`
- `MANUAL_REVIEW`

Severity order:

```text
REJECT > MANUAL_REVIEW > APPROVE
```

Priority remains the primary resolution method. Severity may be used only as a deterministic tie-breaker.

---

## 19. Rule Evaluation Flow

```text
1. Receive decision request.
2. Validate request schema.
3. Load all active policies for the domain.
4. Evaluate each policy condition.
5. Record condition-level results.
6. Collect matched policies.
7. Sort matched policies by priority.
8. Resolve final decision.
9. Calculate deterministic decision confidence.
10. Generate optional AI explanation.
11. Save evaluation and audit data.
12. Return response to frontend.
```

---

## 20. Priority Resolution

Recommended strategy:

1. Highest priority value wins.
2. If multiple rules have the same priority:
   - `REJECT` wins over `MANUAL_REVIEW`
   - `MANUAL_REVIEW` wins over `APPROVE`
3. If priority and severity are identical:
   - Most recently approved version wins, or
   - Lowest rule ID wins for absolute determinism

The selected tie-breaker must be documented and consistently applied.

---

## 21. Confidence Model

The system must separate two different confidence concepts.

### 21.1 AI rule-generation confidence

Represents confidence that the natural-language policy was correctly mapped to structured fields and operators.

This should consider:

- All terms mapped to known fields
- No ambiguity found
- No unsupported operator generated
- No missing threshold
- No conflict detected
- Valid JSON and schema

Example heuristic:

```text
Base score: 100

-20 for each ambiguous term
-15 for unsupported or inferred field
-10 for conflict warning
-10 for missing threshold
-5 for low-quality description
```

The score should be presented as an assistive indicator, not mathematical certainty.

### 21.2 Decision confidence

The deterministic engine should calculate this without asking the LLM.

Possible factors:

- Required input completeness
- Ratio of evaluated conditions
- Number of conflicts
- Distance from thresholds
- Whether manual-review rules matched
- Whether all data types were valid

Simple MVP formula:

```text
Base = 100

-20 if required data is missing
-15 if conflicting policies match
-10 if any numeric value lies within a configurable boundary margin
-10 if manual-review rule wins
-5 for each skipped policy due to missing field
```

The exact heuristic must be documented in code and response metadata.

---

## 22. AI Responsibilities

### 22.1 Natural-language policy generation

Input:

```text
Approve customers with at least 24 months tenure,
no defaults, and a credit score of at least 750.
```

Output:

- Structured rule candidate
- Confidence score
- Warnings
- Ambiguities
- Assumptions
- Suggested test cases

### 22.2 Ambiguity detection

The AI must identify vague terms such as:

- loyal
- valuable
- high risk
- good customer
- expensive device
- long tenure
- low balance

The AI should ask for measurable definitions.

### 22.3 Conflict assistance

The AI can explain why two policies may overlap, but deterministic code must perform baseline conflict checks wherever possible.

### 22.4 Decision explanation

The AI receives structured evaluation evidence and converts it into user-friendly language.

The explanation must not invent facts.

### 22.5 Test-case generation

The AI may suggest:

- Positive case
- Negative case
- Boundary case
- Missing-field case
- Conflict case

---

## 23. AI Safety and Guardrails

Every AI-generated rule must pass through:

1. JSON parsing
2. Pydantic validation
3. Allowed-field validation
4. Allowed-operator validation
5. Type compatibility validation
6. Threshold validation
7. Logical structure validation
8. Conflict scan
9. Human review
10. Explicit activation

The AI must never directly persist an active policy.

---

## 24. Database Entities

### 24.1 Policy

Stores current policy metadata and active configuration.

### 24.2 Policy Version

Stores immutable historical versions.

### 24.3 Evaluation

Stores each decision request and result.

### 24.4 Evaluation Rule Result

Stores per-rule evaluation details.

### 24.5 Audit Log

Stores business and system actions.

Detailed schema will be defined in the database design document.

---

## 25. API Domains

The backend API should expose the following groups:

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

### AI Policy Studio

```text
POST /api/v1/ai/policies/generate
POST /api/v1/ai/policies/check-conflicts
POST /api/v1/ai/policies/generate-tests
```

### Decisions

```text
POST /api/v1/decisions/evaluate
GET  /api/v1/decisions
GET  /api/v1/decisions/{evaluation_id}
```

### Analytics

```text
GET /api/v1/analytics/summary
GET /api/v1/analytics/decision-distribution
GET /api/v1/analytics/top-policies
```

### Audit

```text
GET /api/v1/audit
GET /api/v1/audit/{audit_id}
```

Full request and response schemas will be defined in the API contract document.

---

## 26. End-to-End Policy Creation Flow

```text
User opens AI Policy Studio
    ↓
User enters natural-language policy
    ↓
Frontend sends request to FastAPI
    ↓
AI Policy Generator receives prompt and field catalogue
    ↓
LLM returns structured JSON candidate
    ↓
Validation Service checks schema and semantics
    ↓
Conflict Service compares candidate with active policies
    ↓
Response returned with:
    - Generated rule
    - Confidence
    - Warnings
    - Ambiguities
    - Conflicts
    ↓
User reviews and edits
    ↓
User saves as draft
    ↓
User activates policy
    ↓
Policy and version stored
    ↓
Dashboard statistics updated
```

---

## 27. End-to-End Decision Flow

```text
User opens Decision Center
    ↓
User enters customer data
    ↓
Frontend calls POST /decisions/evaluate
    ↓
Decision Service validates input
    ↓
Policy Service loads active policies
    ↓
Rule Engine evaluates every policy
    ↓
Priority Resolver selects final outcome
    ↓
Confidence Calculator generates deterministic score
    ↓
Explanation Service creates human-readable explanation
    ↓
Evaluation and rule results are stored
    ↓
Audit log is created
    ↓
Analytics become available
    ↓
Frontend displays:
    - Decision
    - Confidence
    - Matched policies
    - Winning policy
    - Evidence
    - Explanation
    - Latency
    - Rules evaluated
```

---

## 28. Error Handling Strategy

All modules should use a consistent error format.

Example:

```json
{
  "success": false,
  "error": {
    "code": "POLICY_VALIDATION_ERROR",
    "message": "The generated policy contains an unsupported field.",
    "details": [
      {
        "field": "customer_loyalty",
        "issue": "Field is not present in the approved field catalogue."
      }
    ],
    "correlation_id": "cor_12345"
  }
}
```

Recommended error categories:

- `VALIDATION_ERROR`
- `POLICY_NOT_FOUND`
- `POLICY_CONFLICT`
- `AI_PROVIDER_ERROR`
- `AI_OUTPUT_INVALID`
- `DATABASE_ERROR`
- `EVALUATION_ERROR`
- `MISSING_REQUIRED_FIELD`
- `UNSUPPORTED_OPERATOR`

---

## 29. Non-Functional Requirements

### Performance

- Target POC decision latency without explanation: under 300 ms
- AI explanation may be asynchronous or optional if provider is slow
- Dashboard APIs should respond under 1 second for small datasets

### Reliability

- Invalid AI output must not crash the backend
- Decision evaluation must work even when the LLM is unavailable
- Explanation should fall back to deterministic text

### Security

- API keys stored in `.env`
- Secrets excluded from Git
- Input payloads validated
- No arbitrary code execution
- Prompt input sanitized
- LLM receives only necessary context

### Auditability

- Every activation, update, disable, and decision is recorded
- Policy versions are immutable after activation

### Maintainability

- Clear folder ownership
- Small service interfaces
- No direct frontend-to-database access
- No business logic inside UI components

---

## 30. Team Ownership

### Person 1: Technical Architect and Integration Lead

Owns:

- Architecture
- API contracts
- Shared schemas
- Decision Service
- Integration
- Main application wiring
- Demo flow
- Merge coordination

### Person 2: Backend and Rule Engine Engineer

Owns:

- Database
- Models
- Repositories
- Policy CRUD
- Rule engine
- Operator registry
- Priority resolver
- Backend unit tests

### Person 3: AI Engineer

Owns:

- LLM provider
- Prompt templates
- Policy generation
- Ambiguity detection
- Conflict explanation
- Decision explanation
- AI test generation
- AI fallback behavior

### Person 4: Frontend Engineer

Owns:

- Admin dashboard
- AI Policy Studio
- Policy list and detail
- Decision Center
- Analytics
- Audit screens
- API client
- UI validation and error states

---

## 31. Integration Boundaries

Each module must expose stable interfaces.

### Backend engine interface

```python
evaluate_policies(
    request_data: dict,
    policies: list[dict]
) -> dict
```

### AI policy generation interface

```python
generate_policy(
    policy_text: str,
    available_fields: list[dict],
    supported_operators: list[str]
) -> dict
```

### Explanation interface

```python
generate_explanation(
    evaluation_result: dict
) -> str
```

### Conflict interface

```python
detect_conflicts(
    candidate_policy: dict,
    active_policies: list[dict]
) -> list[dict]
```

### Decision service interface

```python
evaluate_decision(
    request_data: dict
) -> dict
```

Frontend must depend only on REST APIs, never internal Python functions.

---

## 32. Integration Milestones

### Milestone 1: Skeleton

- Repository created
- Folder structure committed
- FastAPI runs
- Frontend runs
- API contract agreed
- Mock data available

### Milestone 2: Independent modules

- Policy CRUD works
- Rule engine works
- AI generator returns validated rule
- Frontend screens work with mock responses

### Milestone 3: First integration

- Frontend calls real policy APIs
- AI-generated rule can be saved
- Decision API returns deterministic result

### Milestone 4: Full workflow

- Create policy
- Approve policy
- Evaluate customer
- Explain decision
- Store audit
- Update dashboard

### Milestone 5: Demo readiness

- Seed data
- Stable test case
- Error scenario
- Ambiguity scenario
- Conflict scenario
- Final presentation

---

## 33. Demo Scenario

### Step 1: Show dashboard

Highlight:

- Active policies
- Pending policies
- Today's evaluations
- Outcome distribution
- Average confidence
- Average latency

### Step 2: Create policy

Input:

```text
Approve premium device upgrades for customers with at least
24 months tenure, no payment defaults, credit score at least 750,
and fraud risk below 0.6.
```

Show:

- Generated conditions
- AI confidence
- No ambiguity
- Validation success
- Human approval

### Step 3: Evaluate low-risk customer

Input:

```json
{
  "customer_id": "CUST-1001",
  "customer_tenure_months": 36,
  "credit_score": 790,
  "payment_defaults": 0,
  "fraud_risk_score": 0.12,
  "monthly_bill_amount": 3200,
  "requested_device_price": 85000,
  "customer_segment": "PREMIUM",
  "outstanding_balance": 0
}
```

Expected result:

```text
APPROVE
```

### Step 4: Evaluate risky customer

Input:

```json
{
  "customer_id": "CUST-1002",
  "customer_tenure_months": 42,
  "credit_score": 785,
  "payment_defaults": 0,
  "fraud_risk_score": 0.82,
  "monthly_bill_amount": 4000,
  "requested_device_price": 95000,
  "customer_segment": "PREMIUM",
  "outstanding_balance": 0
}
```

Expected result:

```text
MANUAL_REVIEW or REJECT
```

based on the seeded high-priority fraud policy.

### Step 5: Show audit

Display:

- Evaluation ID
- Rules evaluated
- Matched policies
- Winning policy
- Explanation
- Confidence
- Latency

---

## 34. Seed Policies

### Policy 1: Standard approval

```text
Decision: APPROVE
Priority: 100
Conditions:
- Tenure >= 24
- Credit score >= 750
- Defaults = 0
- Fraud risk < 0.6
```

### Policy 2: Fraud rejection

```text
Decision: REJECT
Priority: 300
Conditions:
- Fraud risk >= 0.85
```

### Policy 3: Fraud manual review

```text
Decision: MANUAL_REVIEW
Priority: 250
Conditions:
- Fraud risk >= 0.6
- Fraud risk < 0.85
```

### Policy 4: Outstanding-balance rejection

```text
Decision: REJECT
Priority: 220
Conditions:
- Outstanding balance > 10000
```

### Policy 5: Premium override approval

```text
Decision: APPROVE
Priority: 120
Conditions:
- Customer segment = PREMIUM
- Tenure >= 18
- Credit score >= 780
- Fraud risk < 0.4
```

---

## 35. Success Criteria

The POC is successful when:

1. A user can enter a policy in natural language.
2. The AI returns a valid structured policy.
3. Ambiguous language is flagged.
4. A user can approve and activate a policy.
5. A decision request is evaluated deterministically.
6. Multiple matching rules are resolved consistently.
7. A confidence score and metrics are shown.
8. A human-readable explanation is generated.
9. An audit record is stored.
10. Dashboard analytics reflect the evaluation.
11. The complete workflow can be demonstrated without manually editing code.

---

## 36. Judge and Leadership Questions

### Why is AI required?

AI removes the need for business users to understand rule syntax, detects ambiguous policy language, assists with conflict understanding, and generates readable explanations.

### Why does AI not make the final decision?

Final business decisions must be deterministic, repeatable, auditable, and testable. The LLM is used only where language interpretation adds value.

### What happens when the LLM fails?

The rule engine remains available. Manual JSON policy creation and deterministic explanations provide fallback behavior.

### How is hallucination controlled?

The LLM receives a strict field and operator allow-list. Its output must pass validation and human approval before activation.

### How are conflicts resolved?

Potential conflicts are flagged during policy creation. At evaluation time, deterministic priority and tie-breaker rules determine the outcome.

### How is the solution extensible?

New fields, operators, domains, and policies can be added without modifying the core decision workflow.

### What is the main business value?

Faster policy rollout, lower engineering dependency, improved transparency, and better auditability.

---

## 37. Future Enhancements

- Role-based approval workflows
- Policy simulation
- Bulk customer evaluation
- Version comparison
- Domain configuration UI
- Rule recommendation engine
- Policy impact analysis
- Event-driven evaluation
- Multi-tenant workspaces
- External feature-store integration
- Real-time fraud signals
- LLM evaluation framework
- Retrieval of policy documents
- Policy templates
- Natural-language policy editing
- Approval comments
- Explainability reports
- Production observability
- Cloud deployment

---

## 38. Final Architecture Statement

DecisionFlow AI is not an LLM making uncontrolled business decisions.

It is a governed decision platform in which:

```text
AI understands policy language.
Validation protects the system.
Humans approve configuration.
A deterministic engine makes decisions.
Explainability makes outcomes understandable.
Audit logs make the process traceable.
Analytics make the system measurable.
```

This separation is the foundation of the POC and should remain consistent across frontend, backend, AI, integration, documentation, and presentation.
