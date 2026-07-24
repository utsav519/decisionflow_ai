<<<<<<< HEAD
"""FastAPI dependency providers.

Concrete dependencies will be added as backend and AI modules are integrated.
"""


def get_decision_service():
    raise RuntimeError(
        "DecisionService is not available until backend and AI modules are integrated."
    )
=======
"""
FastAPI dependency injection providers.

Provides request-scoped DB sessions, correlation ID extraction,
and actor context for audit trails.

Spec reference: §25 Dependency Injection
"""

from __future__ import annotations

from fastapi import Depends, Header, Request
from sqlalchemy.orm import Session

from app.core.ids import new_correlation_id
from app.db.session import get_db


def get_correlation_id(
    x_correlation_id: str | None = Header(None),
) -> str:
    """Extract or generate a correlation ID from request headers.

    If the client sends X-Correlation-ID, use it.
    Otherwise, generate a new one with the cor_ prefix.
    """
    return x_correlation_id or new_correlation_id()


def get_current_user(
    x_user_id: str | None = Header(None),
) -> str:
    """Extract the actor identity from request headers.

    Returns 'demo_user' if no header is present.
    """
    return x_user_id or "demo_user"
>>>>>>> origin/feature/backend-rule-engine
