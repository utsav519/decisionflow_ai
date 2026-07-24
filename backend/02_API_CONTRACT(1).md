# DecisionFlow AI
## API Contract and Integration Specification

**Document ID:** DFA-API-002  
**Version:** 1.1  
**Status:** Hackathon POC Baseline — MySQL Edition  
**API Base Path:** `/api/v1`  
**Primary Owner:** Technical Architect and Integration Lead  
**Consumers:** Frontend, Backend Services, AI Module, Integration Layer, Test Suite

---

# 1. Purpose

This document is the shared API contract for all four team members working on DecisionFlow AI.

Its purpose is to ensure that:

- The frontend can be developed using mock responses before the backend is complete.
- The backend engineer knows the exact routes, request bodies, response bodies, and status codes to implement.
- The AI engineer knows the exact input and output format expected from AI-related endpoints.
- The integration lead can connect all modules without changing interface definitions late in the project.
- Unit tests, integration tests, and demo scenarios use the same contract.
- Every module can be developed independently while remaining compatible.

This contract should be treated as the single source of truth for all API communication.

---

# 2. Core API Principles

## 2.1 API-first development

No frontend component, backend service, or AI module should invent its own payload shape.

All payloads must follow this contract.

## 2.2 Versioned routes

All public routes use:

```text
/api/v1
```

Example:

```text
POST /api/v1/decisions/evaluate
```

## 2.3 JSON communication

All request and response bodies use:

```http
Content-Type: application/json
```

## 2.4 Stable response envelope

Success responses use:

```json
{
  "success": true,
  "data": {},
  "meta": {},
  "correlation_id": "cor_01J123ABC"
}
```

Error responses use:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request could not be processed.",
    "details": []
  },
  "correlation_id": "cor_01J123ABC"
}
```

## 2.5 Correlation ID

Every request should carry or receive a correlation ID.

Recommended request header:

```http
X-Correlation-ID: cor_01J123ABC
```

If the frontend does not send one, the backend generates it.

The same correlation ID should appear in:

- API response
- Application logs
- Evaluation records
- Audit records
- AI logs where applicable

## 2.6 Deterministic decisioning

The LLM must not return the final business decision.

The final decision is returned only by the deterministic rule engine.

## 2.7 Human approval before activation

An AI-generated policy may be saved as `DRAFT`, but it cannot become `ACTIVE` without an explicit activation request.

---

# 3. Base URL and Environment Convention

## Local development

Backend:

```text
http://localhost:8000
```

Frontend:

```text
http://localhost:5173
```

Full example endpoint:

```text
http://localhost:8000/api/v1/policies
```

## Environment variable

Frontend should use:

```text
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Backend should expose:

```text
API_V1_PREFIX=/api/v1
```

---

# 4. Common Headers

## Request headers

| Header | Required | Description |
|---|---:|---|
| `Content-Type` | Yes for POST/PUT | Must be `application/json` |
| `Accept` | Recommended | `application/json` |
| `X-Correlation-ID` | Optional | Client-provided request trace ID |
| `X-User-ID` | Optional for POC | Simulated user identity |
| `X-User-Role` | Optional for POC | Simulated role such as `POLICY_MANAGER` |

## Response headers

| Header | Description |
|---|---|
| `X-Correlation-ID` | Correlation ID used for request |
| `Content-Type` | `application/json` |

---

# 5. Standard Data Types

## 5.1 Identifiers

Identifiers are strings.

Examples:

```text
pol_01J123ABC
eval_01J123XYZ
aud_01J123LMN
ver_01J123PQR
```

The backend may internally use UUIDs, but APIs should expose string IDs.

## 5.2 Timestamps

All timestamps use ISO 8601 UTC format.

Example:

```text
2026-07-24T08:45:32.120Z
```

## 5.3 Percentages and scores

Confidence scores use integers from `0` to `100`.

Example:

```json
{
  "ai_confidence": 94,
  "decision_confidence": 88
}
```

## 5.4 Monetary values

POC monetary values use numeric fields without currency conversion.

Example:

```json
{
  "monthly_bill_amount": 3200.0,
  "requested_device_price": 85000.0
}
```

A currency field may be included if needed:

```json
{
  "currency": "INR"
}
```

## 5.5 Enumerations

### Policy status

```text
DRAFT
PENDING_APPROVAL
ACTIVE
DISABLED
ARCHIVED
```

### Decision outcome

```text
APPROVE
REJECT
MANUAL_REVIEW
NO_MATCH
```

`NO_MATCH` is an internal or API outcome when no policy matches and no fallback policy exists.

### Policy source

```text
AI_GENERATED
MANUAL
IMPORTED
SEEDED
```

### Condition group type

```text
all
any
```

### Audit action

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

---

# 6. Standard Success Response

## Single object

```json
{
  "success": true,
  "data": {
    "id": "pol_01J123ABC"
  },
  "meta": {},
  "correlation_id": "cor_01J123ABC"
}
```

## List response

