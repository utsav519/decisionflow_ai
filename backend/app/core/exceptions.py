"""
Application-specific exception hierarchy.

Every custom exception carries: code, message, status_code, details.
Raw SQLAlchemy or framework exceptions must never reach API consumers.

Spec reference: §34 Exception Types
"""

from __future__ import annotations

from typing import Any


class ApplicationError(Exception):
    """Base exception for all application errors."""

    def __init__(
        self,
        code: str = "APPLICATION_ERROR",
        message: str = "An unexpected application error occurred.",
        status_code: int = 500,
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []
        super().__init__(self.message)


class PolicyNotFoundError(ApplicationError):
    """Raised when a policy ID does not exist in the database."""

    def __init__(self, policy_id: str) -> None:
        super().__init__(
            code="POLICY_NOT_FOUND",
            message="The requested policy does not exist.",
            status_code=404,
            details=[
                {
                    "path": "policy_id",
                    "issue": "Unknown identifier",
                    "received": policy_id,
                }
            ],
        )


class DuplicatePolicyNameError(ApplicationError):
    """Raised when creating a policy with a name that already exists."""

    def __init__(self, name: str) -> None:
        super().__init__(
            code="DUPLICATE_POLICY_NAME",
            message="A policy with this name already exists.",
            status_code=409,
            details=[
                {
                    "path": "name",
                    "issue": "Duplicate name",
                    "received": name,
                }
            ],
        )


class PolicyValidationError(ApplicationError):
    """Raised when policy validation fails (fields, operators, values)."""

    def __init__(
        self,
        message: str = "The policy contains invalid data.",
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(
            code="POLICY_VALIDATION_ERROR",
            message=message,
            status_code=400,
            details=details,
        )


class UnsupportedOperatorError(ApplicationError):
    """Raised when an operator is not in the registry."""

    def __init__(self, operator: str) -> None:
        super().__init__(
            code="UNSUPPORTED_OPERATOR",
            message=f"The operator '{operator}' is not supported.",
            status_code=400,
            details=[
                {
                    "path": "operator",
                    "issue": "Unsupported operator",
                    "received": operator,
                }
            ],
        )


class OperatorTypeError(ApplicationError):
    """Raised when a type mismatch occurs during operator evaluation."""

    def __init__(
        self,
        operator: str,
        expected_type: str,
        received_value: Any,
    ) -> None:
        super().__init__(
            code="OPERATOR_TYPE_ERROR",
            message=f"Type mismatch for operator '{operator}'.",
            status_code=400,
            details=[
                {
                    "path": "value",
                    "issue": f"Expected {expected_type}",
                    "received": str(received_value),
                }
            ],
        )


class InvalidPolicyStateError(ApplicationError):
    """Raised when a policy state transition is not allowed."""

    def __init__(
        self,
        current_status: str,
        attempted_action: str,
    ) -> None:
        super().__init__(
            code="INVALID_POLICY_STATE",
            message=(
                f"Cannot {attempted_action} a policy with status "
                f"'{current_status}'."
            ),
            status_code=409,
            details=[
                {
                    "path": "status",
                    "issue": "Invalid state transition",
                    "received": current_status,
                }
            ],
        )


class PolicyActivationBlockedError(ApplicationError):
    """Raised when blocking conflicts prevent policy activation."""

    def __init__(
        self,
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(
            code="POLICY_ACTIVATION_BLOCKED",
            message=(
                "The policy cannot be activated because blocking "
                "conflicts exist."
            ),
            status_code=409,
            details=details,
        )


class DatabaseUnavailableError(ApplicationError):
    """Raised when the MySQL connection cannot be established."""

    def __init__(self) -> None:
        super().__init__(
            code="DATABASE_UNAVAILABLE",
            message=(
                "The persistence service is temporarily unavailable."
            ),
            status_code=500,
        )


class EvaluationPersistenceError(ApplicationError):
    """Raised when evaluation results cannot be saved."""

    def __init__(
        self,
        message: str = "Failed to persist evaluation results.",
    ) -> None:
        super().__init__(
            code="EVALUATION_PERSISTENCE_ERROR",
            message=message,
            status_code=500,
        )


class AuditNotFoundError(ApplicationError):
    """Raised when an audit record does not exist."""

    def __init__(self, audit_id: str) -> None:
        super().__init__(
            code="AUDIT_NOT_FOUND",
            message="The requested audit record does not exist.",
            status_code=404,
            details=[
                {
                    "path": "audit_id",
                    "issue": "Unknown identifier",
                    "received": audit_id,
                }
            ],
        )
