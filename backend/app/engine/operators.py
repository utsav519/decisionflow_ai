"""
Operator registry and functions.

Every operator is a pure function: (actual_value, expected_value) → bool.
No DB, no AI, no side effects.

Spec reference: §20 Supported Operators
"""

from __future__ import annotations

import logging
from typing import Any, Callable

from app.engine.exceptions import OperatorTypeError, UnsupportedOperatorError

logger = logging.getLogger(__name__)

# Type alias for operator functions
OperatorFn = Callable[[Any, Any], bool]


# ──────────────────────────────────────────────
# Operator implementations
# ──────────────────────────────────────────────


def _equals(actual: Any, expected: Any) -> bool:
    """Exact equality check."""
    return actual == expected


def _not_equals(actual: Any, expected: Any) -> bool:
    """Inequality check."""
    return actual != expected


def _greater_than(actual: Any, expected: Any) -> bool:
    """Strict greater-than for numeric values."""
    try:
        return float(actual) > float(expected)
    except (TypeError, ValueError) as exc:
        raise OperatorTypeError("greater_than", "numeric", actual) from exc


def _greater_than_or_equal(actual: Any, expected: Any) -> bool:
    """Greater-than-or-equal for numeric values."""
    try:
        return float(actual) >= float(expected)
    except (TypeError, ValueError) as exc:
        raise OperatorTypeError("greater_than_or_equal", "numeric", actual) from exc


def _less_than(actual: Any, expected: Any) -> bool:
    """Strict less-than for numeric values."""
    try:
        return float(actual) < float(expected)
    except (TypeError, ValueError) as exc:
        raise OperatorTypeError("less_than", "numeric", actual) from exc


def _less_than_or_equal(actual: Any, expected: Any) -> bool:
    """Less-than-or-equal for numeric values."""
    try:
        return float(actual) <= float(expected)
    except (TypeError, ValueError) as exc:
        raise OperatorTypeError("less_than_or_equal", "numeric", actual) from exc


def _contains(actual: Any, expected: Any) -> bool:
    """Check if expected is contained within actual (string or list)."""
    if isinstance(actual, str):
        return str(expected) in actual
    if isinstance(actual, (list, tuple, set)):
        return expected in actual
    raise OperatorTypeError("contains", "string or collection", actual)


def _in(actual: Any, expected: Any) -> bool:
    """Check if actual is a member of expected (which must be a list)."""
    if not isinstance(expected, (list, tuple, set)):
        raise OperatorTypeError("in", "list", expected)
    return actual in expected


def _not_in(actual: Any, expected: Any) -> bool:
    """Check if actual is NOT a member of expected."""
    if not isinstance(expected, (list, tuple, set)):
        raise OperatorTypeError("not_in", "list", expected)
    return actual not in expected


def _is_empty(actual: Any, expected: Any) -> bool:
    """Check if actual is empty (None, empty string, empty list, 0)."""
    if actual is None:
        return True
    if isinstance(actual, str):
        return actual.strip() == ""
    if isinstance(actual, (list, tuple, set, dict)):
        return len(actual) == 0
    return False


def _is_not_empty(actual: Any, expected: Any) -> bool:
    """Check if actual has a value (not empty)."""
    return not _is_empty(actual, expected)


# ──────────────────────────────────────────────
# Operator registry
# ──────────────────────────────────────────────

OPERATOR_REGISTRY: dict[str, OperatorFn] = {
    "equals": _equals,
    "not_equals": _not_equals,
    "greater_than": _greater_than,
    "greater_than_or_equal": _greater_than_or_equal,
    "less_than": _less_than,
    "less_than_or_equal": _less_than_or_equal,
    "contains": _contains,
    "in": _in,
    "not_in": _not_in,
    "is_empty": _is_empty,
    "is_not_empty": _is_not_empty,
}


def get_operator(name: str) -> OperatorFn:
    """Look up an operator function by name.

    Args:
        name: Operator identifier (e.g. 'greater_than').

    Returns:
        The operator function.

    Raises:
        UnsupportedOperatorError: If the operator is not registered.
    """
    fn = OPERATOR_REGISTRY.get(name)
    if fn is None:
        raise UnsupportedOperatorError(name)
    return fn


def get_supported_operators() -> list[dict[str, str]]:
    """Return a list of all registered operators for the config API.

    Returns:
        List of dicts with 'id' and 'description' for each operator.
    """
    descriptions = {
        "equals": "Exact equality check",
        "not_equals": "Inequality check",
        "greater_than": "Strict greater-than (numeric)",
        "greater_than_or_equal": "Greater-than-or-equal (numeric)",
        "less_than": "Strict less-than (numeric)",
        "less_than_or_equal": "Less-than-or-equal (numeric)",
        "contains": "Check if value is contained within field (string/list)",
        "in": "Check if field value is a member of a list",
        "not_in": "Check if field value is NOT a member of a list",
        "is_empty": "Check if field is empty/None/blank",
        "is_not_empty": "Check if field has a value",
    }
    return [
        {"id": op_id, "description": descriptions.get(op_id, "")}
        for op_id in OPERATOR_REGISTRY
    ]
