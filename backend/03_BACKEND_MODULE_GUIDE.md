# DecisionFlow AI
## Backend and Rule Engine Module Implementation Guide

**Document ID:** DFA-BE-003  
**Version:** 1.0  
**Status:** Hackathon POC Baseline — MySQL Edition  
**Primary Owner:** Backend and Rule Engine Engineer  
**Reviewers:** Technical Architect and Integration Lead  
**Dependent Modules:** Frontend, AI Module, Integration Layer  
**Primary Branch:** `feature/backend-rule-engine`

---

# 1. Purpose

This document provides the complete implementation specification for the backend and rule-engine owner.

The engineer following this guide should be able to build the assigned module end to end without requiring access to any previous discussion.

The backend engineer is responsible for:

- MySQL database setup
- SQLAlchemy models
- Alembic migrations
- Policy persistence
- Policy CRUD APIs
- Policy activation and disable flows
- Rule-engine implementation
- Operator registry
- Condition evaluation
- Priority resolution
- Deterministic confidence calculations
- Evaluation persistence support
- Audit persistence support
- Analytics queries
- Configuration endpoints
- Seed data
- Unit tests
- Backend Docker support

The backend engineer is **not** responsible for:

- React UI
- LLM provider implementation
- AI policy generation prompts
- AI explanation generation
- Final decision orchestration endpoint wiring
- Final demo presentation
- Architecture ownership
- Shared API contract changes

Those areas belong to other team members.

---

# 2. Module Objective

The backend module must provide a stable, deterministic, testable foundation for DecisionFlow AI.

It must allow the rest of the team to:

1. Store policies in MySQL.
2. Retrieve and filter policies.
3. Activate and disable policies.
4. Evaluate customer data against active policies.
5. Resolve multiple matching policies deterministically.
6. Store decision results and rule traces.
7. Store audit events.
8. Provide analytics data.
9. Expose stable interfaces for the integration lead.
10. Continue working even when the AI provider is unavailable.

The most important backend principle is:

> The rule engine must never depend on an LLM to produce a business decision.

---

# 3. Frozen Technology Stack

Use the following stack unless the Technical Architect explicitly approves a change.

## Language and framework

```text
Python 3.11+
FastAPI
Uvicorn
```

## Validation

```text
Pydantic v2
pydantic-settings
```

## Persistence

```text
MySQL 8.0+
SQLAlchemy 2.x
PyMySQL
Alembic
```

## Testing

```text
Pytest
pytest-asyncio
httpx
FastAPI TestClient
```

## Packaging

```text
Docker
Docker Compose
```

## Logging

```text
Python logging
Correlation IDs
Structured log messages
```

---

# 4. Required Deliverables

The backend engineer must deliver all of the following.

## 4.1 Working MySQL-backed backend

- Backend starts successfully.
- Database connection is healthy.
- Alembic migrations run successfully.
- Seed data can be loaded repeatedly.
- No SQLite fallback exists.

## 4.2 Policy APIs

```text
POST   /api/v1/policies
GET    /api/v1/policies
GET    /api/v1/policies/{policy_id}
PUT    /api/v1/policies/{policy_id}
DELETE /api/v1/policies/{policy_id}
POST   /api/v1/policies/{policy_id}/activate
POST   /api/v1/policies/{policy_id}/disable
```

## 4.3 Configuration APIs

```text
GET /api/v1/config/fields
GET /api/v1/config/operators
```

## 4.4 Rule-engine package

Must support:

- `all` condition groups
- `any` condition groups
- One nested level
- Supported operators
- Missing-field handling
- Condition-level traces
- Matched/unmatched/skipped policies
- Priority-based resolution
- Severity tie-breaker
- Deterministic confidence

## 4.5 Persistence interfaces for integration

The integration lead must be able to call:

```python
policy_service.get_active_policies(domain)
rule_engine.evaluate(request_data, policies)
priority_resolver.resolve(matched_policies)
confidence_calculator.calculate(...)
evaluation_repository.save(...)
audit_service.record_decision(...)
analytics_service.get_summary(...)
```

## 4.6 Analytics and audit APIs

```text
GET /api/v1/analytics/summary
GET /api/v1/analytics/decision-distribution
GET /api/v1/analytics/decision-trend
GET /api/v1/analytics/top-policies

GET /api/v1/audit
GET /api/v1/audit/{audit_id}
```

## 4.7 Tests

Critical backend functionality must be covered by automated tests.

## 4.8 Handoff notes

The final handoff must include:

- Branch name
- Latest commit hash
- Setup commands
- Migration command
- Seed command
- Test command
- Known limitations
- Example API calls
- Files changed

---

# 5. Repository Ownership

The backend engineer owns the following directories.

```text
backend/
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   └── v1/
│   │       ├── config.py
│   │       ├── policies.py
│   │       ├── analytics.py
│   │       └── audit.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── error_handlers.py
│   │   ├── ids.py
│   │   └── logging.py
│   │
│   ├── schemas/
│   │   ├── common.py
│   │   ├── policy.py
│   │   ├── evaluation.py
│   │   ├── analytics.py
│   │   └── audit.py
│   │
│   ├── models/
│   │   ├── policy.py
│   │   ├── policy_version.py
│   │   ├── evaluation.py
│   │   ├── evaluation_rule_result.py
│   │   └── audit.py
│   │
│   ├── repositories/
│   │   ├── policy_repository.py
│   │   ├── policy_version_repository.py
│   │   ├── evaluation_repository.py
│   │   ├── audit_repository.py
│   │   └── analytics_repository.py
│   │
│   ├── services/
│   │   ├── policy_service.py
│   │   ├── validation_service.py
│   │   ├── audit_service.py
│   │   └── analytics_service.py
│   │
│   ├── engine/
│   │   ├── operators.py
│   │   ├── evaluator.py
│   │   ├── resolver.py
│   │   ├── confidence.py
│   │   ├── result_models.py
│   │   └── exceptions.py
│   │
│   └── db/
│       ├── base.py
│       ├── session.py
│       ├── init_db.py
│       └── seed.py
│
├── alembic/
├── tests/
├── requirements.txt
├── Dockerfile
└── alembic.ini
```

The backend engineer may modify `backend/app/main.py` only for router registration, database startup, or error-handler registration. The integration lead remains the final owner of application wiring.

---

# 6. Local Setup

## 6.1 Create environment

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
```

## 6.2 Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 6.3 Minimum requirements file

```text
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
```

Pin versions after the first stable installation.

## 6.4 Create local environment file

Create:

```text
backend/.env
```

Example:

```text
APP_NAME=DecisionFlow AI
APP_ENV=development
API_V1_PREFIX=/api/v1
LOG_LEVEL=INFO

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=decisionflow
MYSQL_USER=decisionflow
MYSQL_PASSWORD=decisionflow

