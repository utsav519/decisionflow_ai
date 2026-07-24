---
name: schema-validator
description: Validates Pydantic schemas against the API contract (02_API_CONTRACT) and backend spec (§14-15, §19) to ensure field names, types, enums, and response envelopes match exactly.
---

# Schema Validator Agent

## Purpose
Ensures every Pydantic schema in the backend matches the API contract and backend module guide exactly — field names, types, optional/required, enums, and response envelope structure.

## How to Invoke

### As a User
```
/schema-validator
```
Or target a specific schema file:
```
/schema-validator check backend/app/schemas/policy.py
```

### As Another Agent
```
After creating or modifying any schema file, read and follow:
skills/schema-validator/SKILL.md
```

## Execution Steps

### Step 1: Identify Target Schemas
If no specific file is given, scan all schema files:
```
backend/app/schemas/common.py
backend/app/schemas/policy.py
backend/app/schemas/evaluation.py
backend/app/schemas/analytics.py
backend/app/schemas/audit.py
backend/app/engine/result_models.py
```

### Step 2: Cross-Reference Against Contract
For each schema, verify against:

#### Common Schemas (§14 of backend spec, §6-7 of API contract)
- [ ] `ErrorDetail` has: `path`, `issue`, `received`, `allowed_values`, `suggestion`
- [ ] `ErrorBody` has: `code`, `message`, `details`
- [ ] `PaginationMeta` has: `page`, `page_size`, `total_items`, `total_pages`
- [ ] Success envelope: `success`, `data`, `meta`, `correlation_id`
- [ ] Error envelope: `success`, `error`, `correlation_id`

#### Policy Schemas (§15 of backend spec, §11-18 of API contract)
- [ ] `Condition` has: `field` (str), `operator` (str), `value` (Any | None)
- [ ] `ConditionGroup` has: `all` or `any` (mutually exclusive)
- [ ] `ConditionNode` is union of `Condition | ConditionGroup`
- [ ] `PolicyCreate` has: `name`, `domain`, `priority`, `decision`, `conditions`, `source`
- [ ] `PolicyCreate` does NOT accept: `id`, `version`, `created_at`, `updated_at`, `approved_by`, `activated_at`
- [ ] `PolicyResponse` has all 19 fields from §11.1 of API contract
- [ ] `PolicyListItem` is a lightweight version for list responses
- [ ] Status enum: `DRAFT`, `PENDING_APPROVAL`, `ACTIVE`, `DISABLED`, `ARCHIVED`
- [ ] Decision enum: `APPROVE`, `REJECT`, `MANUAL_REVIEW`
- [ ] Source enum: `AI_GENERATED`, `MANUAL`, `IMPORTED`, `SEEDED`
- [ ] `AIMetadata` has: `generated`, `ai_confidence`, `warnings`, `ambiguities`, `model`

#### Evaluation Schemas (§19 of backend spec)
- [ ] `ConditionResult` has: `field`, `operator`, `expected`, `actual`, `matched`, `status`, `reason`
- [ ] Status values: `MATCHED`, `UNMATCHED`, `MISSING_FIELD`, `INVALID_VALUE`, `ERROR`
- [ ] `PolicyEvaluationResult` has all required fields
- [ ] `EngineEvaluationResult` separates matched/unmatched/skipped
- [ ] `ResolutionResult` has: `decision`, `winning_policy`, `strategy`, `reason`, `tie_breaker_used`, `competing_policy_ids`
- [ ] `DecisionConfidenceResult` has: `score` (int 0-100), `factors` (list)

### Step 3: Validate Pydantic v2 Usage
- [ ] Uses `BaseModel` from pydantic, not pydantic v1
- [ ] Uses `model_config` instead of `class Config`
- [ ] Uses `model_validator` instead of `@validator` where needed
- [ ] Uses `Field()` with proper constraints
- [ ] Recursive models use proper forward references

### Step 4: Report Compliance
Generate a compliance matrix:

```
Schema File                      | Fields OK | Types OK | Enums OK | Overall
---------------------------------|-----------|----------|----------|---------
schemas/common.py                | ✅         | ✅        | N/A      | PASS
schemas/policy.py                | ⚠️ missing | ✅        | ✅        | WARN
schemas/evaluation.py            | ❌         | ❌        | N/A      | FAIL
engine/result_models.py          | ✅         | ✅        | ✅        | PASS
```

### Step 5: Generate Fix Suggestions
For each deviation, provide:
1. What the contract says
2. What the code currently has
3. The exact code change needed
4. Wait for approval before applying

## Key Contract References
- API Contract: `backend/02_API_CONTRACT(1).md` sections 6, 7, 9, 10, 11
- Backend Spec: `backend/03_BACKEND_MODULE_GUIDE.md` sections 14, 15, 19