```json
{
  "success": true,
  "data": [
    {
      "id": "pol_01J123ABC"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_items": 1,
    "total_pages": 1
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 7. Standard Error Response

```json
{
  "success": false,
  "error": {
    "code": "POLICY_VALIDATION_ERROR",
    "message": "The policy contains invalid conditions.",
    "details": [
      {
        "path": "conditions.all[1].field",
        "issue": "Unsupported field",
        "received": "customer_loyalty",
        "allowed_values": [
          "customer_tenure_months",
          "credit_score",
          "payment_defaults"
        ]
      }
    ]
  },
  "correlation_id": "cor_01J123ABC"
}
```

## Error detail object

| Field | Type | Description |
|---|---|---|
| `path` | string | Location of invalid field |
| `issue` | string | Human-readable issue |
| `received` | any | Received value |
| `allowed_values` | array, optional | Valid alternatives |
| `suggestion` | string, optional | Correction guidance |

---

# 8. HTTP Status Code Rules

| Status | Use |
|---:|---|
| `200 OK` | Successful GET, PUT, activation, disable, evaluation |
| `201 Created` | Policy or resource created |
| `202 Accepted` | Optional asynchronous processing |
| `204 No Content` | Optional delete response |
| `400 Bad Request` | Malformed request or invalid business payload |
| `404 Not Found` | Resource does not exist |
| `409 Conflict` | Policy conflict, invalid state transition, duplicate name |
| `422 Unprocessable Entity` | Pydantic/schema validation failure |
| `500 Internal Server Error` | Unexpected backend failure |
| `502 Bad Gateway` | AI provider failed or returned invalid upstream response |
| `503 Service Unavailable` | AI provider unavailable or dependency unavailable |

For simplicity, the POC may return a JSON body for all errors including `422`.

---

# 9. Shared Domain Field Catalogue

## Endpoint

```http
GET /api/v1/config/fields
```

## Purpose

Returns the supported telecom fields so the frontend and AI module use the same allow-list.

## Response

```json
{
  "success": true,
  "data": [
    {
      "name": "customer_tenure_months",
      "label": "Customer Tenure",
      "description": "Number of months the customer has been active.",
      "type": "integer",
      "required_for_evaluation": false,
      "supported_operators": [
        "equals",
        "not_equals",
        "greater_than",
        "greater_than_or_equal",
        "less_than",
        "less_than_or_equal",
        "in",
        "not_in"
      ],
      "example": 24
    },
    {
      "name": "fraud_risk_score",
      "label": "Fraud Risk Score",
      "description": "Risk score between 0 and 1.",
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "supported_operators": [
        "equals",
        "not_equals",
        "greater_than",
        "greater_than_or_equal",
        "less_than",
        "less_than_or_equal"
      ],
      "example": 0.42
    }
  ],
  "meta": {
    "domain": "telecom",
    "version": "1.0"
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 10. Shared Operator Catalogue

## Endpoint

```http
GET /api/v1/config/operators
```

## Response

```json
{
  "success": true,
  "data": [
    {
      "name": "equals",
      "label": "Equals",
      "value_required": true,
      "supported_types": [
        "string",
        "integer",
        "number",
        "boolean"
      ]
    },
    {
      "name": "in",
      "label": "In list",
      "value_required": true,
      "supported_types": [
        "string",
        "integer",
        "number"
      ],
      "value_shape": "array"
    },
    {
      "name": "is_empty",
      "label": "Is empty",
      "value_required": false,
      "supported_types": [
        "string",
        "array"
      ]
    }
  ],
  "meta": {},
  "correlation_id": "cor_01J123ABC"
}
```

---

# 11. Policy Resource Schema

## 11.1 Policy response object

```json
{
  "id": "pol_01J123ABC",
  "name": "Premium device upgrade eligibility",
  "description": "Approves low-risk premium device upgrades.",
  "domain": "telecom",
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
  "version": 1,
  "ai_metadata": {
    "generated": true,
    "ai_confidence": 94,
    "warnings": [],
    "ambiguities": [],
    "model": "configured-provider-model"
  },
  "created_by": "user_001",
  "approved_by": "user_001",
  "created_at": "2026-07-24T08:45:32.120Z",
  "updated_at": "2026-07-24T08:50:02.110Z",
  "activated_at": "2026-07-24T08:50:02.110Z"
}
```

## 11.2 Condition object

```json
{
  "field": "credit_score",
  "operator": "greater_than_or_equal",
  "value": 750
}
```

## 11.3 Condition group object

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

## 11.4 Policy validation rules

- `name` is required.
- `name` length: 3 to 120 characters.
- `description` length: maximum 1000 characters.
- `domain` must be `telecom` for the POC.
- `priority` must be between 1 and 1000.
- `decision` must be one of `APPROVE`, `REJECT`, `MANUAL_REVIEW`.
- `conditions` must contain exactly one root key: `all` or `any`.
- Each condition group must contain at least one child.
- Maximum nested group depth for MVP: 2.
- Every field must exist in the field catalogue.
- Every operator must exist in the operator catalogue.
- Value type must match field type and operator requirements.
- `status` cannot be set to `ACTIVE` during initial creation unless using activation endpoint.
- `version` is server-managed.
- `created_at`, `updated_at`, `approved_by`, and `activated_at` are server-managed.

---

# 12. Create Policy

## Endpoint

```http
POST /api/v1/policies
```

## Responsibility

Backend and Policy Service.

## Use cases

- Save manually created policy.
- Save AI-generated policy as a draft.
- Persist an edited generated policy.

## Request

```json
{
  "name": "Premium device upgrade eligibility",
  "description": "Approves low-risk premium device upgrades.",
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
  "reason": "Customer satisfies core upgrade requirements.",
  "source": "AI_GENERATED",
  "ai_metadata": {
    "generated": true,
    "ai_confidence": 94,
    "warnings": [],
    "ambiguities": [],
    "model": "configured-provider-model"
  }
}
```

## Success response

**Status:** `201 Created`

```json
{
  "success": true,
  "data": {
    "id": "pol_01J123ABC",
    "name": "Premium device upgrade eligibility",
    "description": "Approves low-risk premium device upgrades.",
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
    "reason": "Customer satisfies core upgrade requirements.",
    "source": "AI_GENERATED",
    "version": 1,
    "created_by": "user_001",
    "created_at": "2026-07-24T08:45:32.120Z",
    "updated_at": "2026-07-24T08:45:32.120Z"
  },
  "meta": {
    "validation_status": "PASSED",
    "conflict_count": 0
  },
  "correlation_id": "cor_01J123ABC"
}
```

## Possible errors

### Duplicate policy name

**Status:** `409 Conflict`

```json
{
  "success": false,
  "error": {
    "code": "DUPLICATE_POLICY_NAME",
    "message": "A policy with this name already exists.",
    "details": [
      {
        "path": "name",
        "issue": "Duplicate name",
        "received": "Premium device upgrade eligibility"
      }
    ]
  },
  "correlation_id": "cor_01J123ABC"
}
```

### Unsupported field

**Status:** `400 Bad Request`

```json
{
  "success": false,
  "error": {
    "code": "POLICY_VALIDATION_ERROR",
    "message": "The policy contains unsupported fields.",
    "details": [
      {
        "path": "conditions.all[0].field",
        "issue": "Unsupported field",
        "received": "customer_loyalty"
      }
    ]
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 13. List Policies

## Endpoint

```http
GET /api/v1/policies
```

## Query parameters

| Parameter | Type | Required | Example |
|---|---|---:|---|
| `page` | integer | No | `1` |
| `page_size` | integer | No | `20` |
| `status` | string | No | `ACTIVE` |
| `decision` | string | No | `REJECT` |
| `source` | string | No | `AI_GENERATED` |
| `search` | string | No | `upgrade` |
| `sort_by` | string | No | `updated_at` |
| `sort_order` | string | No | `desc` |

## Request example

```text
GET /api/v1/policies?page=1&page_size=20&status=ACTIVE&sort_by=priority&sort_order=desc
```

## Success response

```json
{
  "success": true,
  "data": [
    {
      "id": "pol_01J123ABC",
      "name": "Fraud rejection",
      "description": "Rejects requests with extreme fraud risk.",
      "domain": "telecom",
      "status": "ACTIVE",
      "priority": 300,
      "decision": "REJECT",
      "source": "SEEDED",
      "version": 1,
      "created_at": "2026-07-24T08:40:00.000Z",
      "updated_at": "2026-07-24T08:42:00.000Z"
    },
    {
      "id": "pol_01J123DEF",
      "name": "Premium device upgrade eligibility",
      "description": "Approves low-risk premium upgrades.",
      "domain": "telecom",
      "status": "ACTIVE",
      "priority": 100,
      "decision": "APPROVE",
      "source": "AI_GENERATED",
      "version": 1,
      "created_at": "2026-07-24T08:45:32.120Z",
      "updated_at": "2026-07-24T08:50:02.110Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_items": 2,
    "total_pages": 1
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 14. Get Policy by ID

## Endpoint

```http
GET /api/v1/policies/{policy_id}
```

## Success response

Returns the complete policy object.

## Not found response

**Status:** `404 Not Found`

```json
{
  "success": false,
  "error": {
    "code": "POLICY_NOT_FOUND",
    "message": "The requested policy does not exist.",
    "details": [
      {
        "path": "policy_id",
        "issue": "Unknown identifier",
        "received": "pol_missing"
      }
    ]
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 15. Update Policy

## Endpoint

```http
PUT /api/v1/policies/{policy_id}
```

## State rules

- `DRAFT` policies may be edited directly.
- `ACTIVE` policies should create a new version and return the updated version.
- `ARCHIVED` policies should not be editable.
- Updating an active policy should not silently overwrite history.

## Request

```json
{
  "name": "Premium device upgrade eligibility",
  "description": "Updated premium-device policy.",
  "priority": 110,
  "decision": "APPROVE",
  "conditions": {
    "all": [
      {
        "field": "customer_tenure_months",
        "operator": "greater_than_or_equal",
        "value": 18
      },
      {
        "field": "customer_segment",
        "operator": "equals",
        "value": "PREMIUM"
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
  },
  "reason": "Premium customers qualify earlier when credit and fraud thresholds are met."
}
```

## Success response

```json
{
  "success": true,
  "data": {
    "id": "pol_01J123ABC",
    "name": "Premium device upgrade eligibility",
    "status": "DRAFT",
    "priority": 110,
    "decision": "APPROVE",
    "version": 2,
    "updated_at": "2026-07-24T09:15:00.000Z"
  },
  "meta": {
    "previous_version": 1,
    "new_version": 2,
    "requires_activation": true
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 16. Delete Policy

## Endpoint

```http
DELETE /api/v1/policies/{policy_id}
```

## POC behavior

Recommended behavior:

- Draft policy: hard delete is allowed.
- Active policy: do not hard delete; mark as archived.
- Disabled policy: archive.

## Success response

```json
{
  "success": true,
  "data": {
    "id": "pol_01J123ABC",
    "status": "ARCHIVED",
    "deleted": true
  },
  "meta": {},
  "correlation_id": "cor_01J123ABC"
}
```

---

# 17. Activate Policy

## Endpoint

```http
POST /api/v1/policies/{policy_id}/activate
```

## Request

```json
{
  "approval_comment": "Reviewed and approved for the demo environment."
}
```

## Preconditions

- Policy exists.
- Policy status is `DRAFT`, `PENDING_APPROVAL`, or `DISABLED`.
- Policy passes schema and semantic validation.
- No unresolved blocking conflicts exist.
- AI ambiguity list is empty or user explicitly acknowledges it.

## Success response

```json
{
  "success": true,
  "data": {
    "id": "pol_01J123ABC",
    "status": "ACTIVE",
    "version": 1,
    "approved_by": "user_001",
    "activated_at": "2026-07-24T09:20:00.000Z"
  },
  "meta": {
    "validation_status": "PASSED",
    "blocking_conflicts": 0,
    "warnings": []
  },
  "correlation_id": "cor_01J123ABC"
}
```

## Conflict response

**Status:** `409 Conflict`

```json
{
  "success": false,
  "error": {
    "code": "POLICY_ACTIVATION_BLOCKED",
    "message": "The policy cannot be activated because blocking conflicts exist.",
    "details": [
      {
        "path": "policy",
        "issue": "Conflicting active rule",
        "conflicting_policy_id": "pol_01J999XYZ",
        "conflict_type": "OVERLAPPING_RANGE_DIFFERENT_OUTCOME",
        "suggestion": "Change the priority or adjust the score threshold."
      }
    ]
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 18. Disable Policy

## Endpoint

```http
POST /api/v1/policies/{policy_id}/disable
```

## Request

```json
{
  "reason": "Temporarily disabled for policy review."
}
```

## Success response

```json
{
  "success": true,
  "data": {
    "id": "pol_01J123ABC",
    "status": "DISABLED",
    "updated_at": "2026-07-24T09:25:00.000Z"
  },
  "meta": {},
  "correlation_id": "cor_01J123ABC"
}
```

---

# 19. AI Policy Generation

## Endpoint

```http
POST /api/v1/ai/policies/generate
```

## Responsibility

AI Engineer implements the AI pipeline.  
Integration Lead exposes it through FastAPI.

## Purpose

Converts a natural-language policy into a structured rule candidate.

## Request

```json
{
  "policy_text": "Approve premium device upgrades for customers with at least 24 months tenure, no payment defaults, credit score at least 750, and fraud risk below 0.6.",
  "domain": "telecom",
  "preferred_decision": "APPROVE",
  "preferred_priority": 100,
  "generate_test_cases": true
}
```

## Validation

- `policy_text` required.
- Minimum length: 10 characters.
- Maximum length: 5000 characters.
- `domain` must be supported.
- Preferred decision is optional.
- Preferred priority must be from 1 to 1000.

## Success response

```json
{
  "success": true,
  "data": {
    "generated_policy": {
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
      "reason": "Customer satisfies tenure, payment, credit, and fraud-risk requirements.",
      "source": "AI_GENERATED"
    },
    "ai_confidence": 95,
    "validation": {
      "status": "PASSED",
      "errors": [],
      "warnings": []
    },
    "ambiguities": [],
    "assumptions": [
      "The term 'no payment defaults' was mapped to payment_defaults equals 0."
    ],
    "conflicts": [],
    "suggested_test_cases": [
      {
        "name": "Eligible customer",
        "expected_decision": "APPROVE",
        "input": {
          "customer_tenure_months": 30,
          "payment_defaults": 0,
          "credit_score": 780,
          "fraud_risk_score": 0.2
        }
      },
      {
        "name": "Boundary credit score",
        "expected_decision": "APPROVE",
        "input": {
          "customer_tenure_months": 24,
          "payment_defaults": 0,
          "credit_score": 750,
          "fraud_risk_score": 0.59
        }
      },
      {
        "name": "Fraud threshold failure",
        "expected_decision": "NO_MATCH",
        "input": {
          "customer_tenure_months": 36,
          "payment_defaults": 0,
          "credit_score": 800,
          "fraud_risk_score": 0.7
        }
      }
    ]
  },
  "meta": {
    "provider": "configured-provider",
    "model": "configured-model",
    "processing_time_ms": 1450,
    "fallback_used": false
  },
  "correlation_id": "cor_01J123ABC"
}
```

## Ambiguous response

The endpoint may still return `200 OK` because the AI successfully analyzed the request, even though it could not safely generate an activatable policy.

```json
{
  "success": true,
  "data": {
    "generated_policy": null,
    "ai_confidence": 35,
    "validation": {
      "status": "NEEDS_CLARIFICATION",
      "errors": [],
      "warnings": [
        {
          "code": "AMBIGUOUS_TERM",
          "message": "The term 'loyal customer' is not measurable."
        }
      ]
    },
    "ambiguities": [
      {
        "term": "loyal customer",
        "question": "How should loyalty be measured?",
        "suggested_fields": [
          "customer_tenure_months",
          "monthly_bill_amount",
          "customer_segment"
        ]
      }
    ],
    "assumptions": [],
    "conflicts": [],
    "suggested_test_cases": []
  },
  "meta": {
    "provider": "configured-provider",
    "model": "configured-model",
    "processing_time_ms": 1020,
    "fallback_used": false
  },
  "correlation_id": "cor_01J123ABC"
}
```

## Invalid AI output

**Status:** `502 Bad Gateway`

```json
{
  "success": false,
  "error": {
    "code": "AI_OUTPUT_INVALID",
    "message": "The AI provider returned an invalid policy structure.",
    "details": [
      {
        "path": "generated_policy.conditions",
        "issue": "Missing root condition group"
      }
    ]
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 20. Clarify AI Policy

Optional but recommended.

## Endpoint

```http
POST /api/v1/ai/policies/clarify
```

## Request

```json
{
  "original_policy_text": "Approve loyal customers.",
  "clarifications": {
    "loyal_customer_definition": "Customer tenure must be at least 24 months."
  },
  "domain": "telecom"
}
```

## Response

Same response shape as AI policy generation.

---

# 21. Policy Conflict Check

## Endpoint

```http
POST /api/v1/ai/policies/check-conflicts
```

## Important design rule

Despite the `/ai` route grouping, the backend should first run deterministic conflict checks. AI may then explain the conflict in natural language.

## Request

```json
{
  "candidate_policy": {
    "name": "Credit approval rule",
    "domain": "telecom",
    "priority": 100,
    "decision": "APPROVE",
    "conditions": {
      "all": [
        {
          "field": "credit_score",
          "operator": "greater_than_or_equal",
          "value": 700
        }
      ]
    }
  },
  "include_disabled_policies": false
}
```

## Success response

```json
{
  "success": true,
  "data": {
    "has_conflicts": true,
    "blocking_conflict_count": 1,
    "warning_count": 0,
    "conflicts": [
      {
        "conflict_id": "conf_01J123ABC",
        "candidate_policy_name": "Credit approval rule",
        "existing_policy_id": "pol_01J999XYZ",
        "existing_policy_name": "Credit rejection rule",
        "conflict_type": "OVERLAPPING_RANGE_DIFFERENT_OUTCOME",
        "severity": "BLOCKING",
        "fields": [
          "credit_score"
        ],
        "deterministic_reason": "Candidate approves credit score >= 700 while active policy rejects credit score < 750. Values from 700 to 749 satisfy both.",
        "ai_explanation": "The two policies overlap for customers whose credit score is between 700 and 749. Assign different priorities or adjust the thresholds.",
        "suggestions": [
          "Increase approval threshold to 750.",
          "Lower the rejection upper range to below 700.",
          "Assign explicit priority if the overlap is intentional."
        ]
      }
    ]
  },
  "meta": {
    "policies_compared": 5,
    "processing_time_ms": 75,
    "ai_explanation_used": true
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 22. Generate Policy Test Cases

## Endpoint

```http
POST /api/v1/ai/policies/generate-tests
```

## Request

```json
{
  "policy": {
    "name": "Premium approval",
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
        }
      ]
    }
  },
  "count": 5
}
```

## Response

```json
{
  "success": true,
  "data": {
    "test_cases": [
      {
        "name": "Positive case",
        "category": "POSITIVE",
        "input": {
          "customer_tenure_months": 30,
          "credit_score": 790
        },
        "expected_match": true,
        "expected_decision": "APPROVE"
      },
      {
        "name": "Boundary case",
        "category": "BOUNDARY",
        "input": {
          "customer_tenure_months": 24,
          "credit_score": 750
        },
        "expected_match": true,
        "expected_decision": "APPROVE"
      },
      {
        "name": "Negative tenure case",
        "category": "NEGATIVE",
        "input": {
          "customer_tenure_months": 23,
          "credit_score": 780
        },
        "expected_match": false,
        "expected_decision": "NO_MATCH"
      }
    ]
  },
  "meta": {
    "generated_count": 3
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 23. Decision Evaluation Request Schema

## Customer decision request

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

## Validation rules

- `domain` required.
- `customer.customer_id` recommended.
- At least one evaluable customer field required.
- Numeric fields must use numeric values.
- `fraud_risk_score` must be from 0 to 1.
- `credit_score` recommended range: 300 to 900.
- `payment_defaults` cannot be negative.
- Monetary fields cannot be negative.
- Unknown fields may be ignored or rejected depending on backend setting; recommended behavior is reject with detail.
- Missing fields should not crash the engine.
- Policies requiring missing fields should be marked `SKIPPED_MISSING_FIELD`.

---

# 24. Evaluate Decision

## Endpoint

```http
POST /api/v1/decisions/evaluate
```

## Responsibility

Integration Lead owns the orchestration endpoint.  
Backend Engineer provides policy loading and rule engine.  
AI Engineer provides optional explanation.

## Processing sequence

```text
Validate request
→ Load active policies
→ Evaluate each policy
→ Resolve outcome
→ Calculate decision confidence
→ Generate explanation
→ Save evaluation
→ Save audit
→ Return response
```

## Success response

```json
{
  "success": true,
  "data": {
    "evaluation_id": "eval_01J123ABC",
    "request_id": "req_1001",
    "decision": "APPROVE",
    "decision_confidence": 96,
    "winning_policy": {
      "id": "pol_01J123DEF",
      "name": "Premium device upgrade eligibility",
      "priority": 100,
      "decision": "APPROVE",
      "version": 1
    },
    "matched_policies": [
      {
        "policy_id": "pol_01J123DEF",
        "policy_name": "Premium device upgrade eligibility",
        "priority": 100,
        "decision": "APPROVE",
        "matched": true,
        "condition_results": [
          {
            "field": "customer_tenure_months",
            "operator": "greater_than_or_equal",
            "expected": 24,
            "actual": 36,
            "matched": true
          },
          {
            "field": "payment_defaults",
            "operator": "equals",
            "expected": 0,
            "actual": 0,
            "matched": true
          },
          {
            "field": "credit_score",
            "operator": "greater_than_or_equal",
            "expected": 750,
            "actual": 790,
            "matched": true
          },
          {
            "field": "fraud_risk_score",
            "operator": "less_than",
            "expected": 0.6,
            "actual": 0.12,
            "matched": true
          }
        ]
      }
    ],
    "unmatched_policies": [
      {
        "policy_id": "pol_01J999XYZ",
        "policy_name": "Fraud rejection",
        "priority": 300,
        "decision": "REJECT",
        "matched": false,
        "condition_results": [
          {
            "field": "fraud_risk_score",
            "operator": "greater_than_or_equal",
            "expected": 0.85,
            "actual": 0.12,
            "matched": false
          }
        ]
      }
    ],
    "skipped_policies": [],
    "explanation": {
      "summary": "The request was approved because the customer satisfied the tenure, credit, payment-history, and fraud-risk requirements.",
      "generated_by": "AI",
      "fallback_used": false
    },
    "metrics": {
      "policies_loaded": 5,
      "policies_evaluated": 5,
      "policies_matched": 1,
      "policies_skipped": 0,
      "condition_count": 9,
      "conflicts_detected": 0,
      "engine_latency_ms": 18,
      "explanation_latency_ms": 620,
      "total_latency_ms": 652
    },
    "warnings": [],
    "evaluated_at": "2026-07-24T09:40:00.000Z"
  },
  "meta": {
    "domain": "telecom",
    "engine_version": "1.0.0",
    "explanation_enabled": true
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 25. Decision Response When Multiple Policies Match

Example:

- Fraud rejection priority 300
- Premium approval priority 100

Both match.

The response must clearly show why rejection won.

```json
{
  "success": true,
  "data": {
    "evaluation_id": "eval_01J123XYZ",
    "decision": "REJECT",
    "decision_confidence": 92,
    "winning_policy": {
      "id": "pol_fraud_001",
      "name": "Fraud rejection",
      "priority": 300,
      "decision": "REJECT",
      "version": 1
    },
    "matched_policies": [
      {
        "policy_id": "pol_fraud_001",
        "policy_name": "Fraud rejection",
        "priority": 300,
        "decision": "REJECT",
        "matched": true
      },
      {
        "policy_id": "pol_upgrade_001",
        "policy_name": "Premium device upgrade eligibility",
        "priority": 100,
        "decision": "APPROVE",
        "matched": true
      }
    ],
    "resolution": {
      "strategy": "HIGHEST_PRIORITY",
      "reason": "Fraud rejection had priority 300, which is higher than approval priority 100.",
      "tie_breaker_used": false
    },
    "explanation": {
      "summary": "The request was rejected because the fraud-risk policy had the highest priority. Although the customer met the upgrade criteria, the fraud-risk rule overrides approval rules.",
      "generated_by": "AI",
      "fallback_used": false
    },
    "metrics": {
      "policies_loaded": 5,
      "policies_evaluated": 5,
      "policies_matched": 2,
      "conflicts_detected": 1,
      "engine_latency_ms": 20,
      "explanation_latency_ms": 580,
      "total_latency_ms": 615
    }
  },
  "meta": {},
  "correlation_id": "cor_01J123ABC"
}
```

---

# 26. Decision Response With Missing Fields

If policies cannot be evaluated because required fields are absent:

```json
{
  "success": true,
  "data": {
    "evaluation_id": "eval_01J123MISS",
    "decision": "MANUAL_REVIEW",
    "decision_confidence": 55,
    "winning_policy": null,
    "matched_policies": [],
    "unmatched_policies": [],
    "skipped_policies": [
      {
        "policy_id": "pol_01J123DEF",
        "policy_name": "Premium device upgrade eligibility",
        "reason": "SKIPPED_MISSING_FIELD",
        "missing_fields": [
          "credit_score",
          "fraud_risk_score"
        ]
      }
    ],
    "explanation": {
      "summary": "The request requires manual review because required customer information is missing.",
      "generated_by": "DETERMINISTIC_FALLBACK",
      "fallback_used": true
    },
    "warnings": [
      {
        "code": "MISSING_REQUIRED_FIELDS",
        "message": "Some policies could not be evaluated.",
        "fields": [
          "credit_score",
          "fraud_risk_score"
        ]
      }
    ]
  },
  "meta": {},
  "correlation_id": "cor_01J123ABC"
}
```

---

# 27. Decision Fallback Rule

Recommended POC configuration:

```text
If no active policy matches:
Decision = MANUAL_REVIEW
Reason = No active policy fully matched the request.
```

This avoids silently approving or rejecting an unmatched request.

---

# 28. List Decisions

## Endpoint

```http
GET /api/v1/decisions
```

## Query parameters

| Parameter | Type | Example |
|---|---|---|
| `page` | integer | `1` |
| `page_size` | integer | `20` |
| `decision` | string | `REJECT` |
| `customer_id` | string | `CUST-1001` |
| `from_date` | timestamp/date | `2026-07-24` |
| `to_date` | timestamp/date | `2026-07-25` |
| `policy_id` | string | `pol_01J123ABC` |
| `min_confidence` | integer | `80` |

## Response

```json
{
  "success": true,
  "data": [
    {
      "evaluation_id": "eval_01J123ABC",
      "request_id": "req_1001",
      "customer_id": "CUST-1001",
      "decision": "APPROVE",
      "decision_confidence": 96,
      "winning_policy_name": "Premium device upgrade eligibility",
      "total_latency_ms": 652,
      "evaluated_at": "2026-07-24T09:40:00.000Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_items": 1,
    "total_pages": 1
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 29. Get Decision by ID

## Endpoint

```http
GET /api/v1/decisions/{evaluation_id}
```

Returns the full evaluation response including:

- Request payload
- Final decision
- Matched policies
- Unmatched policies
- Skipped policies
- Condition trace
- Confidence
- Explanation
- Metrics
- Timestamps

---

# 30. Regenerate Decision Explanation

Optional endpoint.

## Endpoint

```http
POST /api/v1/decisions/{evaluation_id}/explanation
```

## Request

```json
{
  "style": "BUSINESS",
  "max_length": 500
}
```

Supported styles:

```text
BUSINESS
TECHNICAL
CUSTOMER_FRIENDLY
AUDIT
```

## Response

```json
{
  "success": true,
  "data": {
    "evaluation_id": "eval_01J123ABC",
    "style": "BUSINESS",
    "explanation": "The upgrade was approved because the customer exceeded the required tenure and credit thresholds, had no payment defaults, and remained below the permitted fraud-risk threshold.",
    "generated_by": "AI",
    "fallback_used": false
  },
  "meta": {
    "processing_time_ms": 540
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 31. Analytics Summary

## Endpoint

```http
GET /api/v1/analytics/summary
```

## Query parameters

| Parameter | Example |
|---|---|
| `from_date` | `2026-07-24` |
| `to_date` | `2026-07-25` |
| `domain` | `telecom` |

## Response

```json
{
  "success": true,
  "data": {
    "policies": {
      "total": 12,
      "active": 7,
      "draft": 3,
      "pending_approval": 1,
      "disabled": 1,
      "ai_generated": 8
    },
    "decisions": {
      "total": 1250,
      "approve": 825,
      "reject": 250,
      "manual_review": 175,
      "approval_rate": 66.0,
      "rejection_rate": 20.0,
      "manual_review_rate": 14.0
    },
    "performance": {
      "average_decision_confidence": 89,
      "average_engine_latency_ms": 22,
      "average_total_latency_ms": 615,
      "p95_total_latency_ms": 920
    },
    "quality": {
      "validation_errors": 6,
      "conflicts_detected": 4,
      "ai_fallback_count": 3
    }
  },
  "meta": {
    "from_date": "2026-07-24",
    "to_date": "2026-07-25"
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 32. Decision Distribution

## Endpoint

```http
GET /api/v1/analytics/decision-distribution
```

## Response

```json
{
  "success": true,
  "data": [
    {
      "decision": "APPROVE",
      "count": 825,
      "percentage": 66.0
    },
    {
      "decision": "REJECT",
      "count": 250,
      "percentage": 20.0
    },
    {
      "decision": "MANUAL_REVIEW",
      "count": 175,
      "percentage": 14.0
    }
  ],
  "meta": {},
  "correlation_id": "cor_01J123ABC"
}
```

---

# 33. Decision Trend

## Endpoint

```http
GET /api/v1/analytics/decision-trend
```

## Query parameters

```text
granularity=hour|day|week
```

## Response

```json
{
  "success": true,
  "data": [
    {
      "period": "2026-07-24T08:00:00Z",
      "approve": 42,
      "reject": 11,
      "manual_review": 7
    },
    {
      "period": "2026-07-24T09:00:00Z",
      "approve": 55,
      "reject": 14,
      "manual_review": 8
    }
  ],
  "meta": {
    "granularity": "hour"
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 34. Top Triggered Policies

## Endpoint

```http
GET /api/v1/analytics/top-policies
```

## Query parameters

```text
limit=5
```

## Response

```json
{
  "success": true,
  "data": [
    {
      "policy_id": "pol_fraud_001",
      "policy_name": "Fraud rejection",
      "decision": "REJECT",
      "trigger_count": 245,
      "match_rate": 19.6
    },
    {
      "policy_id": "pol_upgrade_001",
      "policy_name": "Premium device upgrade eligibility",
      "decision": "APPROVE",
      "trigger_count": 812,
      "match_rate": 64.9
    }
  ],
  "meta": {},
  "correlation_id": "cor_01J123ABC"
}
```

---

# 35. Audit List

## Endpoint

```http
GET /api/v1/audit
```

## Query parameters

| Parameter | Example |
|---|---|
| `page` | `1` |
| `page_size` | `20` |
| `action` | `POLICY_ACTIVATED` |
| `entity_type` | `POLICY` |
| `entity_id` | `pol_01J123ABC` |
| `user_id` | `user_001` |
| `from_date` | `2026-07-24` |
| `to_date` | `2026-07-25` |

## Response

```json
{
  "success": true,
  "data": [
    {
      "audit_id": "aud_01J123ABC",
      "action": "POLICY_ACTIVATED",
      "entity_type": "POLICY",
      "entity_id": "pol_01J123DEF",
      "entity_version": 1,
      "performed_by": "user_001",
      "summary": "Policy activated after successful validation.",
      "correlation_id": "cor_01J123ABC",
      "created_at": "2026-07-24T09:20:00.000Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_items": 1,
    "total_pages": 1
  },
  "correlation_id": "cor_01J123ABC"
}
```

---

# 36. Audit Detail

## Endpoint

```http
GET /api/v1/audit/{audit_id}
```

## Response

```json
{
  "success": true,
  "data": {
    "audit_id": "aud_01J123ABC",
    "action": "DECISION_EVALUATED",
    "entity_type": "EVALUATION",
    "entity_id": "eval_01J123ABC",
    "performed_by": "user_001",
    "correlation_id": "cor_01J123ABC",
    "request_snapshot": {
      "customer_id": "CUST-1001",
      "customer_tenure_months": 36,
      "credit_score": 790
    },
    "result_snapshot": {
      "decision": "APPROVE",
      "decision_confidence": 96,
      "winning_policy_id": "pol_01J123DEF"
    },
    "rule_versions": [
      {
        "policy_id": "pol_01J123DEF",
        "version": 1
      }
    ],
    "created_at": "2026-07-24T09:40:00.000Z"
  },
  "meta": {},
  "correlation_id": "cor_01J123ABC"
}
```

---


# 36.1 MySQL Persistence Contract

The API implementation will use MySQL 8.0+ through SQLAlchemy 2.x.

## Connection requirements

Recommended backend environment variable:

```text
DATABASE_URL=mysql+pymysql://decisionflow:decisionflow@mysql:3306/decisionflow
```

Use `localhost` instead of `mysql` when running the backend outside Docker.

## Transaction requirements

- A policy create or update operation must commit atomically.
- Policy activation and version creation must occur in one transaction.
- Decision, rule-result, and audit persistence should be committed atomically where practical.
- Failed writes must be rolled back.
- Database sessions must not be shared across concurrent requests.
- The backend should use `pool_pre_ping=True` to recover stale MySQL connections.

## API behavior when MySQL is unavailable

Return:

```http
503 Service Unavailable
```

with:

```json
{
  "success": false,
  "error": {
    "code": "DATABASE_UNAVAILABLE",
    "message": "The persistence service is temporarily unavailable.",
    "details": []
  },
  "correlation_id": "cor_01J123ABC"
}
```

No endpoint may silently fall back to in-memory or SQLite persistence during integration or demo execution.


# 37. Health Check

## Endpoint

```http
GET /health
```

## Response

```json
{
  "status": "healthy",
  "service": "decisionflow-api",
  "version": "1.0.0",
  "timestamp": "2026-07-24T09:45:00.000Z"
}
```

---

# 38. Readiness Check

## Endpoint

```http
GET /ready
```

## Response

```json
{
  "status": "ready",
  "dependencies": {
    "database": "available",
    "database_type": "mysql",
    "database_version": "8.x",
    "ai_provider": "available",
    "rule_engine": "available"
  }
}
```

If AI provider is unavailable but deterministic decisioning still works, recommended response:

```json
{
  "status": "degraded",
  "dependencies": {
    "database": "available",
    "database_type": "mysql",
    "ai_provider": "unavailable",
    "rule_engine": "available"
  },
  "capabilities": {
    "decision_evaluation": true,
    "ai_policy_generation": false,
    "ai_explanation": false
  }
}
```

---

# 39. Internal Python Service Contracts

These interfaces are not called directly by the frontend, but they must remain stable for integration.

## 39.1 Policy service

```python
class PolicyService:
    def create_policy(self, payload: PolicyCreate, actor_id: str) -> PolicyResponse:
        ...

    def list_policies(self, filters: PolicyFilters) -> PaginatedPolicyResponse:
        ...

    def get_policy(self, policy_id: str) -> PolicyResponse:
        ...

    def update_policy(
        self,
        policy_id: str,
        payload: PolicyUpdate,
        actor_id: str,
    ) -> PolicyResponse:
        ...

    def activate_policy(
        self,
        policy_id: str,
        actor_id: str,
        approval_comment: str | None,
    ) -> PolicyResponse:
        ...

    def disable_policy(
        self,
        policy_id: str,
        actor_id: str,
        reason: str | None,
    ) -> PolicyResponse:
        ...

    def get_active_policies(self, domain: str) -> list[PolicyResponse]:
        ...
```

## 39.2 Rule engine

```python
class RuleEngine:
    def evaluate(
        self,
        request_data: dict,
        policies: list[dict],
    ) -> EngineEvaluationResult:
        ...
```

## 39.3 Priority resolver

```python
class PriorityResolver:
    def resolve(
        self,
        matched_policies: list[PolicyMatchResult],
    ) -> ResolutionResult:
        ...
```

## 39.4 AI policy generator

```python
class AIPolicyGenerator:
    def generate(
        self,
        policy_text: str,
        domain: str,
        field_catalogue: list[dict],
        operator_catalogue: list[dict],
        preferred_decision: str | None = None,
        preferred_priority: int | None = None,
    ) -> AIPolicyGenerationResult:
        ...
```

## 39.5 Conflict detector

```python
class ConflictDetector:
    def detect(
        self,
        candidate_policy: dict,
        active_policies: list[dict],
    ) -> list[ConflictResult]:
        ...
```

## 39.6 Explanation service

```python
class ExplanationService:
    def generate(
        self,
        evaluation_result: dict,
        style: str = "BUSINESS",
    ) -> ExplanationResult:
        ...
```

## 39.7 Decision service

```python
class DecisionService:
    def evaluate(
        self,
        request: DecisionEvaluationRequest,
        actor_id: str,
        correlation_id: str,
    ) -> DecisionEvaluationResponse:
        ...
```

---

# 40. Decision Service Orchestration Contract

The integration lead should implement the decision service in this exact order.

```python
def evaluate(request, actor_id, correlation_id):
    validated_request = validate_request(request)

    active_policies = policy_service.get_active_policies(
        domain=validated_request.domain
    )

    engine_result = rule_engine.evaluate(
        request_data=validated_request.customer,
        policies=active_policies,
    )

    resolution = priority_resolver.resolve(
        matched_policies=engine_result.matched_policies
    )

    confidence = confidence_calculator.calculate(
        request_data=validated_request.customer,
        engine_result=engine_result,
        resolution=resolution,
    )

    explanation = explanation_service.generate(
        evaluation_result={
            "request": validated_request,
            "engine_result": engine_result,
            "resolution": resolution,
            "confidence": confidence,
        }
    )

    stored_evaluation = evaluation_repository.save(
        request=validated_request,
        result=engine_result,
        resolution=resolution,
        confidence=confidence,
        explanation=explanation,
        correlation_id=correlation_id,
    )

    audit_service.record_decision(
        evaluation=stored_evaluation,
        actor_id=actor_id,
        correlation_id=correlation_id,
    )

    return build_decision_response(
        evaluation=stored_evaluation,
        explanation=explanation,
    )
```

---

# 41. Frontend API Client Contract

Frontend should centralize API calls.

Recommended structure:

```text
frontend/src/services/
├── apiClient.js
├── policyApi.js
├── aiApi.js
├── decisionApi.js
├── analyticsApi.js
└── auditApi.js
```

## Base client behavior

The client should:

- Read `VITE_API_BASE_URL`.
- Set `Content-Type: application/json`.
- Generate or forward `X-Correlation-ID`.
- Parse the standard response envelope.
- Throw normalized frontend errors.
- Apply request timeout.
- Avoid placing API logic inside React components.

Example normalized client error:

```javascript
{
  code: "POLICY_VALIDATION_ERROR",
  message: "The policy contains invalid conditions.",
  details: [],
  correlationId: "cor_01J123ABC"
}
```

---

# 42. Mock API Responses for Parallel Development

The frontend engineer should create mock data matching this contract before the backend is available.

Recommended mock files:

```text
frontend/src/mocks/
├── policies.js
├── aiPolicyGeneration.js
├── decisionEvaluation.js
├── analytics.js
└── audit.js
```

## Minimum frontend mock set

### Dashboard summary

Use the exact response from:

```text
GET /analytics/summary
```

### Policy list

Use the exact response from:

```text
GET /policies
```

### AI generation

Prepare:

- Successful generation
- Ambiguous request
- Conflict warning
- Provider failure

### Decision evaluation

Prepare:

- Approval
- Rejection due to priority
- Manual review due to missing fields
- No matching policy
- Server error

---

# 43. Request and Response Ownership Matrix

| API Group | Primary Implementer | Required Consumer |
|---|---|---|
| `/config/*` | Backend Engineer | Frontend, AI |
| `/policies/*` | Backend Engineer | Frontend, Integration |
| `/ai/policies/*` | AI Engineer + Integration Lead | Frontend |
| `/decisions/*` | Integration Lead | Frontend |
| `/analytics/*` | Backend Engineer | Frontend |
| `/audit/*` | Backend Engineer | Frontend |
| `/health`, `/ready` | Integration Lead | Demo, Docker |

---

# 44. Sequence: AI Policy Creation

```text
Frontend
  │
  │ POST /ai/policies/generate
  ▼
AI Router
  │
  ▼
AI Policy Generator
  │
  ├── Load field catalogue
  ├── Load operator catalogue
  ├── Call LLM
  ├── Parse JSON
  ├── Validate schema
  ├── Run ambiguity checks
  ├── Run deterministic conflict checks
  └── Return candidate
  │
  ▼
Frontend Review Screen
  │
  │ POST /policies
  ▼
Policy Service
  │
  ├── Validate again
  ├── Store as DRAFT
  └── Return policy
```

---

# 45. Sequence: Policy Activation

```text
Frontend
  │
  │ POST /policies/{id}/activate
  ▼
Policy Router
  │
  ▼
Policy Service
  │
  ├── Load policy
  ├── Validate policy
  ├── Run conflict scan
  ├── Verify state transition
  ├── Create immutable version
  ├── Set ACTIVE
  ├── Save approver
  └── Create audit record
  │
  ▼
Frontend
```

---

# 46. Sequence: Decision Evaluation

```text
Frontend
  │
  │ POST /decisions/evaluate
  ▼
Decision Router
  │
  ▼
Decision Service
  │
  ├── Validate request
  ├── Load active policies
  ├── Call Rule Engine
  ├── Call Priority Resolver
  ├── Calculate confidence
  ├── Call Explanation Service
  ├── Store evaluation
  ├── Store condition traces
  ├── Write audit log
  └── Return response
  │
  ▼
Frontend Result Screen
```

---

# 47. AI Failure Fallback Contract

## Policy generation failure

If AI policy generation fails:

- Return `502` or `503`.
- Frontend shows retry.
- Frontend may offer manual policy creation.
- No policy is saved automatically.

## Explanation failure

If AI explanation fails:

- Decision must still be returned successfully.
- Use deterministic fallback explanation.
- Set:

```json
{
  "generated_by": "DETERMINISTIC_FALLBACK",
  "fallback_used": true
}
```

- Add warning:

```json
{
  "code": "AI_EXPLANATION_UNAVAILABLE",
  "message": "A deterministic explanation was provided because the AI explanation service was unavailable."
}
```

## Decision engine failure

If rule evaluation fails:

- Return `500`.
- Do not return an invented decision.
- Log correlation ID.
- Save failure audit record if possible.

---

# 48. Idempotency Guidance

For the POC, idempotency is optional but useful for policy creation and decision evaluation.

Recommended request header:

```http
Idempotency-Key: idem_01J123ABC
```

If implemented:

- Same key and same payload return the original result.
- Same key and different payload return `409 Conflict`.

This is not mandatory for the first integration milestone.

---

# 49. CORS Requirements

Backend should allow the frontend development origin:

```text
http://localhost:5173
```

Example FastAPI configuration:

```python
allow_origins = [
    "http://localhost:5173",
]
```

For demo-only local use, permissive CORS may be temporarily used, but should be documented.

---

# 50. Pagination Contract

Default values:

```text
page = 1
page_size = 20
maximum page_size = 100
```

Response metadata:

```json
{
  "page": 1,
  "page_size": 20,
  "total_items": 45,
  "total_pages": 3
}
```

Invalid page values should return `422`.

---

# 51. Sorting Contract

Supported values depend on endpoint.

Policy sort fields:

```text
name
priority
status
created_at
updated_at
```

Decision sort fields:

```text
evaluated_at
decision_confidence
total_latency_ms
```

Sort order:

```text
asc
desc
```

Unsupported sort field should return `400`.

---

# 52. Search Contract

Policy search should perform case-insensitive matching across:

- Policy name
- Description
- Reason

Audit search may be deferred for the POC.

---

# 53. Date Filter Contract

Use inclusive start and end dates.

Example:

```text
from_date=2026-07-24
to_date=2026-07-25
```

Backend should interpret date-only values in UTC for the POC.

---

# 54. API Validation Checklist

Before a developer declares an endpoint complete, verify:

- Route matches contract.
- HTTP method matches contract.
- Request field names match exactly.
- Response envelope matches exactly.
- Enum values match exactly.
- Dates are ISO 8601.
- Confidence is 0 to 100.
- Errors use standard error envelope.
- Correlation ID is present.
- No internal database IDs leak unexpectedly.
- No secret or API key appears in response.
- AI-generated policy is not automatically active.
- Decision is generated only by deterministic engine.

---

# 55. Contract Test Cases

## Policy API

1. Create valid draft.
2. Reject unsupported field.
3. Reject unsupported operator.
4. Reject incorrect value type.
5. Return duplicate-name conflict.
6. Activate valid draft.
7. Block invalid activation.
8. Disable active policy.
9. List filtered policies.
10. Retrieve policy by ID.

## AI API

1. Generate valid rule.
2. Detect ambiguous term.
3. Reject invalid LLM JSON.
4. Detect unsupported field.
5. Return provider failure.
6. Generate test cases.
7. Detect conflict.

## Decision API

1. Approve eligible customer.
2. Reject fraud-risk customer.
3. Resolve multiple matches by priority.
4. Return manual review for missing fields.
5. Include condition trace.
6. Continue when explanation AI fails.
7. Store audit and evaluation.
8. Return deterministic fallback when no policy matches.

## Analytics API

1. Return zero-state summary.
2. Return counts after evaluations.
3. Return decision distribution.
4. Return top policies.

## Audit API

1. Record policy activation.
2. Record decision evaluation.
3. Filter by entity.
4. Retrieve detail by ID.

---

# 56. Minimum Endpoint Set for Hackathon Demo

If time is limited, the mandatory endpoints are:

```text
GET  /health
GET  /api/v1/config/fields
GET  /api/v1/config/operators

POST /api/v1/ai/policies/generate

POST /api/v1/policies
GET  /api/v1/policies
GET  /api/v1/policies/{policy_id}
POST /api/v1/policies/{policy_id}/activate
POST /api/v1/policies/{policy_id}/disable

POST /api/v1/decisions/evaluate
GET  /api/v1/decisions/{evaluation_id}

GET  /api/v1/analytics/summary
GET  /api/v1/audit
```

Everything else is secondary.

---

# 57. Swagger/OpenAPI Expectations

FastAPI should expose:

```text
/docs
```

and optionally:

```text
/redoc
```

Every endpoint should include:

- Summary
- Description
- Response model
- Status code
- Example request
- Example response
- Error responses
- Tags

Recommended tags:

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

# 58. Naming Conventions

## JSON

Use `snake_case`.

Correct:

```json
{
  "customer_tenure_months": 24
}
```

Incorrect:

```json
{
  "customerTenureMonths": 24
}
```

## Python

Use `snake_case` for functions and variables.

## React

Internal component props may use JavaScript conventions, but network payloads must preserve contract names.

## Routes

Use plural resource names:

```text
/policies
/decisions
```

---

# 59. Backward Compatibility

During the hackathon:

- Do not rename existing fields after frontend work begins.
- Add optional fields instead of changing required fields.
- Do not change enum values without approval from the integration lead.
- Any unavoidable change must update:
  - This document
  - Backend schemas
  - Frontend mocks
  - Frontend types
  - Tests

---

# 60. Change Approval Process

Any contract change requires:

1. Proposed change shared in team chat.
2. Impact identified.
3. Integration lead approves.
4. Document updated.
5. Frontend mock updated.
6. Backend schema updated.
7. Tests updated.

No silent contract changes.

---

# 61. Final Integration Checklist

Before final merge:

- Frontend points to real API base URL.
- CORS is configured.
- Policy creation works.
- AI generation works.
- Generated policy can be saved.
- Draft can be activated.
- Active policy appears in list.
- Decision evaluation uses active policies.
- Priority resolution works.
- Explanation fallback works.
- Audit record is visible.
- Analytics update after evaluation.
- All responses include correlation IDs.
- Demo seed data is loaded.
- `/health` is green.
- Swagger loads.
- `.env.example` exists.
- No API keys are committed.

---

# 62. Final Contract Summary

The project depends on four boundaries remaining stable:

```text
Frontend ↔ REST API
REST API ↔ Application Services
Application Services ↔ Rule Engine
Application Services ↔ AI Module
```

The central rule is:

> Each team member may change implementation details inside their own module, but no one may change a shared request, response, function signature, enum, or state transition without updating this API contract and informing the integration lead.

This contract is the foundation that allows all four developers to work independently and integrate their work with minimal rework.