DATABASE_URL=mysql+pymysql://decisionflow:decisionflow@localhost:3306/decisionflow

DEFAULT_POLICY_PRIORITY=100
MAX_POLICY_PRIORITY=1000
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

Do not commit `.env`.

Create `.env.example` with the same keys and safe placeholder values.

---

# 7. MySQL Setup

## 7.1 Required database

```text
Database name: decisionflow
Character set: utf8mb4
Collation: utf8mb4_unicode_ci
```

## 7.2 Recommended local SQL

```sql
CREATE DATABASE IF NOT EXISTS decisionflow
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'decisionflow'@'%'
  IDENTIFIED BY 'decisionflow';

GRANT ALL PRIVILEGES ON decisionflow.*
  TO 'decisionflow'@'%';

FLUSH PRIVILEGES;
```

## 7.3 Docker Compose service

The repository-level `docker-compose.yml` should contain a MySQL service.

```yaml
services:
  mysql:
    image: mysql:8.0
    container_name: decisionflow-mysql
    restart: unless-stopped
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
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-proot"]
      interval: 5s
      timeout: 5s
      retries: 20

volumes:
  decisionflow_mysql_data:
```

The backend container should use:

```text
DATABASE_URL=mysql+pymysql://decisionflow:decisionflow@mysql:3306/decisionflow
```

---

# 8. Configuration Management

Implement a central settings object.

## File

```text
backend/app/core/config.py
```

## Required behavior

- Read from environment.
- Validate required settings.
- Expose database URL.
- Expose API prefix.
- Expose pagination settings.
- Never hardcode credentials.

## Suggested interface

```python
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DecisionFlow AI"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"

    database_url: str

    default_policy_priority: int = 100
    max_policy_priority: int = 1000
    default_page_size: int = 20
    max_page_size: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

---

# 9. SQLAlchemy Session Management

## File

```text
backend/app/db/session.py
```

## Required behavior

- One SQLAlchemy engine.
- `pool_pre_ping=True`.
- Request-scoped sessions.
- Rollback on exception.
- Close sessions in `finally`.
- No global mutable session.

## Suggested implementation shape

```python
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

---

# 10. Database Base and Naming Convention

## File

```text
backend/app/db/base.py
```

Use SQLAlchemy Declarative Base.

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

Recommended table naming:

```text
policies
policy_versions
evaluations
evaluation_rule_results
audit_logs
```

Use snake_case column names.

---

# 11. Database Models

The detailed database design will exist in `07_DATABASE_DESIGN.md`, but the backend engineer must implement the following baseline.

## 11.1 Policy model

### Table

```text
policies
```

### Required columns

| Column | Type | Notes |
|---|---|---|
| `id` | VARCHAR(40) | Primary key |
| `name` | VARCHAR(120) | Unique |
| `description` | TEXT | Nullable |
| `domain` | VARCHAR(50) | Indexed |
| `status` | VARCHAR(30) | Indexed |
| `priority` | INT | Indexed |
| `decision` | VARCHAR(30) | Indexed |
| `conditions_json` | JSON | Required |
| `reason` | TEXT | Nullable |
| `source` | VARCHAR(30) | Required |
| `current_version` | INT | Required |
| `ai_metadata_json` | JSON | Nullable |
| `created_by` | VARCHAR(100) | Nullable |
| `approved_by` | VARCHAR(100) | Nullable |
| `created_at` | DATETIME(6) | UTC |
| `updated_at` | DATETIME(6) | UTC |
| `activated_at` | DATETIME(6) | Nullable |
| `disabled_at` | DATETIME(6) | Nullable |

### Constraints

- Unique name.
- Priority between 1 and 1000.
- Status enum validation at application level.
- Decision enum validation at application level.

## 11.2 Policy version model

### Table

```text
policy_versions
```

### Required columns

| Column | Type |
|---|---|
| `id` | VARCHAR(40) |
| `policy_id` | VARCHAR(40) |
| `version` | INT |
| `name` | VARCHAR(120) |
| `description` | TEXT |
| `domain` | VARCHAR(50) |
| `status_snapshot` | VARCHAR(30) |
| `priority` | INT |
| `decision` | VARCHAR(30) |
| `conditions_json` | JSON |
| `reason` | TEXT |
| `source` | VARCHAR(30) |
| `ai_metadata_json` | JSON |
| `created_by` | VARCHAR(100) |
| `approved_by` | VARCHAR(100) |
| `created_at` | DATETIME(6) |

### Constraints

Unique composite key:

```text
(policy_id, version)
```

Versions must be immutable after creation.

## 11.3 Evaluation model

### Table

```text
evaluations
```

### Required columns

| Column | Type |
|---|---|
| `id` | VARCHAR(40) |
| `request_id` | VARCHAR(100) |
| `domain` | VARCHAR(50) |
| `customer_id` | VARCHAR(100) |
| `request_json` | JSON |
| `decision` | VARCHAR(30) |
| `decision_confidence` | INT |
| `winning_policy_id` | VARCHAR(40), nullable |
| `winning_policy_version` | INT, nullable |
| `resolution_json` | JSON |
| `explanation_json` | JSON |
| `metrics_json` | JSON |
| `warnings_json` | JSON |
| `correlation_id` | VARCHAR(100) |
| `created_by` | VARCHAR(100), nullable |
| `evaluated_at` | DATETIME(6) |

Indexes:

- `customer_id`
- `decision`
- `evaluated_at`
- `winning_policy_id`
- `correlation_id`

## 11.4 Evaluation rule result model

### Table

```text
evaluation_rule_results
```

### Required columns

| Column | Type |
|---|---|
| `id` | VARCHAR(40) |
| `evaluation_id` | VARCHAR(40) |
| `policy_id` | VARCHAR(40) |
| `policy_version` | INT |
| `policy_name` | VARCHAR(120) |
| `priority` | INT |
| `decision` | VARCHAR(30) |
| `result_status` | VARCHAR(40) |
| `matched` | BOOLEAN |
| `condition_results_json` | JSON |
| `missing_fields_json` | JSON |
| `reason` | TEXT |
| `created_at` | DATETIME(6) |

`result_status` values:

```text
MATCHED
UNMATCHED
SKIPPED_MISSING_FIELD
SKIPPED_INVALID_DATA
```

## 11.5 Audit model

### Table

```text
audit_logs
```

### Required columns

