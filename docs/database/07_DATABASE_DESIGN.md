# DecisionFlow AI
## MySQL Database Design and Persistence Specification

**Document ID:** DFA-DB-007  
**Version:** 1.0  
**Status:** Hackathon POC Baseline — MySQL Edition  
**Primary Owner:** Backend and Rule Engine Engineer  
**Reviewers:** Technical Architect and Integration Lead  
**Database:** MySQL 8.0+  
**ORM:** SQLAlchemy 2.x  
**Driver:** PyMySQL  
**Migration Tool:** Alembic

---

# 1. Purpose

This document defines the complete database design for DecisionFlow AI.

It is the source of truth for:

- MySQL schema
- Table relationships
- Column definitions
- Primary and foreign keys
- Indexes
- Constraints
- JSON column structures
- Policy versioning
- Evaluation persistence
- Rule-level execution traces
- Audit logging
- Transaction boundaries
- Alembic migrations
- Seed data
- Test-database strategy
- Query expectations
- Data retention
- Backup and recovery assumptions
- Integration requirements

The database must support the complete product lifecycle:

```text
Policy generation
    ↓
Draft storage
    ↓
Human activation
    ↓
Version snapshot
    ↓
Customer evaluation
    ↓
Rule-level execution trace
    ↓
Final decision
    ↓
Explanation
    ↓
Audit record
    ↓
Analytics
```

The system will use MySQL from the beginning.

There must be no SQLite or in-memory fallback in the integrated application.

---

# 2. Database Responsibilities

MySQL is responsible for storing:

- Current policy state
- Immutable policy versions
- Decision requests
- Decision outcomes
- Rule-evaluation results
- Condition-level traces
- AI metadata
- Explanation metadata
- Audit events
- Analytics source data
- Correlation identifiers
- Actor information
- Performance metrics
- Demo seed data

MySQL is not responsible for:

- Executing rule logic
- Calling the LLM
- Rendering UI
- Generating explanations
- Validating natural-language intent
- Replacing application-level policy validation

The database stores governed results and state. The application owns business execution.

---

# 3. Database Technology Baseline

## Required stack

```text
MySQL 8.0+
SQLAlchemy 2.x
PyMySQL
Alembic
```

## Required character set

```text
utf8mb4
```

## Required collation

```text
utf8mb4_unicode_ci
```

## Recommended server time zone

```text
UTC
```

## Recommended database name

```text
decisionflow
```

## Recommended test database name

```text
decisionflow_test
```

---

# 4. Connection Configuration

## Local backend

```text
DATABASE_URL=mysql+pymysql://decisionflow:decisionflow@localhost:3306/decisionflow
```

## Docker backend

```text
DATABASE_URL=mysql+pymysql://decisionflow:decisionflow@mysql:3306/decisionflow
```

## Test database

```text
TEST_DATABASE_URL=mysql+pymysql://decisionflow:decisionflow@localhost:3306/decisionflow_test
```

## SQLAlchemy engine requirements

```python
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=5,
    max_overflow=10,
)
```

For a hackathon POC, smaller pool settings are acceptable.

---

# 5. Database Naming Conventions

## Tables

Use plural snake_case.

```text
policies
policy_versions
evaluations
evaluation_rule_results
audit_logs
```

## Columns

Use snake_case.

Correct:

```text
winning_policy_id
decision_confidence
created_at
```

Incorrect:

```text
winningPolicyId
DecisionConfidence
CreatedAt
```

## Primary keys

Use string identifiers.

```text
pol_<uuid>
ver_<uuid>
eval_<uuid>
rr_<uuid>
aud_<uuid>
```

## Foreign keys

Use `<referenced_entity>_id`.

Examples:

```text
policy_id
evaluation_id
winning_policy_id
```

## Index names

Recommended pattern:

```text
ix_<table>_<column>
ix_<table>_<column1>_<column2>
uq_<table>_<column>
fk_<table>_<column>
```

---

# 6. Entity Overview

The POC uses five core tables.

```text
policies
policy_versions
evaluations
evaluation_rule_results
audit_logs
```

Optional future tables are documented later.

---

# 7. Entity Relationship Diagram

```text
┌─────────────────────────────┐
│          policies           │
├─────────────────────────────┤
│ id PK                       │
│ name UQ                     │
│ status                      │
│ priority                    │
│ decision                    │
│ current_version             │
│ conditions_json             │
│ ai_metadata_json            │
│ ...                         │
└──────────────┬──────────────┘
               │ 1
               │
               │ N
┌──────────────▼──────────────┐
│      policy_versions        │
├─────────────────────────────┤
│ id PK                       │
│ policy_id FK                │
│ version                     │
│ policy snapshot fields      │
│ conditions_json             │
│ ai_metadata_json            │
│ ...                         │
└─────────────────────────────┘


┌─────────────────────────────┐
│         evaluations         │
├─────────────────────────────┤
│ id PK                       │
│ request_id                  │
│ customer_id                 │
│ decision                    │
│ decision_confidence         │
│ winning_policy_id FK        │
│ request_json                │
│ resolution_json             │
│ explanation_json            │
│ metrics_json                │
│ warnings_json               │
│ ...                         │
└──────────────┬──────────────┘
               │ 1
               │
               │ N
┌──────────────▼──────────────┐
│ evaluation_rule_results     │
├─────────────────────────────┤
│ id PK                       │
│ evaluation_id FK            │
│ policy_id                   │
│ policy_version              │
│ matched                     │
│ result_status               │
│ condition_results_json      │
│ missing_fields_json         │
│ ...                         │
└─────────────────────────────┘


┌─────────────────────────────┐
│         audit_logs          │
├─────────────────────────────┤
│ id PK                       │
│ action                      │
│ entity_type                 │
│ entity_id                   │
│ entity_version              │
│ performed_by                │
│ request_snapshot_json       │
│ result_snapshot_json        │
│ metadata_json               │
│ correlation_id              │
│ created_at                  │
└─────────────────────────────┘
```

---

# 8. Table: policies

## Purpose

Stores the current working state of every policy.

A row may represent:

- Draft policy
- Pending policy
- Active policy
- Disabled policy
- Archived policy

This table contains the latest mutable policy state.

Historical activated versions are preserved separately in `policy_versions`.

---

# 9. policies Column Specification

| Column | MySQL Type | Nullable | Default | Description |
|---|---|---:|---|---|
| `id` | VARCHAR(40) | No | — | Primary policy ID |
| `name` | VARCHAR(120) | No | — | Unique policy name |
| `description` | TEXT | Yes | NULL | Business description |
| `domain` | VARCHAR(50) | No | `telecom` | Policy domain |
| `status` | VARCHAR(30) | No | `DRAFT` | Current policy status |
| `priority` | INT | No | 100 | Runtime priority |
| `decision` | VARCHAR(30) | No | — | APPROVE, REJECT, MANUAL_REVIEW |
| `conditions_json` | JSON | No | — | Rule condition tree |
| `reason` | TEXT | Yes | NULL | Business reason |
| `source` | VARCHAR(30) | No | `MANUAL` | AI_GENERATED, MANUAL, IMPORTED, SEEDED |
| `current_version` | INT | No | 1 | Current version number |
| `ai_metadata_json` | JSON | Yes | NULL | AI generation metadata |
| `validation_metadata_json` | JSON | Yes | NULL | Validation results |
| `conflict_metadata_json` | JSON | Yes | NULL | Conflict results |
| `created_by` | VARCHAR(100) | Yes | NULL | Creator |
| `approved_by` | VARCHAR(100) | Yes | NULL | Approver |
| `created_at` | DATETIME(6) | No | current UTC | Creation time |
| `updated_at` | DATETIME(6) | No | current UTC | Last update |
| `activated_at` | DATETIME(6) | Yes | NULL | Activation time |
| `disabled_at` | DATETIME(6) | Yes | NULL | Disable time |
| `archived_at` | DATETIME(6) | Yes | NULL | Archive time |

