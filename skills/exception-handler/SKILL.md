---
name: exception-handler
description: Diagnoses backend errors by tailing logs, identifying exception types, mapping to the spec's exception hierarchy (§34-35), assessing impact area, and proposing fixes with approval workflow.
---

# Exception Handler Agent

## Purpose
When the backend crashes or returns unexpected errors, this agent diagnoses the issue by analyzing logs, mapping exceptions to the spec's hierarchy, and proposing fixes.

## How to Invoke

### As a User
Type in chat:
```
/exception-handler
```
Or with context:
```
/exception-handler the policy creation endpoint is returning a 500 error
```

### As Another Agent
Reference this skill when encountering errors during any phase:
```
When you encounter an unhandled exception or 500 error, read and follow:
skills/exception-handler/SKILL.md
```

## Execution Steps

### Step 1: Collect Log Evidence
1. Check if the uvicorn dev server is running — look for a background task or process on port 8000
2. Read the most recent log output. Try these sources in order:
   - Terminal output from the running uvicorn process (use `manage_task` to check status)
   - If logs are written to a file, tail the last 150 lines:
     ```powershell
     Get-Content backend/app.log -Tail 150
     ```
   - If pytest failed, read the pytest output from the last test run
3. If no logs are available, ask the user to reproduce the error and share the traceback

### Step 2: Classify the Exception
Map the exception to one of the spec-defined types from `backend/app/core/exceptions.py` (Spec §34):

| Exception Class | HTTP Status | When It Occurs |
|---|---|---|
| `PolicyNotFoundError` | 404 | Policy ID doesn't exist in DB |
| `DuplicatePolicyNameError` | 409 | Creating policy with existing name |
| `PolicyValidationError` | 400 | Invalid conditions, fields, operators, or values |
| `UnsupportedOperatorError` | 400 | Operator not in registry |
| `OperatorTypeError` | 400 | Type mismatch in operator evaluation |
| `InvalidPolicyStateError` | 409 | Invalid status transition (e.g., activate archived) |
| `PolicyActivationBlockedError` | 409 | Blocking conflicts prevent activation |
| `DatabaseUnavailableError` | 500 | MySQL connection failed |
| `EvaluationPersistenceError` | 500 | Failed to save evaluation results |
| `AuditNotFoundError` | 404 | Audit ID doesn't exist |

If the exception is NOT one of these, it's either:
- A **Pydantic ValidationError** → should be caught by the global error handler
- A **SQLAlchemy error** → should be wrapped, never exposed raw
- An **unexpected Python error** → log with traceback, return safe message

### Step 3: Identify Impact Area
Determine which architectural layer is affected:

```
API Layer (routers)        → Check: request parsing, dependency injection, response envelope
Service Layer              → Check: business logic, transaction management, validation calls
Repository Layer           → Check: SQLAlchemy queries, session management, N+1 queries
Rule Engine Layer          → Check: operator functions, condition evaluation, resolver logic
Database Layer             → Check: MySQL connectivity, migration state, schema mismatch
```

### Step 4: Check Error Handler Coverage
1. Open `backend/app/core/error_handlers.py`
2. Verify that a handler exists for this exception type
3. Verify the handler returns the correct error envelope (Spec §35):
   ```json
   {
     "success": false,
     "error": {
       "code": "ERROR_CODE",
       "message": "Human-readable message",
       "details": []
     },
     "correlation_id": "cor_..."
   }
   ```
4. If no handler exists, propose adding one

### Step 5: Propose Fix
1. Show the root cause with file path and line number
2. Show the proposed code change as a diff
3. Explain WHY this fix is correct per the spec
4. **Wait for user approval before applying any changes**

### Step 6: Verify Fix
After the fix is approved and applied:
1. Re-run the failing scenario
2. Verify the correct HTTP status code is returned
3. Verify the error envelope format matches the contract
4. Verify the correlation ID is present in the response

## Important Rules
- NEVER silently catch exceptions and return `false` — the spec explicitly forbids this (§17)
- NEVER expose raw SQLAlchemy exceptions to API consumers (§34)
- NEVER expose stack traces in API responses (§52)
- ALWAYS include correlation_id in error responses (§36)
- ALWAYS log the full traceback server-side for unexpected errors (§35)