| Column | Type |
|---|---|
| `id` | VARCHAR(40) |
| `action` | VARCHAR(50) |
| `entity_type` | VARCHAR(50) |
| `entity_id` | VARCHAR(40) |
| `entity_version` | INT, nullable |
| `performed_by` | VARCHAR(100), nullable |
| `summary` | TEXT |
| `request_snapshot_json` | JSON, nullable |
| `result_snapshot_json` | JSON, nullable |
| `metadata_json` | JSON, nullable |
| `correlation_id` | VARCHAR(100) |
| `created_at` | DATETIME(6) |

Indexes:

- `action`
- `entity_type`
- `entity_id`
- `performed_by`
- `created_at`
- `correlation_id`

---

# 12. Identifier Generation

## File

```text
backend/app/core/ids.py
```

Identifiers should be strings with readable prefixes.

Examples:

```text
pol_...
ver_...
eval_...
rr_...
aud_...
```

A simple implementation may use UUID4.

```python
from uuid import uuid4


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"
```

Required prefixes:

```text
pol
ver
eval
rr
aud
cor
```

---

# 13. Alembic Migrations

## 13.1 Initialize

```bash
alembic init alembic
```

## 13.2 Configure

`alembic/env.py` must import all SQLAlchemy models and use the configured database URL.

## 13.3 First migration

Create:

```text
001_create_core_tables
```

It should create:

- policies
- policy_versions
- evaluations
- evaluation_rule_results
- audit_logs

## 13.4 Commands

```bash
alembic revision --autogenerate -m "create core tables"
alembic upgrade head
```

## 13.5 Rules

- Do not use `Base.metadata.create_all()` as the primary deployment path.
- It may be used temporarily in tests only.
- All persistent schema changes require an Alembic migration.
- Migrations must run against MySQL.
- Test the downgrade path if time permits.

---

# 14. Shared API Response Schemas

## File

```text
backend/app/schemas/common.py
```

Create reusable response models.

Suggested models:

```python
class ErrorDetail(BaseModel):
    path: str | None = None
    issue: str
    received: Any | None = None
    allowed_values: list[Any] | None = None
    suggestion: str | None = None


class ErrorBody(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] = []


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
```

The API contract requires the response envelope:

```json
{
  "success": true,
  "data": {},
  "meta": {},
  "correlation_id": "cor_..."
}
```

Do not return raw ORM objects.

---

# 15. Policy Pydantic Schemas

## File

```text
backend/app/schemas/policy.py
```

Implement at least:

```text
Condition
ConditionGroup
PolicyCreate
PolicyUpdate
PolicyResponse
PolicyListItem
PolicyFilters
PolicyActivateRequest
PolicyDisableRequest
AIMetadata
```

## 15.1 Condition

```python
class Condition(BaseModel):
    field: str
    operator: str
    value: Any | None = None
```

## 15.2 Condition group

The model must support recursive condition groups.

One acceptable design:

```python
class ConditionGroup(BaseModel):
    all: list["ConditionNode"] | None = None
    any: list["ConditionNode"] | None = None
```

Where `ConditionNode` is a union of:

```text
Condition
ConditionGroup
```

Validation requirements:

- Exactly one of `all` or `any`.
- At least one child.
- Maximum depth 2 for MVP.

## 15.3 Policy create

Required fields:

```text
name
domain
priority
decision
conditions
source
```

Server-managed fields must not be accepted from the client:

```text
id
version
created_at
updated_at
approved_by
activated_at
```

---

# 16. Domain Field Catalogue

## Recommended file

```text
backend/app/core/domain_catalogue.py
```

Use one shared source of truth.

Example shape:

```python
FIELD_CATALOGUE = {
    "customer_id": {
        "label": "Customer ID",
        "type": "string",
        "supported_operators": ["equals", "not_equals", "in", "not_in"],
    },
    "customer_tenure_months": {
        "label": "Customer Tenure",
        "type": "integer",
        "minimum": 0,
        "supported_operators": [
            "equals",
            "not_equals",
            "greater_than",
            "greater_than_or_equal",
            "less_than",
            "less_than_or_equal",
            "in",
            "not_in",
        ],
    },
    "credit_score": {
        "label": "Credit Score",
        "type": "integer",
        "minimum": 300,
        "maximum": 900,
        "supported_operators": [
            "equals",
            "not_equals",
            "greater_than",
            "greater_than_or_equal",
            "less_than",
            "less_than_or_equal",
            "in",
            "not_in",
        ],
    },
    "payment_defaults": {
        "label": "Payment Defaults",
        "type": "integer",
        "minimum": 0,
        "supported_operators": [
            "equals",
            "not_equals",
            "greater_than",
            "greater_than_or_equal",
            "less_than",
            "less_than_or_equal",
        ],
    },
    "fraud_risk_score": {
        "label": "Fraud Risk Score",
        "type": "number",
        "minimum": 0,
        "maximum": 1,
        "supported_operators": [
            "equals",
            "not_equals",
            "greater_than",
            "greater_than_or_equal",
            "less_than",
            "less_than_or_equal",
        ],
    },
    "monthly_bill_amount": {
        "label": "Monthly Bill Amount",
        "type": "number",
        "minimum": 0,
        "supported_operators": [
            "equals",
            "not_equals",
            "greater_than",
            "greater_than_or_equal",
            "less_than",
            "less_than_or_equal",
        ],
    },
    "requested_device_price": {
        "label": "Requested Device Price",
        "type": "number",
        "minimum": 0,
        "supported_operators": [
            "equals",
            "not_equals",
            "greater_than",
            "greater_than_or_equal",
            "less_than",
            "less_than_or_equal",
        ],
    },
    "customer_segment": {
        "label": "Customer Segment",
        "type": "string",
        "allowed_values": ["STANDARD", "PREMIUM", "BUSINESS"],
        "supported_operators": [
            "equals",
            "not_equals",
            "in",
            "not_in",
        ],
    },
    "current_plan": {
        "label": "Current Plan",
        "type": "string",
        "supported_operators": [
            "equals",
            "not_equals",
            "contains",
            "in",
            "not_in",
            "is_empty",
            "is_not_empty",
        ],
    },
    "outstanding_balance": {
        "label": "Outstanding Balance",
        "type": "number",
        "minimum": 0,
        "supported_operators": [
            "equals",
            "not_equals",
            "greater_than",
            "greater_than_or_equal",
            "less_than",
            "less_than_or_equal",
        ],
    },
    "is_existing_customer": {
        "label": "Existing Customer",
        "type": "boolean",
        "supported_operators": ["equals", "not_equals"],
    },
    "previous_upgrade_months_ago": {
        "label": "Previous Upgrade",
        "type": "integer",
        "minimum": 0,
        "supported_operators": [
            "equals",
            "not_equals",
            "greater_than",
            "greater_than_or_equal",
            "less_than",
            "less_than_or_equal",
        ],
    },
}
```