---

# 10. policies Constraints

## Primary key

```sql
PRIMARY KEY (id)
```

## Unique name

```sql
UNIQUE KEY uq_policies_name (name)
```

For future multi-tenancy, uniqueness may become:

```text
(tenant_id, name)
```

## Priority check

Application validation is required.

A MySQL check constraint may also be added:

```sql
CHECK (priority BETWEEN 1 AND 1000)
```

## Version check

```sql
CHECK (current_version >= 1)
```

## Allowed status

Application-enforced values:

```text
DRAFT
PENDING_APPROVAL
ACTIVE
DISABLED
ARCHIVED
```

## Allowed decision

Application-enforced values:

```text
APPROVE
REJECT
MANUAL_REVIEW
```

## Allowed source

Application-enforced values:

```text
AI_GENERATED
MANUAL
IMPORTED
SEEDED
```

---

# 11. policies Indexes

Required:

```sql
CREATE INDEX ix_policies_domain
ON policies(domain);

CREATE INDEX ix_policies_status
ON policies(status);

CREATE INDEX ix_policies_priority
ON policies(priority);

CREATE INDEX ix_policies_decision
ON policies(decision);

CREATE INDEX ix_policies_updated_at
ON policies(updated_at);

CREATE INDEX ix_policies_active_lookup
ON policies(domain, status, priority);
```

The main runtime query is:

```text
All active policies in one domain ordered by priority.
```

Recommended query:

```sql
SELECT *
FROM policies
WHERE domain = 'telecom'
  AND status = 'ACTIVE'
ORDER BY priority DESC, current_version DESC, id ASC;
```

---

# 12. conditions_json Structure

Example:

```json
{
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
}
```

Nested example:

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

The application validates the condition tree before persistence.

---

# 13. ai_metadata_json Structure

Example:

```json
{
  "generated": true,
  "ai_confidence": 94,
  "provider": "openai",
  "model": "configured-model",
  "prompt_version": "1.0",
  "warnings": [],
  "ambiguities": [],
  "assumptions": [
    "No payment defaults was mapped to payment_defaults equals 0."
  ],
  "processing_time_ms": 1450,
  "fallback_used": false
}
```

Do not store API keys or secrets.

---

# 14. validation_metadata_json Structure

Example:

```json
{
  "status": "PASSED",
  "validated_at": "2026-07-24T08:48:00.000Z",
  "errors": [],
  "warnings": [],
  "field_count": 4,
  "condition_count": 4
}
```

---

# 15. conflict_metadata_json Structure

Example:

```json
{
  "has_conflicts": false,
  "blocking_conflict_count": 0,
  "warning_count": 0,
  "conflicts": []
}
```

Conflict metadata is informational for the current policy state.

Historical conflict state should also be preserved in policy versions where needed.

---

# 16. Table: policy_versions

## Purpose

Stores immutable snapshots of policy versions.

A policy version should be created when:

- A draft is activated
- An active policy is meaningfully changed
- A new version replaces a previous active version
- A policy is reactivated with changed configuration

The version table protects auditability.

---

# 17. policy_versions Column Specification

| Column | MySQL Type | Nullable | Description |
|---|---|---:|---|
| `id` | VARCHAR(40) | No | Version record ID |
| `policy_id` | VARCHAR(40) | No | Parent policy |
| `version` | INT | No | Version number |
| `name` | VARCHAR(120) | No | Snapshot name |
| `description` | TEXT | Yes | Snapshot description |
| `domain` | VARCHAR(50) | No | Snapshot domain |
| `status_snapshot` | VARCHAR(30) | No | Status at snapshot |
| `priority` | INT | No | Snapshot priority |
| `decision` | VARCHAR(30) | No | Snapshot decision |
| `conditions_json` | JSON | No | Snapshot conditions |
| `reason` | TEXT | Yes | Snapshot reason |
| `source` | VARCHAR(30) | No | Snapshot source |
| `ai_metadata_json` | JSON | Yes | Snapshot AI metadata |
| `validation_metadata_json` | JSON | Yes | Snapshot validation |
| `conflict_metadata_json` | JSON | Yes | Snapshot conflicts |
| `created_by` | VARCHAR(100) | Yes | Original creator |
| `approved_by` | VARCHAR(100) | Yes | Version approver |
| `approval_comment` | TEXT | Yes | Activation comment |
| `created_at` | DATETIME(6) | No | Snapshot time |

---

# 18. policy_versions Constraints

## Primary key

```sql
PRIMARY KEY (id)
```

## Foreign key

```sql
CONSTRAINT fk_policy_versions_policy_id
FOREIGN KEY (policy_id)
REFERENCES policies(id)
ON DELETE RESTRICT
```

Use `RESTRICT` to protect historical versions.

## Unique version

```sql
UNIQUE KEY uq_policy_versions_policy_version
(policy_id, version)
```

## Immutability

The application must never update a policy-version row after creation.

No update method should exist in the repository.

---

# 19. policy_versions Indexes

```sql
CREATE INDEX ix_policy_versions_policy_id
ON policy_versions(policy_id);

CREATE INDEX ix_policy_versions_created_at
ON policy_versions(created_at);

CREATE INDEX ix_policy_versions_policy_version
ON policy_versions(policy_id, version);
```

---

# 20. Versioning Rules

## Initial draft

```text
current_version = 1
```

## First activation

Create:

```text
policy_versions.version = 1
```

## Meaningful update

Increment current version:

```text
current_version = 2
```

## Activation of new version

Create:

```text
policy_versions.version = 2
```

## Historical evaluation

Every evaluation stores:

```text
winning_policy_id
winning_policy_version
```

Each rule result stores:

```text
policy_id
policy_version
```

This allows reconstruction of the exact policy state used.

---

# 21. Table: evaluations

## Purpose

Stores every customer decision evaluation.

An evaluation row records:

- Input request snapshot
- Final outcome
- Winning policy
- Resolution
- Confidence
- Explanation
- Metrics
- Warnings
- Correlation ID
- Actor
- Timestamp

---

# 22. evaluations Column Specification

| Column | MySQL Type | Nullable | Description |
|---|---|---:|---|
| `id` | VARCHAR(40) | No | Evaluation ID |
| `request_id` | VARCHAR(100) | Yes | Client request ID |
| `domain` | VARCHAR(50) | No | Domain |
| `customer_id` | VARCHAR(100) | Yes | Customer reference |
| `request_json` | JSON | No | Full decision request |
| `decision` | VARCHAR(30) | No | Final outcome |
| `decision_confidence` | INT | No | Deterministic score |
| `winning_policy_id` | VARCHAR(40) | Yes | Winning policy |
| `winning_policy_version` | INT | Yes | Winning version |
| `resolution_strategy` | VARCHAR(50) | No | HIGHEST_PRIORITY, DEFAULT_FALLBACK |
| `resolution_json` | JSON | No | Full resolution details |
| `explanation_json` | JSON | Yes | Explanation details |
| `metrics_json` | JSON | No | Performance metrics |
| `warnings_json` | JSON | Yes | Evaluation warnings |
| `correlation_id` | VARCHAR(100) | No | Trace ID |
| `created_by` | VARCHAR(100) | Yes | Actor |
| `evaluated_at` | DATETIME(6) | No | Evaluation time |

