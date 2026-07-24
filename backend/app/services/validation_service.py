"""
Validation service — validates policy conditions against domain catalogue.

Checks that all referenced fields and operators are valid.

Spec reference: §27 Validation
"""

from __future__ import annotations

import logging
from typing import Any

from app.core.domain_catalogue import DomainCatalogue
from app.engine.operators import OPERATOR_REGISTRY

logger = logging.getLogger(__name__)


class ValidationResult:
    """Container for validation outcome."""

    def __init__(self) -> None:
        self.errors: list[dict[str, Any]] = []
        self.warnings: list[str] = []

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    @property
    def status(self) -> str:
        return "PASSED" if self.passed else "FAILED"

    def add_error(self, path: str, issue: str, **kwargs: Any) -> None:
        detail = {"path": path, "issue": issue}
        detail.update(kwargs)
        self.errors.append(detail)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)


def validate_conditions(
    conditions: dict[str, Any],
    domain: str,
) -> ValidationResult:
    """Validate a condition tree against known fields and operators.

    Args:
        conditions: The conditions_json (ConditionGroup dict).
        domain: Business domain for field catalogue lookup.

    Returns:
        ValidationResult with errors and warnings.
    """
    result = ValidationResult()
    known_fields = DomainCatalogue.get_fields_for_domain(domain)

    _validate_group(conditions, known_fields, result, path="conditions")

    if not known_fields:
        result.add_warning(
            f"Domain '{domain}' has no registered fields in the catalogue. "
            "Field validation was skipped."
        )

    return result


def _validate_group(
    group: dict[str, Any],
    known_fields: dict[str, str],
    result: ValidationResult,
    path: str,
) -> None:
    """Recursively validate a condition group."""
    has_all = "all" in group and group["all"] is not None
    has_any = "any" in group and group["any"] is not None

    if not has_all and not has_any:
        result.add_error(path, "Condition group must contain 'all' or 'any'")
        return

    if has_all and has_any:
        result.add_error(path, "'all' and 'any' are mutually exclusive in a single group")
        return

    children = group.get("all") or group.get("any") or []
    group_type = "all" if has_all else "any"

    if len(children) == 0:
        result.add_error(f"{path}.{group_type}", "Condition group must have at least one child")
        return

    for i, child in enumerate(children):
        child_path = f"{path}.{group_type}[{i}]"
        if "field" in child and "operator" in child:
            _validate_condition(child, known_fields, result, child_path)
        elif "all" in child or "any" in child:
            _validate_group(child, known_fields, result, child_path)
        else:
            result.add_error(child_path, "Invalid condition node — must be a condition or group")


def _validate_condition(
    condition: dict[str, Any],
    known_fields: dict[str, str],
    result: ValidationResult,
    path: str,
) -> None:
    """Validate a single leaf condition."""
    field = condition.get("field", "")
    operator = condition.get("operator", "")

    if not field:
        result.add_error(f"{path}.field", "Field name is required")

    if not operator:
        result.add_error(f"{path}.operator", "Operator is required")

    # Validate operator exists in registry
    if operator and operator not in OPERATOR_REGISTRY:
        result.add_error(
            f"{path}.operator",
            f"Unsupported operator: '{operator}'",
            received=operator,
            allowed_values=list(OPERATOR_REGISTRY.keys()),
        )

    # Validate field exists in domain catalogue
    if field and known_fields and field not in known_fields:
        result.add_error(
            f"{path}.field",
            f"Field '{field}' is not in the domain catalogue.",
            received=field
        )