Both the frontend and AI module depend on this catalogue.

Do not duplicate field definitions elsewhere.

---

# 17. Operator Registry

## File

```text
backend/app/engine/operators.py
```

## Required operators

```text
equals
not_equals
greater_than
greater_than_or_equal
less_than
less_than_or_equal
contains
in
not_in
is_empty
is_not_empty
```

## Recommended implementation

Use named functions, not only anonymous lambdas, so errors are easier to debug.

```python
from collections.abc import Callable
from typing import Any


OperatorFunction = Callable[[Any, Any], bool]


def equals(actual: Any, expected: Any) -> bool:
    return actual == expected


def not_equals(actual: Any, expected: Any) -> bool:
    return actual != expected


def greater_than(actual: Any, expected: Any) -> bool:
    return actual > expected


def greater_than_or_equal(actual: Any, expected: Any) -> bool:
    return actual >= expected


def less_than(actual: Any, expected: Any) -> bool:
    return actual < expected


def less_than_or_equal(actual: Any, expected: Any) -> bool:
    return actual <= expected


def contains(actual: Any, expected: Any) -> bool:
    return expected in actual


def in_operator(actual: Any, expected: list[Any]) -> bool:
    return actual in expected


def not_in(actual: Any, expected: list[Any]) -> bool:
    return actual not in expected


def is_empty(actual: Any, _: Any = None) -> bool:
    return actual is None or actual == "" or actual == []


def is_not_empty(actual: Any, _: Any = None) -> bool:
    return not is_empty(actual)


OPERATORS: dict[str, OperatorFunction] = {
    "equals": equals,
    "not_equals": not_equals,
    "greater_than": greater_than,
    "greater_than_or_equal": greater_than_or_equal,
    "less_than": less_than,
    "less_than_or_equal": less_than_or_equal,
    "contains": contains,
    "in": in_operator,
    "not_in": not_in,
    "is_empty": is_empty,
    "is_not_empty": is_not_empty,
}
```

## Error behavior

Unsupported operator:

```text
UNSUPPORTED_OPERATOR
```

Type mismatch:

```text
OPERATOR_TYPE_ERROR
```

The engine must not catch all exceptions and silently return false. It must produce a traceable result.

---

# 18. Policy Validation Service

## File

```text
backend/app/services/validation_service.py
```

## Required checks

### Structural validation

- Policy has required fields.
- Condition group is valid.
- Maximum nesting depth is not exceeded.
- Root contains exactly one of `all` or `any`.

### Field validation

- Field exists in field catalogue.
- Field name is exact.
- Unknown field is rejected.

### Operator validation

- Operator exists.
- Operator is allowed for field type.

### Value validation

- Numeric fields receive numeric values.
- Integer fields do not receive strings.
- Boolean fields receive booleans.
- `in` and `not_in` receive arrays.
- `is_empty` and `is_not_empty` do not require values.
- Allowed-value fields use valid values.
- Minimum and maximum constraints are enforced.

### Policy validation

- Priority is 1 to 1000.
- Decision is valid.
- Domain is `telecom`.
- Name is valid.
- Status transition is valid.

## Required interface

```python
class PolicyValidationService:
    def validate_policy(self, policy: dict) -> ValidationResult:
        ...

    def validate_condition_tree(self, conditions: dict) -> ValidationResult:
        ...

    def validate_customer_payload(self, customer: dict) -> ValidationResult:
        ...
```

`ValidationResult` should contain:

```python
{
    "valid": True,
    "errors": [],
    "warnings": [],
}
```

---

# 19. Rule Engine Result Models

## File

```text
backend/app/engine/result_models.py
```

Create typed dataclasses or Pydantic models for:

```text
ConditionResult
PolicyEvaluationResult
EngineEvaluationResult
ResolutionResult
DecisionConfidenceResult
```

## Condition result

```python
class ConditionResult(BaseModel):
    field: str
    operator: str
    expected: Any | None
    actual: Any | None
    matched: bool
    status: str
    reason: str | None = None
```

Status values:

```text
MATCHED
UNMATCHED
MISSING_FIELD
INVALID_VALUE
ERROR
```

## Policy evaluation result

```python
class PolicyEvaluationResult(BaseModel):
    policy_id: str
    policy_name: str
    policy_version: int
    priority: int
    decision: str
    matched: bool
    result_status: str
    condition_results: list[ConditionResult]
    missing_fields: list[str] = []
    reason: str | None = None
```

## Engine result

```python
class EngineEvaluationResult(BaseModel):
    matched_policies: list[PolicyEvaluationResult]
    unmatched_policies: list[PolicyEvaluationResult]
    skipped_policies: list[PolicyEvaluationResult]
    policies_loaded: int
    policies_evaluated: int
    condition_count: int
    engine_latency_ms: int
```

---

# 20. Rule Evaluation Algorithm

## File

```text
backend/app/engine/evaluator.py
```

## Required interface

```python
class RuleEngine:
    def evaluate(
        self,
        request_data: dict,
        policies: list[dict],
    ) -> EngineEvaluationResult:
        ...
```

## Processing steps

```text
1. Start performance timer.
2. Iterate through policies.
3. Evaluate policy condition tree.
4. Capture condition-level result.
5. Classify policy as matched, unmatched, or skipped.
6. Count conditions.
7. Stop performance timer.
8. Return typed result.
```

## Condition-group behavior

### `all`

All children must match.

```text
all(A, B, C) = A AND B AND C
```

### `any`

At least one child must match.

```text
any(A, B, C) = A OR B OR C
```

## Missing-field behavior

The preferred rule for the POC is:

- Missing field does not crash evaluation.
- That condition receives `MISSING_FIELD`.
- A policy using `all` becomes skipped if a required condition cannot be evaluated.
- A policy using `any` can still match if another branch matches.
- Missing fields must be returned in the trace.

## Example

Policy:

```json
{
  "all": [
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

Request:

```json
{
  "credit_score": 790
}
```

Result:

```json
{
  "matched": false,
  "result_status": "SKIPPED_MISSING_FIELD",
  "missing_fields": ["fraud_risk_score"]
}
```

---

# 21. Recursive Evaluation Design

Use a recursive function.

Suggested signature:

```python
def evaluate_node(
    node: dict,
    request_data: dict,
    depth: int = 0,
) -> NodeEvaluationResult:
    ...
```

Rules:

- Reject depth greater than 2 during validation.
- Each condition generates a trace.
- Group result includes child traces.
- Do not mutate input policy objects.
- Preserve original expected values in the output.

---

# 22. Priority Resolver

## File

```text
backend/app/engine/resolver.py
```

## Required interface

```python
class PriorityResolver:
    def resolve(
        self,
        matched_policies: list[PolicyEvaluationResult],
    ) -> ResolutionResult:
        ...