---

# 23. evaluations Constraints

## Primary key

```sql
PRIMARY KEY (id)
```

## Optional foreign key to winning policy

```sql
CONSTRAINT fk_evaluations_winning_policy_id
FOREIGN KEY (winning_policy_id)
REFERENCES policies(id)
ON DELETE SET NULL
```

Historical rule-result snapshots still preserve policy details even if current policy status changes.

## Confidence range

```sql
CHECK (decision_confidence BETWEEN 0 AND 100)
```

## Allowed decisions

Application-enforced:

```text
APPROVE
REJECT
MANUAL_REVIEW
NO_MATCH
```

---

# 24. evaluations Indexes

Required:

```sql
CREATE INDEX ix_evaluations_request_id
ON evaluations(request_id);

CREATE INDEX ix_evaluations_customer_id
ON evaluations(customer_id);

CREATE INDEX ix_evaluations_decision
ON evaluations(decision);

CREATE INDEX ix_evaluations_winning_policy_id
ON evaluations(winning_policy_id);

CREATE INDEX ix_evaluations_correlation_id
ON evaluations(correlation_id);

CREATE INDEX ix_evaluations_evaluated_at
ON evaluations(evaluated_at);

CREATE INDEX ix_evaluations_domain_date
ON evaluations(domain, evaluated_at);

CREATE INDEX ix_evaluations_decision_date
ON evaluations(decision, evaluated_at);
```

---

# 25. request_json Structure

Example:

```json
{
  "request_id": "req_1001",
  "domain": "telecom",
  "customer": {
    "customer_id": "CUST-1001",
    "customer_tenure_months": 36,
    "credit_score": 790,
    "payment_defaults": 0,
    "fraud_risk_score": 0.12,
    "monthly_bill_amount": 3200,
    "requested_device_price": 85000,
    "customer_segment": "PREMIUM",
    "current_plan": "Magenta Max",
    "outstanding_balance": 0,
    "is_existing_customer": true,
    "previous_upgrade_months_ago": 30
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

---

# 26. resolution_json Structure

Example:

```json
{
  "strategy": "HIGHEST_PRIORITY",
  "reason": "Fraud rejection priority 300 exceeded approval priority 100.",
  "tie_breaker_used": false,
  "competing_policy_ids": [
    "pol_fraud_001",
    "pol_upgrade_001"
  ]
}
```

No-match example:

```json
{
  "strategy": "DEFAULT_FALLBACK",
  "reason": "No active policy fully matched the request.",
  "tie_breaker_used": false,
  "competing_policy_ids": []
}
```

---

# 27. explanation_json Structure

AI explanation:

```json
{
  "summary": "The request was rejected because the fraud-risk policy had the highest priority.",
  "key_factors": [
    "Fraud risk score 0.91 was greater than or equal to 0.85.",
    "Fraud rejection priority 300 exceeded approval priority 100."
  ],
  "generated_by": "AI",
  "fallback_used": false,
  "provider": "configured-provider",
  "model": "configured-model",
  "prompt_version": "1.0",
  "processing_time_ms": 580
}
```

Fallback:

```json
{
  "summary": "The request was rejected because policy Fraud rejection matched and had the highest priority.",
  "key_factors": [],
  "generated_by": "DETERMINISTIC_FALLBACK",
  "fallback_used": true
}
```

---

# 28. metrics_json Structure

Example:

```json
{
  "policies_loaded": 5,
  "policies_evaluated": 5,
  "policies_matched": 2,
  "policies_skipped": 0,
  "condition_count": 9,
  "conflicts_detected": 1,
  "engine_latency_ms": 20,
  "explanation_latency_ms": 580,
  "total_latency_ms": 615
}
```

---

# 29. warnings_json Structure

Example:

```json
[
  {
    "code": "AI_EXPLANATION_UNAVAILABLE",
    "message": "A deterministic explanation was provided because the AI explanation service was unavailable."
  }
]
```

---

# 30. Table: evaluation_rule_results

## Purpose

Stores the result of evaluating each policy during a customer decision.

This table allows the system to explain:

- Which policies matched
- Which policies did not match
- Which policies were skipped
- Which conditions passed
- Which conditions failed
- Which fields were missing
- Which version was evaluated

---

# 31. evaluation_rule_results Column Specification

| Column | MySQL Type | Nullable | Description |
|---|---|---:|---|
| `id` | VARCHAR(40) | No | Rule-result ID |
| `evaluation_id` | VARCHAR(40) | No | Parent evaluation |
| `policy_id` | VARCHAR(40) | No | Evaluated policy |
| `policy_version` | INT | No | Evaluated version |
| `policy_name` | VARCHAR(120) | No | Snapshot name |
| `priority` | INT | No | Snapshot priority |
| `decision` | VARCHAR(30) | No | Policy outcome |
| `result_status` | VARCHAR(40) | No | MATCHED, UNMATCHED, etc. |
| `matched` | BOOLEAN | No | Policy match flag |
| `condition_results_json` | JSON | No | Condition trace |
| `missing_fields_json` | JSON | Yes | Missing fields |
| `reason` | TEXT | Yes | Evaluation reason |
| `created_at` | DATETIME(6) | No | Persistence time |

---

# 32. evaluation_rule_results Constraints

## Primary key

```sql
PRIMARY KEY (id)
```

## Foreign key

```sql
CONSTRAINT fk_rule_results_evaluation_id
FOREIGN KEY (evaluation_id)
REFERENCES evaluations(id)
ON DELETE CASCADE
```

Deleting an evaluation should delete its rule traces.

For the POC, evaluation deletion is not exposed through APIs.

## Policy reference

A strict foreign key to `policies` is optional.

Recommended POC choice:

```text
Do not require a foreign key from evaluation_rule_results.policy_id to policies.
```

Reason:

- The row is a historical snapshot.
- Archived or removed current policies should not invalidate history.
- Policy name, priority, version, decision, and condition results are already stored.

The application still stores the policy ID.

---

# 33. evaluation_rule_results Indexes

```sql
CREATE INDEX ix_rule_results_evaluation_id
ON evaluation_rule_results(evaluation_id);

CREATE INDEX ix_rule_results_policy_id
ON evaluation_rule_results(policy_id);

CREATE INDEX ix_rule_results_result_status
ON evaluation_rule_results(result_status);

CREATE INDEX ix_rule_results_matched
ON evaluation_rule_results(matched);

