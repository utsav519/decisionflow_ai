---
name: engine-test
description: Runs rule engine tests (operators, evaluator, resolver, confidence) and checks coverage against the 15 evaluator tests (§42), 8 resolver tests (§43), and operator tests (§41) required by the spec.
---

# Engine Test Agent

## Purpose
Runs all rule-engine related tests, compares results against spec-required test cases, identifies missing coverage, and generates skeleton tests for gaps.

## How to Invoke

### As a User
```
/engine-test
```
Or target a specific component:
```
/engine-test operators
/engine-test resolver
```

### As Another Agent
```
After modifying any file in backend/app/engine/, read and follow:
skills/engine-test/SKILL.md
```

## Execution Steps

### Step 1: Run Engine Tests
Execute the engine test suite:
```powershell
cd e:\code\hackathon\decisionflow_ai\backend
.venv\Scripts\python -m pytest tests/test_operators.py tests/test_evaluator.py tests/test_resolver.py tests/test_confidence.py -v --tb=short 2>&1
```

If specific test files don't exist yet, note them as missing.

### Step 2: Check Operator Test Coverage (Spec §41)
Every operator must be tested with 4 cases:

| Operator | Match | No Match | Invalid Type | Edge/Boundary |
|---|---|---|---|---|
| `equals` | ☐ | ☐ | ☐ | ☐ |
| `not_equals` | ☐ | ☐ | ☐ | ☐ |
| `greater_than` | ☐ | ☐ | ☐ | ☐ |
| `greater_than_or_equal` | ☐ | ☐ | ☐ | ☐ |
| `less_than` | ☐ | ☐ | ☐ | ☐ |
| `less_than_or_equal` | ☐ | ☐ | ☐ | ☐ |
| `contains` | ☐ | ☐ | ☐ | ☐ |
| `in` | ☐ | ☐ | ☐ | ☐ |
| `not_in` | ☐ | ☐ | ☐ | ☐ |
| `is_empty` | ☐ | ☐ | ☐ | ☐ |
| `is_not_empty` | ☐ | ☐ | ☐ | ☐ |

Scan `tests/test_operators.py` and check each test function name and assertions against this matrix.

### Step 3: Check Evaluator Test Coverage (Spec §42)
The spec requires these 15 test scenarios:

1. ☐ Single matching condition
2. ☐ Single non-matching condition
3. ☐ `all` group matches
4. ☐ `all` group fails
5. ☐ `any` group matches
6. ☐ `any` group fails
7. ☐ Nested group
8. ☐ Missing field
9. ☐ Unsupported operator
10. ☐ Invalid value type
11. ☐ Multiple matching policies
12. ☐ No policies
13. ☐ No matching policies
14. ☐ Performance metric present
15. ☐ Input objects are not mutated

Scan `tests/test_evaluator.py` and map each test to this list.

### Step 4: Check Resolver Test Coverage (Spec §43)
The spec requires these 8 test scenarios:

1. ☐ Highest priority wins
2. ☐ REJECT wins a same-priority tie
3. ☐ MANUAL_REVIEW wins over APPROVE at same priority
4. ☐ Higher version wins after same priority and same decision
5. ☐ Policy ID resolves the final tie
6. ☐ No match returns MANUAL_REVIEW fallback
7. ☐ Resolution reason is present
8. ☐ Result is deterministic across repeated calls

### Step 5: Generate Missing Tests
For each uncovered scenario, generate a skeleton test:
```python
def test_<scenario_name>():
    """Spec §XX requirement: <description>"""
    # Arrange
    ...
    # Act
    ...
    # Assert
    ...
```

### Step 6: Report Coverage Matrix
```
Component       | Required | Found | Missing | Pass | Fail
----------------|----------|-------|---------|------|-----
Operators       | 44       | ??    | ??      | ??   | ??
Evaluator       | 15       | ??    | ??      | ??   | ??
Resolver        | 8        | ??    | ??      | ??   | ??
Confidence      | 6+       | ??    | ??      | ??   | ??
TOTAL           | 73+      | ??    | ??      | ??   | ??
```

## Important Rules
- The rule engine tests must NOT require MySQL — use in-memory fixtures (§56)
- Engine must be pure: no DB, no AI calls (§62)
- Input objects must NOT be mutated during evaluation (§42 item 15)
- Same input must always produce same output (§22, §43 item 8)