```

## Resolution rules

1. If no policy matches:
   - Decision = `MANUAL_REVIEW`
   - Strategy = `DEFAULT_FALLBACK`
   - Winning policy = `None`

2. Sort matched policies by descending priority.

3. Highest priority wins.

4. If two or more policies have the same priority:
   - `REJECT` wins over `MANUAL_REVIEW`
   - `MANUAL_REVIEW` wins over `APPROVE`

5. If priority and decision severity are identical:
   - Highest policy version wins.

6. If still tied:
   - Lowest lexicographic policy ID wins.

The same input must always produce the same output.

## Resolution result

```python
class ResolutionResult(BaseModel):
    decision: str
    winning_policy: PolicyEvaluationResult | None
    strategy: str
    reason: str
    tie_breaker_used: bool
    competing_policy_ids: list[str]
```

---

# 23. Decision Confidence Calculator

## File

```text
backend/app/engine/confidence.py
```

## Important rule

Decision confidence is deterministic. It must not be generated by the LLM.

## Required interface

```python
class DecisionConfidenceCalculator:
    def calculate(
        self,
        request_data: dict,
        engine_result: EngineEvaluationResult,
        resolution: ResolutionResult,
    ) -> DecisionConfidenceResult:
        ...
```

## Suggested heuristic

Start from:

```text
100
```

Apply penalties:

| Condition | Penalty |
|---|---:|
| Missing fields caused skipped policy | 20 |
| Different outcomes matched | 15 |
| Winning result is manual review | 10 |
| Numeric value is near a winning threshold | 10 |
| Invalid policy data encountered | 10 |
| No policy matched | 25 |
| Each additional skipped policy | 5, capped |

Clamp result to:

```text
0 to 100
```

## Result model

```python
class DecisionConfidenceResult(BaseModel):
    score: int
    factors: list[dict]
```

Example:

```json
{
  "score": 75,
  "factors": [
    {
      "type": "MISSING_FIELDS",
      "impact": -20,
      "message": "One policy was skipped due to missing fields."
    },
    {
      "type": "MANUAL_REVIEW",
      "impact": -10,
      "message": "The final outcome requires human review."
    }
  ]
}
```

---

# 24. Policy Repository

## File

```text
backend/app/repositories/policy_repository.py
```

## Required interface

```python
class PolicyRepository:
    def create(self, policy: Policy) -> Policy:
        ...

    def get_by_id(self, policy_id: str) -> Policy | None:
        ...

    def get_by_name(self, name: str) -> Policy | None:
        ...

    def list(self, filters: PolicyFilters) -> tuple[list[Policy], int]:
        ...

    def update(self, policy: Policy) -> Policy:
        ...

    def delete(self, policy: Policy) -> None:
        ...

    def get_active_by_domain(self, domain: str) -> list[Policy]:
        ...
```

## Query behavior

`get_active_by_domain` should order policies by:

```text
priority DESC
current_version DESC
id ASC
```

Repository methods should not build API responses. They return ORM objects or repository result objects.

---

# 25. Policy Version Repository

## File

```text
backend/app/repositories/policy_version_repository.py
```

## Required interface

```python
class PolicyVersionRepository:
    def create_snapshot(self, policy: Policy) -> PolicyVersion:
        ...

    def list_by_policy(self, policy_id: str) -> list[PolicyVersion]:
        ...

    def get_version(
        self,
        policy_id: str,
        version: int,
    ) -> PolicyVersion | None:
        ...
```

Every activation or active-policy update must create an immutable snapshot.

---

# 26. Policy Service

## File

```text
backend/app/services/policy_service.py
```

## Required interface

```python
class PolicyService:
    def create_policy(
        self,
        payload: PolicyCreate,
        actor_id: str,
        correlation_id: str,
    ) -> PolicyResponse:
        ...

    def list_policies(
        self,
        filters: PolicyFilters,
    ) -> PaginatedPolicyResponse:
        ...

    def get_policy(self, policy_id: str) -> PolicyResponse:
        ...

    def update_policy(
        self,
        policy_id: str,
        payload: PolicyUpdate,
        actor_id: str,
        correlation_id: str,
    ) -> PolicyResponse:
        ...

    def activate_policy(
        self,
        policy_id: str,
        actor_id: str,
        approval_comment: str | None,
        correlation_id: str,
    ) -> PolicyResponse:
        ...

    def disable_policy(
        self,
        policy_id: str,
        actor_id: str,
        reason: str | None,
        correlation_id: str,
    ) -> PolicyResponse:
        ...

    def get_active_policies(self, domain: str) -> list[PolicyResponse]:
        ...
```

## Create behavior

1. Check duplicate name.
2. Validate policy.
3. Force initial status to `DRAFT`.
4. Set version to 1.
5. Persist policy.
6. Write audit record.
7. Commit transaction.
8. Return response.

## Update behavior

### Draft policy

- Update fields.
- Keep status draft.
- Increment version only if agreed by architect; recommended to increment on meaningful update.

### Active policy

Recommended POC behavior:

- Create a new draft version.
- Do not mutate currently active snapshot silently.
- Return `requires_activation=true`.

## Activate behavior

1. Load policy.
2. Validate allowed state.
3. Revalidate policy.
4. Run deterministic conflict check if available.
5. Block only confirmed blocking conflicts.
6. Create policy version snapshot.
7. Set status active.
8. Set approver and timestamp.
9. Write audit.
10. Commit atomically.

## Disable behavior

1. Load policy.
2. Require active status.
3. Set disabled.
4. Store reason.
5. Set disabled timestamp.
6. Write audit.
7. Commit.

---

# 27. Policy Router

## File

```text
backend/app/api/v1/policies.py
```

Implement exactly the routes in `02_API_CONTRACT.md`.

## Router responsibilities

- Parse path and query parameters.
- Resolve database dependency.
- Resolve actor and correlation ID.
- Call Policy Service.
- Return standard response envelope.
- Avoid business logic in route functions.

## Example shape

```python
@router.post("", status_code=status.HTTP_201_CREATED)
def create_policy(
    payload: PolicyCreate,
    db: Session = Depends(get_db),
    actor: ActorContext = Depends(get_actor_context),
    correlation_id: str = Depends(get_correlation_id),
):
    service = build_policy_service(db)
    policy = service.create_policy(
        payload=payload,
        actor_id=actor.user_id,
        correlation_id=correlation_id,
    )
    return success_response(
        data=policy,
        meta={},
        correlation_id=correlation_id,
    )
