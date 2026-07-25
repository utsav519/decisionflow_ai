"""FastAPI dependency injection providers."""

from __future__ import annotations

import logging

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.ai.explainer import DecisionExplainer
from app.ai.providers.factory import get_llm_provider
from app.core.config import get_settings
from app.core.ids import new_correlation_id
from app.db.session import get_db
from app.repositories.evaluation_repository import EvaluationRepository
from app.services.audit_service import AuditService
from app.services.decision_service import DecisionService
from app.services.evaluation_service import EvaluationService
from app.services.explanation_service import ExplanationService

logger = logging.getLogger(__name__)


def get_correlation_id(
    x_correlation_id: str | None = Header(None),
) -> str:
    """Return the supplied correlation ID or generate one."""
    return x_correlation_id or new_correlation_id()


def get_current_user(
    x_user_id: str | None = Header(None),
) -> str:
    """Return the request actor or the demo user."""
    return x_user_id or "demo_user"


def get_explanation_service() -> ExplanationService:
    """Create the AI explanation wrapper.

    Provider construction failures degrade safely to deterministic fallback.
    """
    settings = get_settings()

    if not settings.ENABLE_AI_EXPLANATION:
        return ExplanationService(explainer=None)

    try:
        provider = get_llm_provider(settings)
        explainer = DecisionExplainer(provider)
        return ExplanationService(explainer=explainer)
    except Exception as exc:
        logger.warning(
            "AI provider initialization failed; using deterministic fallback: %s",
            type(exc).__name__,
        )
        return ExplanationService(explainer=None)


def get_evaluation_service(
    db: Session = Depends(get_db),
) -> EvaluationService:
    return EvaluationService(db)


def get_evaluation_repository(
    db: Session = Depends(get_db),
) -> EvaluationRepository:
    return EvaluationRepository(db)


def get_audit_service(
    db: Session = Depends(get_db),
) -> AuditService:
    return AuditService(db)


def get_decision_service(
    db: Session = Depends(get_db),
    evaluation_service: EvaluationService = Depends(
        get_evaluation_service
    ),
    evaluation_repository: EvaluationRepository = Depends(
        get_evaluation_repository
    ),
    audit_service: AuditService = Depends(get_audit_service),
    explanation_service: ExplanationService = Depends(
        get_explanation_service
    ),
) -> DecisionService:
    return DecisionService(
        db=db,
        evaluation_service=evaluation_service,
        evaluation_repository=evaluation_repository,
        audit_service=audit_service,
        explanation_service=explanation_service,
    )
