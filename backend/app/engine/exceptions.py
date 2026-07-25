"""
Engine-specific exceptions.

These are raised during condition evaluation and never leak to API consumers.

Spec reference: §34 Exception Types (engine subset)
"""

from app.core.exceptions import ApplicationError


class EngineError(ApplicationError):
    """Base for all engine errors."""

    def __init__(self, code: str, message: str, **kwargs):
        super().__init__(code=code, message=message, status_code=400, **kwargs)


class UnsupportedOperatorError(EngineError):
    """Raised when an operator is not registered."""

    def __init__(self, operator: str):
        super().__init__(
            code="UNSUPPORTED_OPERATOR",
            message=f"The operator '{operator}' is not supported.",
            details=[{"path": "operator", "issue": "Unsupported operator", "received": operator}],
        )


class OperatorTypeError(EngineError):
    """Raised when operand types are incompatible."""

    def __init__(self, operator: str, expected_type: str, received_value):
        super().__init__(
            code="OPERATOR_TYPE_ERROR",
            message=f"Type mismatch for operator '{operator}'.",
            details=[
                {"path": "value", "issue": f"Expected {expected_type}", "received": str(received_value)}
            ],
        )