```

---

# 28. Configuration Router

## File

```text
backend/app/api/v1/config.py
```

Implement:

```text
GET /api/v1/config/fields
GET /api/v1/config/operators
```

These endpoints should return values from the shared catalogues.

No database call is needed.

---

# 29. Evaluation Repository

## File

```text
backend/app/repositories/evaluation_repository.py
```

The integration lead will use this repository through a service or direct dependency.

## Required interface

```python
class EvaluationRepository:
    def save(
        self,
        evaluation: Evaluation,
        rule_results: list[EvaluationRuleResult],
    ) -> Evaluation:
        ...

    def get_by_id(self, evaluation_id: str) -> Evaluation | None:
        ...

    def list(
        self,
        filters: EvaluationFilters,
    ) -> tuple[list[Evaluation], int]:
        ...
```

## Transaction rule

The evaluation record and all rule-result records should be committed in one transaction.

---

# 30. Audit Repository and Service

## Files

```text
backend/app/repositories/audit_repository.py
backend/app/services/audit_service.py
```

## Required service methods

```python
class AuditService:
    def record_policy_created(...):
        ...

    def record_policy_updated(...):
        ...

    def record_policy_activated(...):
        ...

    def record_policy_disabled(...):
        ...

    def record_decision(...):
        ...

    def list_audit(...):
        ...

    def get_audit(...):
        ...
```

## Audit principles

- Do not store secrets.
- Store enough context to explain an event.
- Request and result snapshots should be JSON.
- Use the same correlation ID as the API request.
- Record actor where available.
- Audit records should be append-only.

---

# 31. Analytics Repository

## File

```text
backend/app/repositories/analytics_repository.py
```

## Required queries

### Policy counts

- Total policies
- Active
- Draft
- Pending approval
- Disabled
- AI generated

### Decision counts

- Total
- Approve
- Reject
- Manual review

### Performance

- Average decision confidence
- Average engine latency
- Average total latency
- P95 latency if practical

### Quality

- Validation errors
- Conflicts detected
- AI fallback count

### Top policies

- Policy ID
- Policy name
- Decision
- Trigger count
- Match rate

---

# 32. Analytics Service and Router

## Files

```text
backend/app/services/analytics_service.py
backend/app/api/v1/analytics.py
```

Implement endpoints exactly as defined in the API contract.

The frontend depends on stable response keys.

Do not return database-specific names like:

```text
count_1
avg_2
```

Map all query results into Pydantic response models.

---

# 33. Audit Router

## File

```text
backend/app/api/v1/audit.py
```

Implement:

```text
GET /api/v1/audit
GET /api/v1/audit/{audit_id}
```

Support filtering and pagination.

---

# 34. Exception Types

## File

```text
backend/app/core/exceptions.py
```

Create application-specific exceptions.

Recommended exceptions:

```text
ApplicationError
PolicyNotFoundError
DuplicatePolicyNameError
PolicyValidationError
UnsupportedOperatorError
OperatorTypeError
InvalidPolicyStateError
PolicyActivationBlockedError
DatabaseUnavailableError
EvaluationPersistenceError
AuditNotFoundError
```

Each exception should carry:

```text
code
message
status_code
details
```

Do not raise raw SQLAlchemy exceptions to API consumers.

---

# 35. Global Error Handlers

## File

```text
backend/app/core/error_handlers.py
```

Register handlers for:

- Application errors
- Pydantic validation errors
- SQLAlchemy errors
- Unexpected errors

All handlers must return the contract error envelope.

Example:

```json
{
  "success": false,
  "error": {
    "code": "DATABASE_UNAVAILABLE",
    "message": "The persistence service is temporarily unavailable.",
    "details": []
  },
  "correlation_id": "cor_..."
}
```

Unexpected exceptions should be logged with traceback but return a safe message.

---

# 36. Correlation ID Dependency

## File

```text
backend/app/api/dependencies.py
```

Required behavior:

- Read `X-Correlation-ID`.
- Generate one if absent.
- Return it to route.
- Add it to response headers.
- Add it to logs.

Suggested approach:

```python
def get_correlation_id(
    x_correlation_id: str | None = Header(default=None),
) -> str:
    return x_correlation_id or new_id("cor")
```

---

# 37. Actor Context

For the POC, identity may be simulated.

Read:

```text
X-User-ID
X-User-Role
```

Defaults:

```text
user_id = demo_user
role = POLICY_MANAGER
```

Create:

```python
class ActorContext(BaseModel):
    user_id: str
    role: str