CREATE INDEX ix_rule_results_policy_match
ON evaluation_rule_results(policy_id, matched);
```

---

# 34. condition_results_json Structure

Example:

```json
[
  {
    "field": "customer_tenure_months",
    "operator": "greater_than_or_equal",
    "expected": 24,
    "actual": 36,
    "matched": true,
    "status": "MATCHED",
    "reason": null
  },
  {
    "field": "fraud_risk_score",
    "operator": "less_than",
    "expected": 0.6,
    "actual": 0.91,
    "matched": false,
    "status": "UNMATCHED",
    "reason": "Actual value was not less than expected threshold."
  }
]
```

Missing field:

```json
[
  {
    "field": "credit_score",
    "operator": "greater_than_or_equal",
    "expected": 750,
    "actual": null,
    "matched": false,
    "status": "MISSING_FIELD",
    "reason": "Field was not present in the decision request."
  }
]
```

---

# 35. missing_fields_json Structure

Example:

```json
[
  "credit_score",
  "fraud_risk_score"
]
```

Use an empty array rather than null when possible.

---

# 36. result_status Values

```text
MATCHED
UNMATCHED
SKIPPED_MISSING_FIELD
SKIPPED_INVALID_DATA
ERROR
```

The application should never silently convert `ERROR` to `UNMATCHED`.

---

# 37. Table: audit_logs

## Purpose

Stores append-only audit events for important platform actions.

The audit log supports:

- Governance
- Troubleshooting
- Demo explainability
- User accountability
- Correlation tracing
- Policy change history
- Decision traceability

---

# 38. audit_logs Column Specification

| Column | MySQL Type | Nullable | Description |
|---|---|---:|---|
| `id` | VARCHAR(40) | No | Audit ID |
| `action` | VARCHAR(50) | No | Event action |
| `entity_type` | VARCHAR(50) | No | POLICY, EVALUATION, AI_OPERATION |
| `entity_id` | VARCHAR(40) | No | Referenced entity |
| `entity_version` | INT | Yes | Optional version |
| `performed_by` | VARCHAR(100) | Yes | Actor |
| `summary` | TEXT | No | Human-readable summary |
| `request_snapshot_json` | JSON | Yes | Request snapshot |
| `result_snapshot_json` | JSON | Yes | Result snapshot |
| `metadata_json` | JSON | Yes | Extra metadata |
| `correlation_id` | VARCHAR(100) | No | Trace ID |
| `created_at` | DATETIME(6) | No | Event time |

---

# 39. Audit Actions

Supported baseline values:

```text
POLICY_CREATED
POLICY_UPDATED
POLICY_ACTIVATED
POLICY_DISABLED
POLICY_ARCHIVED
POLICY_GENERATED_BY_AI
DECISION_EVALUATED
AI_EXPLANATION_GENERATED
AI_EXPLANATION_FAILED
```

The POC must implement at least:

```text
POLICY_CREATED
POLICY_ACTIVATED
POLICY_DISABLED
DECISION_EVALUATED
AI_EXPLANATION_FAILED
```

---

# 40. Audit Entity Types

```text
POLICY
POLICY_VERSION
EVALUATION
AI_OPERATION
SYSTEM
```

---

# 41. audit_logs Indexes

```sql
CREATE INDEX ix_audit_logs_action
ON audit_logs(action);

CREATE INDEX ix_audit_logs_entity_type
ON audit_logs(entity_type);

CREATE INDEX ix_audit_logs_entity_id
ON audit_logs(entity_id);

CREATE INDEX ix_audit_logs_performed_by
ON audit_logs(performed_by);

CREATE INDEX ix_audit_logs_correlation_id
ON audit_logs(correlation_id);

CREATE INDEX ix_audit_logs_created_at
ON audit_logs(created_at);

CREATE INDEX ix_audit_logs_entity_lookup
ON audit_logs(entity_type, entity_id, created_at);
```

---

# 42. Audit Snapshot Examples

## Policy activation request snapshot

```json
{
  "policy_id": "pol_01J123ABC",
  "approval_comment": "Reviewed for demo environment."
}
```

## Policy activation result snapshot

```json
{
  "status": "ACTIVE",
  "version": 1,
  "approved_by": "demo_user",
  "activated_at": "2026-07-24T09:20:00.000Z"
}
```

## Decision evaluation request snapshot

```json
{
  "customer_id": "CUST-1001",
  "requested_action": "DEVICE_UPGRADE"
}
```

## Decision evaluation result snapshot

```json
{
  "evaluation_id": "eval_01J123ABC",
  "decision": "APPROVE",
  "decision_confidence": 96,
  "winning_policy_id": "pol_01J123DEF",
  "winning_policy_version": 1
}
```

---

# 43. Audit Data Minimization

Audit logs should not store unnecessary sensitive data.

Preferred:

- Customer ID
- Decision
- Winning rule
- Confidence
- Version
- Correlation ID

Avoid:

- Full secrets
- Database credentials
- API keys
- Provider authentication headers
- Full personal profile unless required

The POC may store request snapshots, but the design should remain deliberate.

---

# 44. SQLAlchemy Model Guidance

Use SQLAlchemy 2.x declarative models.

Example pattern:

```python
from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[str] = mapped_column(
        String(40),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    domain: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    decision: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    conditions_json: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
    )
