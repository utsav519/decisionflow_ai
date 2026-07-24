"""
Condition evaluator.

Evaluates a set of active policies against customer input data.
Recursively walks ConditionGroup trees (all/any).
Pure function — no DB, no AI. Input objects are never mutated.

Spec reference: §21 Condition Evaluator
"""

from __future__ import annotations

import copy
import logging
import time
from typing import Any

from app.engine.exceptions import OperatorTypeError, UnsupportedOperatorError
from app.engine.operators import get_operator
from app.engine.result_models import (
    ConditionResult,
    EngineEvaluationResult,
    PolicyEvaluationResult,
)

logger = logging.getLogger(__name__)


def _resolve_field(data: dict[str, Any], field_path: str) -> tuple[Any, bool]:
    """Resolve a dot-notation field path against input data.

    Args:
        data: The flat or nested input dictionary.
        field_path: Dot-separated path (e.g. 'customer.credit_score').

    Returns:
        Tuple of (value, found). If the field is missing, returns (None, False).
    """
    keys = field_path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None, False
    return current, True


def _evaluate_condition(
    condition: dict[str, Any],
    data: dict[str, Any],
) -> ConditionResult:
    """Evaluate a single leaf condition against input data.

    Args:
        condition: Dict with 'field', 'operator', 'value'.
        data: Customer/request data to evaluate against.

    Returns:
        ConditionResult with match status and reason.
    """
    field_path = condition["field"]
    operator_name = condition["operator"]
    expected = condition.get("value")

    actual, found = _resolve_field(data, field_path)

    if not found:
        return ConditionResult(
            field=field_path,
            operator=operator_name,
            expected=expected,
            actual=None,
            matched=False,
            status="MISSING_FIELD",
            reason=f"Field '{field_path}' not present in input data",
        )

    try:
        op_fn = get_operator(operator_name)
    except UnsupportedOperatorError:
        return ConditionResult(
            field=field_path,
            operator=operator_name,
            expected=expected,
            actual=actual,
            matched=False,
            status="ERROR",
            reason=f"Unsupported operator: '{operator_name}'",
        )

    try:
        matched = op_fn(actual, expected)
    except OperatorTypeError as e:
        return ConditionResult(
            field=field_path,
            operator=operator_name,
            expected=expected,
            actual=actual,
            matched=False,
            status="INVALID_VALUE",
            reason=str(e.message),
        )
    except Exception as e:
        return ConditionResult(
            field=field_path,
            operator=operator_name,
            expected=expected,
            actual=actual,
            matched=False,
            status="ERROR",
            reason=f"Evaluation error: {e}",
        )

    return ConditionResult(
        field=field_path,
        operator=operator_name,
        expected=expected,
        actual=actual,
        matched=matched,
        status="MATCHED" if matched else "UNMATCHED",
    )


def _evaluate_group(
    group: dict[str, Any],
    data: dict[str, Any],
) -> tuple[bool, list[ConditionResult]]:
    """Recursively evaluate a condition group (all/any).

    Args:
        group: Dict with 'all' or 'any' key containing a list of conditions/groups.
        data: Customer/request data.

    Returns:
        Tuple of (group_matched, list_of_all_condition_results).
    """
    all_results: list[ConditionResult] = []

    if "all" in group and group["all"] is not None:
        children = group["all"]
        group_matched = True
        for child in children:
            if "field" in child and "operator" in child:
                # Leaf condition
                result = _evaluate_condition(child, data)
                all_results.append(result)
                if not result.matched:
                    group_matched = False
            else:
                # Nested group
                child_matched, child_results = _evaluate_group(child, data)
                all_results.extend(child_results)
                if not child_matched:
                    group_matched = False
        return group_matched, all_results

    elif "any" in group and group["any"] is not None:
        children = group["any"]
        group_matched = False
        for child in children:
            if "field" in child and "operator" in child:
                result = _evaluate_condition(child, data)
                all_results.append(result)
                if result.matched:
                    group_matched = True
            else:
                child_matched, child_results = _evaluate_group(child, data)
                all_results.extend(child_results)
                if child_matched:
                    group_matched = True
        return group_matched, all_results

    else:
        # Empty or invalid group — treat as no match
        return False, all_results


def evaluate_policy(
    policy: dict[str, Any],
    data: dict[str, Any],
) -> PolicyEvaluationResult:
    """Evaluate a single policy against input data.

    Does NOT mutate the policy or data dicts.

    Args:
        policy: Dict with 'id', 'name', 'current_version', 'priority',
                'decision', 'conditions_json'.
        data: Customer/request data to evaluate.

    Returns:
        PolicyEvaluationResult with match status and condition traces.
    """
    conditions = policy["conditions_json"]
    if isinstance(conditions, str):
        import json
        conditions = json.loads(conditions)

    matched, condition_results = _evaluate_group(conditions, data)

    missing_fields = [
        cr.field for cr in condition_results if cr.status == "MISSING_FIELD"
    ]

    # Determine result status
    if missing_fields and not matched:
        result_status = "SKIPPED_MISSING_FIELD"
    elif any(cr.status == "INVALID_VALUE" for cr in condition_results) and not matched:
        result_status = "SKIPPED_INVALID_DATA"
    elif matched:
        result_status = "MATCHED"
    else:
        result_status = "UNMATCHED"

    return PolicyEvaluationResult(
        policy_id=policy["id"],
        policy_name=policy["name"],
        policy_version=policy["current_version"],
        priority=policy["priority"],
        decision=policy["decision"],
        matched=matched,
        condition_results=condition_results,
        missing_fields=missing_fields,
        result_status=result_status,
    )


def evaluate_policies(
    policies: list[dict[str, Any]],
    data: dict[str, Any],
) -> EngineEvaluationResult:
    """Evaluate multiple policies against input data.

    Pure function. Does NOT mutate inputs.

    Args:
        policies: List of policy dicts (active policies only).
        data: Customer/request data.

    Returns:
        EngineEvaluationResult grouping policies into matched/unmatched/skipped.
    """
    # Deep copy inputs to guarantee immutability (spec §42 item 15)
    safe_data = copy.deepcopy(data)

    start = time.perf_counter()
    matched: list[PolicyEvaluationResult] = []
    unmatched: list[PolicyEvaluationResult] = []
    skipped: list[PolicyEvaluationResult] = []
    warnings: list[str] = []

    for policy in policies:
        try:
            result = evaluate_policy(policy, safe_data)
            if result.result_status == "MATCHED":
                matched.append(result)
            elif result.result_status in ("SKIPPED_MISSING_FIELD", "SKIPPED_INVALID_DATA"):
                skipped.append(result)
                warnings.append(
                    f"Policy '{result.policy_name}' ({result.policy_id}) skipped: "
                    f"{result.result_status}"
                )
            else:
                unmatched.append(result)
        except Exception as e:
            logger.error("Error evaluating policy %s: %s", policy.get("id"), e)
            warnings.append(f"Policy '{policy.get('name')}' evaluation error: {e}")

    elapsed_ms = (time.perf_counter() - start) * 1000

    if not policies:
        warnings.append("No active policies provided for evaluation")

    return EngineEvaluationResult(
        matched=matched,
        unmatched=unmatched,
        skipped=skipped,
        evaluation_time_ms=round(elapsed_ms, 2),
        warnings=warnings,
    )