```

Do not implement full authentication unless requested later.

---

# 38. Logging

## File

```text
backend/app/core/logging.py
```

Minimum log fields:

```text
timestamp
level
correlation_id
event
entity_id
duration_ms
```

Example events:

```text
policy_created
policy_updated
policy_activated
policy_disabled
rule_evaluation_started
rule_evaluation_completed
database_error
audit_written
```

Never log:

- API keys
- Database passwords
- Full secrets
- Sensitive user data unnecessarily

For the demo, masked customer IDs are optional but preferred.

---

# 39. Seed Data

## File

```text
backend/app/db/seed.py
```

Seed data must be idempotent.

Required policies:

## Fraud rejection

```json
{
  "name": "Fraud rejection",
  "status": "ACTIVE",
  "priority": 300,
  "decision": "REJECT",
  "conditions": {
    "all": [
      {
        "field": "fraud_risk_score",
        "operator": "greater_than_or_equal",
        "value": 0.85
      }
    ]
  }
}
```

## Fraud manual review

```json
{
  "name": "Fraud manual review",
  "status": "ACTIVE",
  "priority": 250,
  "decision": "MANUAL_REVIEW",
  "conditions": {
    "all": [
      {
        "field": "fraud_risk_score",
        "operator": "greater_than_or_equal",
        "value": 0.6
      },
      {
        "field": "fraud_risk_score",
        "operator": "less_than",
        "value": 0.85
      }
    ]
  }
}
```

## Outstanding-balance rejection

```json
{
  "name": "Outstanding balance rejection",
  "status": "ACTIVE",
  "priority": 220,
  "decision": "REJECT",
  "conditions": {
    "all": [
      {
        "field": "outstanding_balance",
        "operator": "greater_than",
        "value": 10000
      }
    ]
  }
}
```

## Standard upgrade approval

```json
{
  "name": "Standard upgrade approval",
  "status": "ACTIVE",
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
        "field": "credit_score",
        "operator": "greater_than_or_equal",
        "value": 750
      },
      {
        "field": "payment_defaults",
        "operator": "equals",
        "value": 0
      },
      {
        "field": "fraud_risk_score",
        "operator": "less_than",
        "value": 0.6
      }
    ]
  }
}
```

## Premium override approval

```json
{
  "name": "Premium override approval",
  "status": "ACTIVE",
  "priority": 120,
  "decision": "APPROVE",
  "conditions": {
    "all": [
      {
        "field": "customer_segment",
        "operator": "equals",
        "value": "PREMIUM"
      },
      {
        "field": "customer_tenure_months",
        "operator": "greater_than_or_equal",
        "value": 18
      },
      {
        "field": "credit_score",
        "operator": "greater_than_or_equal",
        "value": 780
      },
      {
        "field": "fraud_risk_score",
        "operator": "less_than",
        "value": 0.4
      }
    ]
  }
}
```

Seed command:

```bash
python -m app.db.seed
```

Running it more than once must not create duplicates.

---

# 40. Testing Strategy

## 40.1 Test database

Preferred:

- Separate MySQL test database.
- Database name: `decisionflow_test`.
- Migrations run before test suite.
- Tables cleaned between tests.

Alternative for very limited time:

- Use transactions and roll back after each test.

Do not silently replace MySQL with SQLite in tests because JSON behavior and SQL semantics can differ.

## 40.2 Required test files

```text
tests/
├── conftest.py
├── test_operators.py
├── test_validation_service.py
├── test_evaluator.py
├── test_resolver.py
├── test_confidence.py
├── test_policy_repository.py
├── test_policy_service.py
├── test_policy_api.py
├── test_analytics_api.py
└── test_audit_api.py
```

---

# 41. Required Operator Tests

Test every operator with:

- Matching case
- Non-matching case
- Invalid type
- Edge or boundary value

Examples:

```text
greater_than(10, 5) → true
greater_than(5, 10) → false
greater_than("10", 5) → type error
in("PREMIUM", ["STANDARD", "PREMIUM"]) → true
is_empty("") → true
is_empty(None) → true
contains("Magenta Max", "Max") → true
```

---

# 42. Required Rule-Engine Tests

At minimum:

1. Single matching condition.
2. Single non-matching condition.
3. `all` group matches.
4. `all` group fails.
5. `any` group matches.
6. `any` group fails.
7. Nested group.
8. Missing field.
9. Unsupported operator.
10. Invalid value type.
11. Multiple matching policies.
12. No policies.
13. No matching policies.
14. Performance metric present.
15. Input objects are not mutated.

---

# 43. Required Resolver Tests

1. Highest priority wins.
2. Reject wins a same-priority tie.
3. Manual review wins over approval at same priority.
4. Higher version wins after same priority and same decision.
5. Policy ID resolves the final tie.
6. No match returns manual review fallback.
7. Resolution reason is present.
8. Result is deterministic across repeated calls.

---

# 44. Required Policy API Tests

1. Create valid policy.
2. Duplicate name returns 409.
3. Invalid field returns 400 or 422 according to contract.
4. Invalid operator is rejected.
5. Invalid value type is rejected.
6. List supports pagination.
7. List supports status filter.
8. Get existing policy.
9. Get missing policy returns 404.
10. Update draft.
11. Activate valid draft.
12. Block invalid activation.
13. Disable active policy.
14. Delete or archive behavior.
15. Correlation ID is returned.

---

# 45. Analytics Tests

1. Empty database returns zero values.
2. Policy counts are correct.
3. Decision counts are correct.
4. Percentages are calculated safely.
5. Average confidence is correct.
6. Top policies are ordered correctly.
7. Date filters work.

---

# 46. Audit Tests

1. Policy creation writes audit.
2. Policy activation writes audit.
3. Policy disable writes audit.
4. Decision evaluation can be recorded.
5. Audit list pagination works.
6. Audit detail returns snapshots.
7. Missing audit ID returns 404.

---

# 47. API Contract Compliance Tests

The backend engineer should compare every implemented route against `02_API_CONTRACT.md`.

Verify:

- Exact path
- Exact method
- Exact JSON field names
- Exact enum values
- Standard response envelope
- Standard error envelope
- Correlation ID
- Correct status codes
- Correct pagination metadata

Do not change the contract without architect approval.

---

# 48. Dockerfile

## File

```text
backend/Dockerfile
```

Recommended shape:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The final startup command may run migrations before Uvicorn through an entrypoint script.

---

# 49. Backend Startup Script

Optional but recommended.

## File

```text
backend/entrypoint.sh
```

```bash
#!/usr/bin/env sh
set -e

alembic upgrade head
python -m app.db.seed
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For production-style behavior, seeding should be configurable.

Example:

```text
SEED_DATA_ON_STARTUP=true
```

---

# 50. Health and Readiness Support

The integration lead owns final route wiring, but the backend engineer must provide database health utilities.

Required function:

```python
def check_database_health(db: Session) -> bool:
    db.execute(text("SELECT 1"))
    return True
```

Readiness must report MySQL explicitly.

Example:

```json
{
  "status": "ready",
  "dependencies": {
    "database": "available",
    "database_type": "mysql",
    "rule_engine": "available"
  }
}
```

---

# 51. Performance Expectations

For the small hackathon dataset:

- Policy list under 500 ms.
- Rule evaluation under 300 ms without AI explanation.
- Database aggregate queries under 1 second.
- Active policy retrieval indexed and ordered.
- No N+1 queries for rule results.
- Batch insert evaluation rule results where practical.

Do not prematurely optimize beyond these targets.

---

# 52. Security Requirements

- Never commit `.env`.
- Never return database credentials.
- Validate all API input.
- Use parameterized SQL through SQLAlchemy.
- Do not execute user-provided expressions.
- Do not use Python `eval`.
- Do not dynamically import operators from user input.
- Restrict operators to the registry.
- Limit page size.
- Do not expose stack traces in API responses.
- Protect database connection failure details.

---

# 53. Explicit Prohibitions

The backend engineer must not:

- Add SQLite fallback.
- Put policy logic inside routers.
- Ask the LLM to choose the final decision.
- Use `eval()` for rule execution.
- Store active AI policies without human activation.
- Return raw ORM objects.
- Change API field names independently.
- Add unnecessary microservices.
- Add Kafka, Redis, Celery, or a vector database.
- Build authentication unless requested.
- Introduce a second source of truth for fields or operators.
- Hardcode secrets.

---

# 54. Development Order

Follow this order to minimize blocking.

## Phase 1: Foundation

1. Create backend structure.
2. Add settings.
3. Configure MySQL.
4. Configure SQLAlchemy.
5. Add models.
6. Add Alembic migrations.
7. Verify database health.

## Phase 2: Shared schemas

1. Common response models.
2. Field catalogue.
3. Operator catalogue.
4. Policy schemas.
5. Evaluation result schemas.

## Phase 3: Rule engine

1. Operator registry.
2. Condition evaluator.
3. Group evaluator.
4. Policy evaluator.
5. Engine result.
6. Priority resolver.
7. Confidence calculator.
8. Unit tests.

