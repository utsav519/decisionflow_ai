"""Official Decision API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status

from app.api.dependencies import (
    get_correlation_id,
    get_current_user,
    get_decision_service,
)
from app.schemas.common import StandardResponse
from app.schemas.decision import (
    DecisionDetailResponse,
    DecisionEvaluationRequest,
    DecisionEvaluationResponse,
)
from app.services.decision_service import DecisionService

router = APIRouter(
    prefix="/api/v1/decisions",
    tags=["Decisions"],
)


@router.post(
    "/evaluate",
    response_model=StandardResponse[DecisionEvaluationResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Evaluate a decision",
)
async def evaluate_decision(
    body: DecisionEvaluationRequest,
    response: Response,
    decision_service: DecisionService = Depends(
        get_decision_service
    ),
    correlation_id: str = Depends(get_correlation_id),
    actor_id: str = Depends(get_current_user),
) -> StandardResponse[DecisionEvaluationResponse]:
    result = await decision_service.evaluate(
        request=body,
        actor_id=actor_id,
        correlation_id=correlation_id,
    )

    response.headers["X-Correlation-ID"] = correlation_id

    return StandardResponse(
        success=True,
        data=result,
        meta={
            "domain": body.domain,
            "explanation_enabled": (
                body.options.include_explanation
            ),
        },
        correlation_id=correlation_id,
    )


@router.get(
    "/{evaluation_id}",
    response_model=StandardResponse[DecisionDetailResponse],
    summary="Retrieve a decision",
)
def get_decision(
    evaluation_id: str,
    response: Response,
    decision_service: DecisionService = Depends(
        get_decision_service
    ),
    correlation_id: str = Depends(get_correlation_id),
) -> StandardResponse[DecisionDetailResponse]:
    result = decision_service.get_decision(evaluation_id)

    response.headers["X-Correlation-ID"] = correlation_id

    return StandardResponse(
        success=True,
        data=result,
        correlation_id=correlation_id,
    )
