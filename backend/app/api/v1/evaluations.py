"""
Evaluation API router — execute evaluations and retrieve results.

Spec reference: API contract §5-6
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.api.dependencies import get_correlation_id, get_current_user
from app.db.session import get_db
from app.schemas.evaluation import EvaluationRequest
from app.services.evaluation_service import EvaluationService

router = APIRouter(prefix="/evaluations", tags=["Evaluations"])


@router.post("", status_code=201)
def execute_evaluation(
    body: EvaluationRequest,
    response: Response,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
    user_id: str = Depends(get_current_user),
) -> dict:
    """Execute a decision evaluation against active policies."""
    service = EvaluationService(db)
    result = service.evaluate(
        domain=body.domain,
        customer_id=body.customer_id,
        data=body.data,
        options=body.options,
        performed_by=user_id,
        correlation_id=correlation_id,
    )

    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": result,
        "correlation_id": correlation_id,
    }


@router.get("/{evaluation_id}")
def get_evaluation(
    evaluation_id: str,
    response: Response,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
) -> dict:
    """Retrieve a stored evaluation with full rule results."""
    service = EvaluationService(db)
    result = service.get_evaluation(evaluation_id)

    response.headers["X-Correlation-ID"] = correlation_id
    return {
        "success": True,
        "data": result,
        "correlation_id": correlation_id,
    }