## Phase 4: Policy persistence

1. Policy repository.
2. Version repository.
3. Validation service.
4. Policy service.
5. Audit service.
6. Policy routes.
7. Tests.

## Phase 5: Decision persistence and analytics

1. Evaluation repository.
2. Rule-result persistence.
3. Analytics repository.
4. Analytics service.
5. Audit list/detail.
6. Tests.

## Phase 6: Packaging

1. Seed data.
2. Dockerfile.
3. Compose integration.
4. Swagger checks.
5. Handoff notes.

---

# 55. Parallel Work Guidance

The backend engineer should provide the integration lead with early interfaces before the entire module is finished.

## First handoff

Provide:

```python
OPERATORS
PolicyCreate
PolicyResponse
RuleEngine.evaluate
PriorityResolver.resolve
```

## Second handoff

Provide:

```python
PolicyService.get_active_policies
Policy CRUD endpoints
MySQL migrations
Seed data
```

## Third handoff

Provide:

```python
EvaluationRepository
AuditService
AnalyticsService
```

This allows the integration lead to wire the decision endpoint early.

---

# 56. Mock Interfaces During Development

Until MySQL repositories are complete, the backend engineer may use in-memory fixtures for unit-testing the engine only.

However:

- API integration must use MySQL.
- Final demo must use MySQL.
- No in-memory fallback should remain in application startup.

Example engine fixture:

```python
policies = [
    {
        "id": "pol_test",
        "name": "Test approval",
        "version": 1,
        "priority": 100,
        "decision": "APPROVE",
        "conditions": {
            "all": [
                {
                    "field": "credit_score",
                    "operator": "greater_than_or_equal",
                    "value": 750,
                }
            ]
        },
    }
]
```

---

# 57. Backend Definition of Done

The backend module is considered complete only when all of the following are true.

## Database

- MySQL container starts.
- Database is created.
- Migrations succeed.
- Seed succeeds.
- Re-running seed creates no duplicates.

## Policy management

- Create works.
- List works.
- Filter works.
- Detail works.
- Update works.
- Activate works.
- Disable works.
- History is preserved.

## Rule engine

- Supported operators work.
- All/any groups work.
- Nested conditions work.
- Missing fields are traced.
- Multiple rules are resolved.
- No-match fallback is deterministic.
- Confidence is deterministic.

## Persistence

- Evaluations can be saved.
- Rule traces can be saved.
- Audit events can be saved.
- Transactions roll back on failure.

## Analytics

- Summary works.
- Distribution works.
- Trend works.
- Top policies works.

## Quality

- Tests pass.
- Swagger reflects contract.
- Correlation IDs work.
- Standard errors work.
- No secrets are committed.
- No SQLite references remain.

---

# 58. Required Handoff Package

The backend engineer must give the integration lead:

## Code

```text
Branch: feature/backend-rule-engine
Latest commit: <hash>
```

## Setup

```bash
docker compose up -d mysql
cd backend
source .venv/bin/activate
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload
```

## Tests

```bash
pytest -q
```

## Swagger

```text
http://localhost:8000/docs
```

## Required notes

- Completed endpoints
- Incomplete endpoints
- Known limitations
- Database migration status
- Seed status
- Test count
- Example policy ID
- Any breaking concern
- Integration functions and import paths

---

# 59. Handoff Message Template

The backend engineer should send a message in this exact structure.

```text
Backend module handoff

Branch:
feature/backend-rule-engine

Latest commit:
<commit hash>

Completed:
- MySQL models and migrations
- Policy CRUD
- Policy activation and disable
- Rule engine
- Priority resolver
- Confidence calculator
- Audit persistence
- Analytics queries

Run:
1. docker compose up -d mysql
2. cd backend
3. source .venv/bin/activate
4. alembic upgrade head
5. python -m app.db.seed
6. uvicorn app.main:app --reload

Tests:
pytest -q
Result: <passed count>

Integration imports:
- app.services.policy_service.PolicyService
- app.engine.evaluator.RuleEngine
- app.engine.resolver.PriorityResolver
- app.engine.confidence.DecisionConfidenceCalculator
- app.repositories.evaluation_repository.EvaluationRepository
- app.services.audit_service.AuditService

Known limitations:
- <list>

API contract deviations:
- None
```

If there is a contract deviation, it must be highlighted before merge.

---

# 60. Integration Lead Verification Checklist

The integration lead will verify:

1. MySQL startup.
2. Alembic migration.
3. Seed command.
4. Policy APIs.
5. Rule engine with approval case.
6. Rule engine with fraud rejection case.
7. Priority resolution.
8. Missing-field behavior.
9. Evaluation persistence.
10. Audit creation.
11. Analytics response.
12. Swagger contract.
13. Test suite.
14. No secret exposure.
15. No SQLite dependency.

The backend engineer should run these checks before handoff.

---

# 61. Example End-to-End Backend Validation

## Step 1: Start MySQL

```bash
docker compose up -d mysql
```

## Step 2: Run migrations

```bash
cd backend
alembic upgrade head
```

## Step 3: Seed policies

```bash
python -m app.db.seed
```

## Step 4: Start API

```bash
uvicorn app.main:app --reload
```

## Step 5: Verify policy list

```bash
curl http://localhost:8000/api/v1/policies
```

## Step 6: Verify fields

```bash
curl http://localhost:8000/api/v1/config/fields
```

## Step 7: Run engine unit tests

```bash
pytest tests/test_evaluator.py -q
```

## Step 8: Verify audit

```bash
curl http://localhost:8000/api/v1/audit
```

---

# 62. Final Backend Architecture Summary

The backend module should be understood as four layers.

```text
API Layer
    ↓
Service Layer
    ↓
Repository and Rule Engine Layer
    ↓
MySQL
```

Responsibilities must remain separated.

## API layer

- HTTP
- Dependencies
- Request and response models

## Service layer

- Business workflow
- Transactions
- Validation
- Audit calls

## Repository layer

- SQLAlchemy queries
- Persistence

## Rule-engine layer

- Pure deterministic evaluation
- No database access
- No AI calls

The backend module is successful when the integration lead can call stable service and engine interfaces without needing to understand internal database implementation details.

---

# 63. Final Instruction to the Backend Engineer

Build for integration, not only for local correctness.

That means:

- Follow the exact contract.
- Keep interfaces small.
- Keep the engine pure.
- Use MySQL from the beginning.
- Add meaningful tests.
- Return complete traces.
- Document assumptions.
- Hand off early.
- Do not wait until the final hour to merge.

Your module is the deterministic core of DecisionFlow AI. The rest of the product depends on its correctness, stability, and predictability.