```

Use UTC-naive database timestamps consistently if the application guarantees UTC.

---

# 45. Timestamp Strategy

Recommended:

- Application generates UTC timestamps.
- Database stores `DATETIME(6)`.
- API returns ISO 8601 UTC strings with `Z`.
- All developers treat database values as UTC.

Example application helper:

```python
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)
```

Do not mix local time and UTC.

---

# 46. Boolean Strategy

Use MySQL boolean-compatible columns.

SQLAlchemy:

```python
mapped_column(Boolean, nullable=False)
```

MySQL stores as `TINYINT(1)` internally.

API remains:

```json
true
false
```

---

# 47. JSON Column Strategy

Use MySQL native JSON columns for:

- Rule condition trees
- AI metadata
- Validation metadata
- Conflict metadata
- Decision requests
- Resolution
- Explanation
- Metrics
- Warnings
- Condition traces
- Audit snapshots

Why JSON is appropriate:

- Flexible nested structure
- POC speed
- Preserves exact evidence
- Avoids over-normalizing condition trees
- Supports later JSON queries if needed

Do not store everything as JSON.

Use typed relational columns for frequently filtered values such as:

```text
status
decision
priority
customer_id
evaluated_at
correlation_id
```

---

# 48. JSON Validation Strategy

MySQL ensures valid JSON syntax.

The application ensures semantic validity through Pydantic.

Required rule:

> JSON columns must only receive data already validated by application schemas.

Do not rely on database JSON validity as business validation.

---

# 49. Transaction Design

## Policy creation transaction

```text
Insert policy
Insert audit log
Commit
```

If audit insertion fails:

Recommended POC behavior:

```text
Rollback policy creation
```

This provides strong governance.

## Policy activation transaction

```text
Lock or load policy
Validate state
Create version snapshot
Update policy status
Insert audit log
Commit
```

All steps must succeed together.

## Policy disable transaction

```text
Update status
Set disabled timestamp
Insert audit log
Commit
```

## Decision evaluation transaction

Recommended:

```text
Insert evaluation
Insert all rule results
Insert decision audit
Commit
```

AI explanation is generated before persistence.

If explanation falls back, the fallback is persisted.

---

# 50. Policy Activation Atomicity

Policy activation must be atomic.

Incorrect:

```text
Update policy to ACTIVE
Commit
Create version
Commit
Create audit
Commit
```

Correct:

```text
BEGIN
Create version
Update policy
Create audit
COMMIT
```

If any step fails:

```text
ROLLBACK
```

---

# 51. Evaluation Persistence Atomicity

Recommended:

```text
BEGIN
Insert evaluation
Bulk insert evaluation_rule_results
Insert audit
COMMIT
```

This guarantees that an evaluation never exists without its execution trace.

---

# 52. Isolation Level

MySQL default:

```text
REPEATABLE READ
```

This is acceptable for the POC.

For simple request transactions, no custom isolation is required.

Potential activation race conditions can be handled with:

- Application state checks
- Version number checks
- Row locking if needed

Optional:

```sql
SELECT ...
FOR UPDATE
```

for policy activation.

---

# 53. Optimistic Concurrency

For the POC, current version can support basic optimistic concurrency.

Update request may include:

```text
expected_version
```

If current version differs:

```text
409 POLICY_VERSION_CONFLICT
```

This is optional but recommended if time permits.

---

# 54. Soft Delete Strategy

## Policies

Do not physically delete active or historical policies.

Use:

```text
ARCHIVED
```

and set:

```text
archived_at
```

Draft policies may be hard-deleted if desired.

Recommended simplified behavior:

- Draft: hard delete allowed
- Active: archive
- Disabled: archive
- Archived: retained

## Evaluations

No delete API in POC.

## Audit logs

Append-only.

No delete API in POC.

---

# 55. Foreign Key Strategy

Use foreign keys where they improve consistency.

Recommended:

```text
policy_versions.policy_id → policies.id
evaluations.winning_policy_id → policies.id, nullable
evaluation_rule_results.evaluation_id → evaluations.id
```

Do not use strict policy foreign keys for every historical trace field if it risks losing immutable history.

---

# 56. Migration Strategy

Use Alembic for every persistent schema change.

Required migration sequence:

```text
001_create_policies
002_create_policy_versions
003_create_evaluations
004_create_evaluation_rule_results
005_create_audit_logs
006_add_indexes
```

For a short hackathon, these may be combined into fewer migrations, but the final migration history must be understandable.

---

# 57. Alembic Configuration

## alembic.ini

Use environment-based URL rather than storing credentials.

## env.py

Import:

```python
from app.db.base import Base
from app.models import policy
from app.models import policy_version
from app.models import evaluation
from app.models import evaluation_rule_result
from app.models import audit
```

Set:

```python
target_metadata = Base.metadata
```

Load URL from settings.

---

# 58. Migration Commands

Create revision:

```bash
alembic revision --autogenerate -m "create core tables"
```

Apply:

```bash
alembic upgrade head
```

Rollback one:

```bash
alembic downgrade -1
```

Show current:

```bash
alembic current
```

Show history:

```bash
alembic history
```

---

# 59. Migration Rules

- Never edit an applied migration in shared environments.
- Create a new migration for schema changes.
- Test migrations against MySQL.
- Do not generate SQLite-specific SQL.
- Review generated constraints and indexes.
- Confirm downgrade behavior if time permits.
- Keep migration names descriptive.

---

# 60. Initial MySQL DDL

The following DDL is a reference baseline.

```sql
CREATE TABLE policies (
    id VARCHAR(40) NOT NULL,
    name VARCHAR(120) NOT NULL,
    description TEXT NULL,
    domain VARCHAR(50) NOT NULL DEFAULT 'telecom',
    status VARCHAR(30) NOT NULL DEFAULT 'DRAFT',
    priority INT NOT NULL DEFAULT 100,
    decision VARCHAR(30) NOT NULL,
    conditions_json JSON NOT NULL,
    reason TEXT NULL,
    source VARCHAR(30) NOT NULL DEFAULT 'MANUAL',
    current_version INT NOT NULL DEFAULT 1,
    ai_metadata_json JSON NULL,
    validation_metadata_json JSON NULL,
    conflict_metadata_json JSON NULL,
    created_by VARCHAR(100) NULL,
    approved_by VARCHAR(100) NULL,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    activated_at DATETIME(6) NULL,
    disabled_at DATETIME(6) NULL,
    archived_at DATETIME(6) NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_policies_name (name),
    CHECK (priority BETWEEN 1 AND 1000),
    CHECK (current_version >= 1),
    INDEX ix_policies_domain (domain),
    INDEX ix_policies_status (status),
    INDEX ix_policies_priority (priority),
    INDEX ix_policies_decision (decision),
    INDEX ix_policies_updated_at (updated_at),
    INDEX ix_policies_active_lookup (domain, status, priority)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;
```

---

# 61. policy_versions DDL

```sql
CREATE TABLE policy_versions (
    id VARCHAR(40) NOT NULL,
    policy_id VARCHAR(40) NOT NULL,
    version INT NOT NULL,
    name VARCHAR(120) NOT NULL,
    description TEXT NULL,
    domain VARCHAR(50) NOT NULL,
    status_snapshot VARCHAR(30) NOT NULL,
    priority INT NOT NULL,
    decision VARCHAR(30) NOT NULL,
    conditions_json JSON NOT NULL,
    reason TEXT NULL,
    source VARCHAR(30) NOT NULL,
    ai_metadata_json JSON NULL,
    validation_metadata_json JSON NULL,
    conflict_metadata_json JSON NULL,
    created_by VARCHAR(100) NULL,
    approved_by VARCHAR(100) NULL,
    approval_comment TEXT NULL,
    created_at DATETIME(6) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_policy_versions_policy_version (
        policy_id,
        version
    ),
    INDEX ix_policy_versions_policy_id (policy_id),
    INDEX ix_policy_versions_created_at (created_at),
    CONSTRAINT fk_policy_versions_policy_id
        FOREIGN KEY (policy_id)
        REFERENCES policies(id)
        ON DELETE RESTRICT
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;
```

---

# 62. evaluations DDL

```sql
CREATE TABLE evaluations (
    id VARCHAR(40) NOT NULL,
    request_id VARCHAR(100) NULL,
    domain VARCHAR(50) NOT NULL,
    customer_id VARCHAR(100) NULL,
    request_json JSON NOT NULL,
    decision VARCHAR(30) NOT NULL,
    decision_confidence INT NOT NULL,
    winning_policy_id VARCHAR(40) NULL,
    winning_policy_version INT NULL,
    resolution_strategy VARCHAR(50) NOT NULL,
    resolution_json JSON NOT NULL,
    explanation_json JSON NULL,
    metrics_json JSON NOT NULL,
    warnings_json JSON NULL,
    correlation_id VARCHAR(100) NOT NULL,
    created_by VARCHAR(100) NULL,
    evaluated_at DATETIME(6) NOT NULL,
    PRIMARY KEY (id),
    CHECK (decision_confidence BETWEEN 0 AND 100),
    INDEX ix_evaluations_request_id (request_id),
    INDEX ix_evaluations_customer_id (customer_id),
    INDEX ix_evaluations_decision (decision),
    INDEX ix_evaluations_winning_policy_id (winning_policy_id),
    INDEX ix_evaluations_correlation_id (correlation_id),
    INDEX ix_evaluations_evaluated_at (evaluated_at),
    INDEX ix_evaluations_domain_date (domain, evaluated_at),
    INDEX ix_evaluations_decision_date (decision, evaluated_at),
    CONSTRAINT fk_evaluations_winning_policy_id
        FOREIGN KEY (winning_policy_id)
        REFERENCES policies(id)
        ON DELETE SET NULL
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;
```

---

# 63. evaluation_rule_results DDL

```sql
CREATE TABLE evaluation_rule_results (
    id VARCHAR(40) NOT NULL,
    evaluation_id VARCHAR(40) NOT NULL,
    policy_id VARCHAR(40) NOT NULL,
    policy_version INT NOT NULL,
    policy_name VARCHAR(120) NOT NULL,
    priority INT NOT NULL,
    decision VARCHAR(30) NOT NULL,
    result_status VARCHAR(40) NOT NULL,
    matched BOOLEAN NOT NULL,
    condition_results_json JSON NOT NULL,
    missing_fields_json JSON NULL,
    reason TEXT NULL,
    created_at DATETIME(6) NOT NULL,
    PRIMARY KEY (id),
    INDEX ix_rule_results_evaluation_id (evaluation_id),
    INDEX ix_rule_results_policy_id (policy_id),
    INDEX ix_rule_results_result_status (result_status),
    INDEX ix_rule_results_matched (matched),
    INDEX ix_rule_results_policy_match (policy_id, matched),
    CONSTRAINT fk_rule_results_evaluation_id
        FOREIGN KEY (evaluation_id)
        REFERENCES evaluations(id)
        ON DELETE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;
```

---

# 64. audit_logs DDL

```sql
CREATE TABLE audit_logs (
    id VARCHAR(40) NOT NULL,
    action VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(40) NOT NULL,
    entity_version INT NULL,
    performed_by VARCHAR(100) NULL,
    summary TEXT NOT NULL,
    request_snapshot_json JSON NULL,
    result_snapshot_json JSON NULL,
    metadata_json JSON NULL,
    correlation_id VARCHAR(100) NOT NULL,
    created_at DATETIME(6) NOT NULL,
    PRIMARY KEY (id),
    INDEX ix_audit_logs_action (action),
    INDEX ix_audit_logs_entity_type (entity_type),
    INDEX ix_audit_logs_entity_id (entity_id),
    INDEX ix_audit_logs_performed_by (performed_by),
    INDEX ix_audit_logs_correlation_id (correlation_id),
    INDEX ix_audit_logs_created_at (created_at),
    INDEX ix_audit_logs_entity_lookup (
        entity_type,
        entity_id,
        created_at
    )
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;
```

---

# 65. Seed Data Strategy

Seed data must be idempotent.

Recommended approach:

1. Use stable policy names.
2. Query by name before insert.
3. Insert only missing policies.
4. Create version snapshot for active seed policies.
5. Do not duplicate audits unnecessarily.
6. Commit once after all seed operations.

---

# 66. Required Seed Policies

## Fraud rejection

```text
Priority: 300
Decision: REJECT
Condition: fraud_risk_score >= 0.85
```

## Fraud manual review

```text
Priority: 250
Decision: MANUAL_REVIEW
Conditions:
fraud_risk_score >= 0.6
fraud_risk_score < 0.85
```

## Outstanding-balance rejection

```text
Priority: 220
Decision: REJECT
Condition: outstanding_balance > 10000
```

## Premium override approval

```text
Priority: 120
Decision: APPROVE
Conditions:
customer_segment = PREMIUM
customer_tenure_months >= 18
credit_score >= 780
fraud_risk_score < 0.4
```

## Standard upgrade approval

```text
Priority: 100
Decision: APPROVE
Conditions:
customer_tenure_months >= 24
credit_score >= 750
payment_defaults = 0
fraud_risk_score < 0.6
```

---

# 67. Seed Record Metadata

Recommended:

```text
source = SEEDED
status = ACTIVE
created_by = system_seed
approved_by = system_seed
current_version = 1
```

Create `policy_versions` version 1 for every active seed policy.

---

# 68. Seed Command

```bash
python -m app.db.seed
```

Expected output:

```text
Seed completed.
Created: 5
Skipped existing: 0
```

Second run:

```text
Seed completed.
Created: 0
Skipped existing: 5
```

---

# 69. Test Database Strategy

The test suite must use MySQL.

Do not use SQLite because:

- JSON behavior differs
- Constraint behavior differs
- Index behavior differs
- Transaction semantics may differ
- SQL syntax may differ

Recommended test database:

```text
decisionflow_test
```

---

# 70. Test Database Setup

```sql
CREATE DATABASE IF NOT EXISTS decisionflow_test
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

GRANT ALL PRIVILEGES ON decisionflow_test.*
  TO 'decisionflow'@'%';
```

Environment:

```text
TEST_DATABASE_URL=mysql+pymysql://decisionflow:decisionflow@localhost:3306/decisionflow_test
```

---

# 71. Test Isolation Options

## Preferred

Wrap each test in a transaction and roll back.

## Alternative

Truncate tables between tests.

Required truncate order:

```text
audit_logs
evaluation_rule_results
evaluations
policy_versions
policies
```

Disable foreign-key checks only in controlled test setup if needed.

---

# 72. Test Fixtures

Recommended fixtures:

```text
db_engine
db_session
clean_database
seeded_policies
active_approval_policy
active_rejection_policy
draft_policy
sample_evaluation
```

---

# 73. Repository Query Requirements

## List policies

Support:

- Pagination
- Status filter
- Decision filter
- Source filter
- Search
- Sort

## Active policies

Query:

```sql
WHERE domain = :domain
AND status = 'ACTIVE'
ORDER BY priority DESC, current_version DESC, id ASC
```

## Evaluation history

Support:

- Decision
- Customer ID
- Date range
- Policy ID
- Minimum confidence

## Audit history

Support:

- Action
- Entity type
- Entity ID
- User
- Date range

---

# 74. Pagination Query Pattern

```sql
SELECT ...
FROM ...
WHERE ...
ORDER BY ...
LIMIT :page_size
OFFSET :offset;
```

Count query:

```sql
SELECT COUNT(*)
FROM ...
WHERE ...;
```

Default:

```text
page = 1
page_size = 20
```

Maximum:

```text
page_size = 100
```

---

# 75. Analytics Queries

## Policy summary

```sql
SELECT
    COUNT(*) AS total,
    SUM(status = 'ACTIVE') AS active,
    SUM(status = 'DRAFT') AS draft,
    SUM(status = 'PENDING_APPROVAL') AS pending_approval,
    SUM(status = 'DISABLED') AS disabled,
    SUM(source = 'AI_GENERATED') AS ai_generated
FROM policies
WHERE status <> 'ARCHIVED';
```

---

# 76. Decision summary

```sql
SELECT
    COUNT(*) AS total,
    SUM(decision = 'APPROVE') AS approve,
    SUM(decision = 'REJECT') AS reject_count,
    SUM(decision = 'MANUAL_REVIEW') AS manual_review,
    AVG(decision_confidence) AS average_confidence
FROM evaluations
WHERE evaluated_at >= :from_date
  AND evaluated_at < :to_date;
```

---

# 77. Approval Rate

Calculate safely:

```text
approve / total * 100
```

When total is zero:

```text
0
```

Do not divide by zero.

---

# 78. Average Latency

Because metrics are in JSON, MySQL can read them:

```sql
SELECT
    AVG(
        CAST(
            JSON_UNQUOTE(
                JSON_EXTRACT(metrics_json, '$.engine_latency_ms')
            ) AS UNSIGNED
        )
    ) AS average_engine_latency_ms
FROM evaluations;
```

For simplicity and speed, frequently queried metrics may later become typed columns.

For the POC, JSON extraction is acceptable.

---

# 79. Optional Typed Metric Columns

If analytics performance becomes difficult, add:

```text
engine_latency_ms INT
explanation_latency_ms INT
total_latency_ms INT
```

to `evaluations`.

This is an optional optimization.

The original `metrics_json` should remain the complete source snapshot.

---

# 80. Decision Distribution Query

```sql
SELECT
    decision,
    COUNT(*) AS count
FROM evaluations
WHERE evaluated_at >= :from_date
  AND evaluated_at < :to_date
GROUP BY decision;
```

---

# 81. Decision Trend Query

Daily:

```sql
SELECT
    DATE(evaluated_at) AS period,
    SUM(decision = 'APPROVE') AS approve,
    SUM(decision = 'REJECT') AS reject_count,
    SUM(decision = 'MANUAL_REVIEW') AS manual_review
FROM evaluations
WHERE evaluated_at >= :from_date
  AND evaluated_at < :to_date
GROUP BY DATE(evaluated_at)
ORDER BY period;
```

---

# 82. Top Triggered Policies Query

```sql
SELECT
    policy_id,
    policy_name,
    decision,
    COUNT(*) AS trigger_count
FROM evaluation_rule_results
WHERE matched = TRUE
GROUP BY
    policy_id,
    policy_name,
    decision
ORDER BY trigger_count DESC
LIMIT :limit;
```

---

# 83. Match Rate Query

```sql
SELECT
    policy_id,
    policy_name,
    SUM(matched = TRUE) AS matches,
    COUNT(*) AS evaluated_count,
    (
        SUM(matched = TRUE) / COUNT(*)
    ) * 100 AS match_rate
FROM evaluation_rule_results
GROUP BY policy_id, policy_name;
```

---

# 84. Audit Query

Recent activity:

```sql
SELECT *
FROM audit_logs
ORDER BY created_at DESC
LIMIT 10;
```

Entity history:

```sql
SELECT *
FROM audit_logs
WHERE entity_type = :entity_type
  AND entity_id = :entity_id
ORDER BY created_at DESC;
```

Correlation trace:

```sql
SELECT *
FROM audit_logs
WHERE correlation_id = :correlation_id
ORDER BY created_at ASC;
```

---

# 85. Database Health Check

Use:

```sql
SELECT 1;
```

Optional metadata:

```sql
SELECT VERSION();
```

Readiness response may include:

```text
database_type = mysql
database_version = 8.x
```

Do not expose full connection details.

---

# 86. Database Error Mapping

Common mapping:

| Database Error | Application Error |
|---|---|
| Connection failure | `DATABASE_UNAVAILABLE` |
| Unique constraint | `DUPLICATE_POLICY_NAME` |
| Foreign key failure | `DATABASE_CONSTRAINT_ERROR` |
| Deadlock | Retry or `DATABASE_TRANSACTION_ERROR` |
| Timeout | `DATABASE_TIMEOUT` |
| Invalid JSON | `DATABASE_VALIDATION_ERROR` |

Do not return raw SQL to API clients.

---

# 87. Retry Policy

For normal application writes:

- Do not automatically retry every transaction.
- One retry may be used for deadlock or transient connection reset.
- Never retry validation or unique-constraint errors.
- Preserve correlation ID across retry.

---

# 88. Connection Pooling

Required:

```text
pool_pre_ping = true
```

Recommended:

```text
pool_recycle = 1800
```

This helps recover stale connections.

---

# 89. Session Management

Per request:

```text
Open session
Execute service workflow
Commit or rollback
Close session
```

Never use one global session.

Never pass an active SQLAlchemy session to frontend or AI provider code.

---

# 90. Repository Boundaries

Repositories own:

- SQLAlchemy queries
- Inserts
- Updates
- Deletes
- Aggregate queries

Services own:

- Business state changes
- Validation sequence
- Transaction meaning
- Audit calls
- Cross-repository orchestration

Routers own:

- HTTP input
- Dependency resolution
- HTTP output

---

# 91. Data Retention

POC recommendation:

- Policies: retain
- Policy versions: retain
- Evaluations: retain
- Rule results: retain
- Audit logs: retain

No automated cleanup is required during the hackathon.

Future production retention should consider:

- Regulatory rules
- Privacy
- Cost
- Analytics needs
- Customer-data minimization

---

# 92. Backup Strategy

For the hackathon:

- MySQL data volume
- Optional `mysqldump` before demo
- Git contains schema and seed, not runtime data

Backup command:

```bash
mysqldump \
  -h localhost \
  -u decisionflow \
  -p decisionflow \
  > decisionflow_backup.sql
```

Restore:

```bash
mysql \
  -h localhost \
  -u decisionflow \
  -p decisionflow \
  < decisionflow_backup.sql
```

Do not commit backup files containing sensitive data.

---

# 93. Demo Data Persistence

Docker named volume:

```text
decisionflow_mysql_data
```

This allows data to survive container restart.

To reset:

```bash
docker compose down
docker volume rm decisionflow-ai_decisionflow_mysql_data
docker compose up --build
```

The exact volume name may vary by project directory.

---

# 94. Demo Reset Safety

Create a script:

```text
scripts/reset_demo.sh
```

It must clearly warn:

```text
This deletes the local DecisionFlow MySQL demo volume.
```

Do not run reset automatically on normal startup.

---

# 95. Security Requirements

- Credentials only in environment variables.
- Database user should not be root.
- Use parameterized SQL.
- Use SQLAlchemy ORM or Core.
- No string-concatenated SQL from user input.
- No API keys in JSON columns.
- No hidden prompts in audit snapshots.
- Do not expose connection strings through APIs.
- Restrict database port in production.
- Use separate credentials for test and production.

---

# 96. Privacy Considerations

The request snapshot may contain customer data.

Recommended POC approach:

- Use synthetic demo data.
- Do not use real customer information.
- Store only necessary fields.
- Use demo customer IDs.
- Do not include email, phone, or address.

---

# 97. Performance Baseline

Expected POC size:

```text
Policies: under 100
Evaluations: under 10,000
Rule results: under 100,000
Audit logs: under 100,000
```

The proposed indexes are sufficient.

No partitioning is required.

---

# 98. Query Performance Targets

For POC dataset:

```text
Active policy lookup: < 100 ms
Policy list: < 500 ms
Evaluation insert: < 300 ms
Audit list: < 500 ms
Analytics summary: < 1 second
```

Application and network latency may add overhead.

---

# 99. Explain Plan Checks

For slow queries, use:

```sql
EXPLAIN
SELECT ...
```

Verify that:

- Active-policy lookup uses composite index.
- Evaluation date filters use evaluated_at index.
- Audit entity lookup uses entity composite index.
- Policy search may scan text; acceptable for POC.

---

# 100. Optional Full-Text Search

Not required for POC.

Future option:

```sql
FULLTEXT(name, description, reason)
```

For the hackathon, case-insensitive `LIKE` is sufficient.

---

# 101. Optional Future Tables

Not part of MVP unless time permits.

## policy_approvals

For multi-step approval workflows.

## domains

For configurable domain metadata.

## field_definitions

For database-driven field catalogue.

## operator_definitions

For configurable operators.

## users

For real authentication.

## tenants

For multi-tenancy.

## policy_conflicts

For persisted conflict lifecycle.

## ai_operations

For detailed provider usage and cost.

## decision_batches

For bulk evaluation.

---

# 102. Future Normalization Options

The current JSON rule tree is appropriate for POC.

Future enterprise design may normalize:

```text
policy_condition_groups
policy_conditions
```

However, that would increase complexity.

The current design prioritizes:

- Fast implementation
- Exact rule snapshot
- Flexible nesting
- Simple versioning

---

# 103. Data Export

Future APIs may export:

- Policy JSON
- Audit CSV
- Evaluation CSV
- Version comparison

The database already stores the required source data.

No export table is required.

---

# 104. Repository Method Expectations

## Policy repository

```python
create
get_by_id
get_by_name
list
update
delete_draft
archive
get_active_by_domain
```

## Version repository

```python
create_snapshot
list_by_policy
get_version
```

## Evaluation repository

```python
save_complete_evaluation
get_by_id
list
```

## Audit repository

```python
create
get_by_id
list
```

## Analytics repository

```python
get_summary
get_decision_distribution
get_decision_trend
get_top_policies
```

---

# 105. MySQL-Specific Implementation Notes

## JSON

Use SQLAlchemy `JSON`.

## Text

Use `Text`.

## Timestamps

Use `DateTime`.

## Boolean

Use `Boolean`.

## Engine

Use InnoDB.

## Character set

Use utf8mb4.

## Collation

Use utf8mb4_unicode_ci.

## Driver

Use PyMySQL.

---

# 106. No-SQLite Rule

The following are prohibited in integrated code:

```text
sqlite:///
sqlite3
decisionflow.db
Base.metadata.create_all as deployment strategy
SQLite-specific tests
SQLite fallback
```

Repository search before final merge:

```bash
grep -R "sqlite" .
grep -R "decisionflow.db" .
```

Expected result:

```text
No runtime references
```

Documentation explaining that SQLite was rejected may remain only if clearly historical, but current docs should use MySQL.

---

# 107. Data Integrity Checklist

Before handoff:

- Unique policy name works.
- Policy version uniqueness works.
- Policy version cannot exist without policy.
- Rule result cannot exist without evaluation.
- Deleting evaluation cascades rule results.
- Winning policy deletion sets null.
- Confidence rejects invalid values.
- Required JSON columns reject null.
- Seed is idempotent.
- Activation transaction is atomic.
- Decision transaction is atomic.
- Audit records have correlation IDs.

---

# 108. Migration Verification Checklist

Run:

```bash
alembic upgrade head
alembic current
```

Verify tables:

```sql
SHOW TABLES;
```

Expected:

```text
alembic_version
policies
policy_versions
evaluations
evaluation_rule_results
audit_logs
```

Verify indexes:

```sql
SHOW INDEX FROM policies;
SHOW INDEX FROM evaluations;
SHOW INDEX FROM audit_logs;
```

---

# 109. Seed Verification Checklist

Run:

```bash
python -m app.db.seed
```

Query:

```sql
SELECT
    name,
    status,
    priority,
    decision,
    current_version
FROM policies
ORDER BY priority DESC;
```

Expected five active seed policies.

Query:

```sql
SELECT
    policy_id,
    version,
    name
FROM policy_versions;
```

Expected one version per active seed policy.

---

# 110. Evaluation Verification Checklist

After one decision:

```sql
SELECT
    id,
    customer_id,
    decision,
    decision_confidence,
    winning_policy_id,
    evaluated_at
FROM evaluations
ORDER BY evaluated_at DESC
LIMIT 1;
```

Then:

```sql
SELECT
    policy_name,
    priority,
    decision,
    result_status,
    matched
FROM evaluation_rule_results
WHERE evaluation_id = :evaluation_id
ORDER BY priority DESC;
```

---

# 111. Audit Verification Checklist

```sql
SELECT
    action,
    entity_type,
    entity_id,
    performed_by,
    correlation_id,
    created_at
FROM audit_logs
ORDER BY created_at DESC
LIMIT 20;
```

Expected:

- Policy creation
- Activation
- Decision evaluation

---

# 112. Analytics Verification Checklist

After demo decisions:

```sql
SELECT
    decision,
    COUNT(*)
FROM evaluations
GROUP BY decision;
```

Expected values should match dashboard counts.

---

# 113. Database Definition of Done

The database module is complete only when:

## Setup

- MySQL starts.
- Database exists.
- Application user connects.
- Character set is utf8mb4.

## Schema

- All core tables exist.
- Constraints exist.
- Indexes exist.
- JSON columns are valid.
- Foreign keys behave correctly.

## Migrations

- Alembic upgrade succeeds.
- Current revision is head.
- Fresh database migration succeeds.

## Seed

- Five policies are seeded.
- Policy versions exist.
- Re-running seed creates no duplicates.

## Runtime

- Policy create persists.
- Policy activation persists atomically.
- Evaluation and rule traces persist atomically.
- Audit persists.
- Analytics query succeeds.

## Quality

- Test database uses MySQL.
- No SQLite references remain.
- No credentials are committed.
- Queries meet POC performance needs.

---

# 114. Database Handoff Package

The backend engineer must provide:

```text
Migration revision:
<revision id>

Tables:
- policies
- policy_versions
- evaluations
- evaluation_rule_results
- audit_logs

Database:
MySQL 8.0+

Connection:
Configured through DATABASE_URL

Migration command:
alembic upgrade head

Seed command:
python -m app.db.seed

Test database:
decisionflow_test

Known limitations:
<list>
```

---

# 115. Database Handoff Message Template

```text
Database module handoff

Branch:
feature/backend-rule-engine

Latest commit:
<commit hash>

Database:
MySQL 8.0+

Driver:
PyMySQL

ORM:
SQLAlchemy 2.x

Migration head:
<revision>

Completed:
- Core schema
- Foreign keys
- Indexes
- JSON columns
- Policy versioning
- Evaluation persistence
- Rule-result persistence
- Audit persistence
- Analytics queries
- Seed script
- MySQL test database setup

Run:
1. docker compose up -d mysql
2. cd backend
3. alembic upgrade head
4. python -m app.db.seed

Verification:
- Migrations: passed
- Seed first run: passed
- Seed second run: passed
- Repository tests: passed
- Transaction tests: passed

Known limitations:
- <list>

SQLite references:
None
```

---

# 116. Integration Lead Verification

The Integration Lead should verify:

1. MySQL health.
2. Database creation.
3. Application-user login.
4. Alembic migration.
5. Table list.
6. Index list.
7. Seed first run.
8. Seed second run.
9. Policy create.
10. Policy activation.
11. Policy version snapshot.
12. Approval evaluation.
13. Rejection evaluation.
14. Rule-result persistence.
15. Audit persistence.
16. Analytics counts.
17. Correlation trace.
18. No SQLite artifacts.

---

# 117. Final Database Architecture Statement

DecisionFlow AI uses a hybrid relational and JSON persistence model.

Relational columns are used for:

```text
Identifiers
Status
Priority
Decision
Version
Customer reference
Timestamps
Correlation IDs
Frequently filtered values
```

JSON columns are used for:

```text
Condition trees
AI metadata
Validation details
Conflict details
Decision requests
Resolution evidence
Explanation metadata
Metrics
Warnings
Condition traces
Audit snapshots
```

This approach gives the POC:

- Strong transactional behavior
- Clear auditability
- Flexible rule structures
- Simple version snapshots
- Practical analytics
- Easy MySQL deployment
- A realistic path toward enterprise hardening

The database is not merely storage.

It is the governed record of:

```text
What policy existed
Which version was active
What request was evaluated
Which rules matched
Why one rule won
What decision was returned
How the result was explained
Who performed the action
When it happened
```

That traceability is central to the value of DecisionFlow AI.
