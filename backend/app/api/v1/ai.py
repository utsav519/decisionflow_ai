from __future__ import annotations

import inspect
import json
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from app.ai.ambiguity_detector import AmbiguityDetector
from app.ai.conflict_assistant import ConflictAssistant
from app.ai.explainer import Explainer
from app.ai.policy_generator import PolicyGenerator
from app.ai.providers.factory import get_llm_provider
from app.ai.schemas.ambiguity import AmbiguityDetectionResult
from app.ai.schemas.conflict import ConflictAnalysisResult
from app.ai.schemas.explanation import ExplanationResult
from app.ai.schemas.policy_generation import (
    AIPolicyGenerationInput,
    AIPolicyGenerationResult,
)
from app.ai.schemas.test_case import TestCaseGenerationResult
from app.ai.test_case_generator import AITestCaseGenerator
from app.core.config import settings


router = APIRouter(
    prefix="/api/v1/ai",
    tags=["AI"],
)


class ClarifyPolicyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_text: str = Field(..., min_length=5)


class ConflictCheckRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_a: str = Field(..., min_length=5)
    policy_b: str = Field(..., min_length=5)


class GenerateTestsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_definition: str = Field(..., min_length=5)


class ExplainDecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_name: str = Field(..., min_length=1)
    decision: str = Field(..., min_length=1)
    input_data: dict[str, Any] | str


async def _resolve_result(value: Any) -> Any:
    """
    Support both asynchronous and synchronous service implementations.
    """

    if inspect.isawaitable(value):
        return await value

    return value


def _raise_ai_error(operation: str, exc: Exception) -> None:
    """
    Convert an unexpected AI service error into an HTTP response.

    Internal exception text is included during integration so failures
    remain diagnosable. Replace this with structured logging and a generic
    production error response before production deployment.
    """

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"{operation} failed: {exc}",
    ) from exc


@router.post(
    "/policies/generate",
    response_model=AIPolicyGenerationResult,
    status_code=status.HTTP_200_OK,
)
async def generate_policy(
    request: AIPolicyGenerationInput,
) -> AIPolicyGenerationResult:
    """Generate a structured policy from natural-language input."""

    try:
        provider = get_llm_provider(settings)
        service = PolicyGenerator(provider)

        result = service.generate(request)
        return await _resolve_result(result)

    except HTTPException:
        raise
    except Exception as exc:
        _raise_ai_error("AI policy generation", exc)


@router.post(
    "/policies/clarify",
    response_model=AmbiguityDetectionResult,
    status_code=status.HTTP_200_OK,
)
async def clarify_policy(
    request: ClarifyPolicyRequest,
) -> AmbiguityDetectionResult:
    """Detect ambiguity and produce clarification questions."""

    try:
        provider = get_llm_provider(settings)
        service = AmbiguityDetector(provider)

        result = service.analyze(request.policy_text)
        return await _resolve_result(result)

    except HTTPException:
        raise
    except Exception as exc:
        _raise_ai_error("AI ambiguity analysis", exc)


@router.post(
    "/policies/check-conflicts",
    response_model=ConflictAnalysisResult,
    status_code=status.HTTP_200_OK,
)
async def check_conflicts(
    request: ConflictCheckRequest,
) -> ConflictAnalysisResult:
    """Analyze two policy definitions for logical conflicts."""

    try:
        provider = get_llm_provider(settings)
        service = ConflictAssistant(provider)

        result = service.analyze(
            policy_a=request.policy_a,
            policy_b=request.policy_b,
        )
        return await _resolve_result(result)

    except HTTPException:
        raise
    except Exception as exc:
        _raise_ai_error("AI conflict analysis", exc)


@router.post(
    "/policies/generate-tests",
    response_model=TestCaseGenerationResult,
    status_code=status.HTTP_200_OK,
)
async def generate_tests(
    request: GenerateTestsRequest,
) -> TestCaseGenerationResult:
    """Generate positive, negative, boundary and missing-field test cases."""

    try:
        provider = get_llm_provider(settings)
        service = AITestCaseGenerator(provider)

        result = service.generate(request.policy_definition)
        return await _resolve_result(result)

    except HTTPException:
        raise
    except Exception as exc:
        _raise_ai_error("AI test-case generation", exc)


@router.post(
    "/decisions/explain",
    response_model=ExplanationResult,
    status_code=status.HTTP_200_OK,
)
async def explain_decision(
    request: ExplainDecisionRequest,
) -> ExplanationResult:
    """Explain a decision already produced by the deterministic rule engine."""

    try:
        provider = get_llm_provider(settings)
        service = Explainer(provider)

        if isinstance(request.input_data, str):
            serialized_input = request.input_data
        else:
            serialized_input = json.dumps(
                request.input_data,
                ensure_ascii=False,
                sort_keys=True,
            )

        result = service.explain(
            policy_name=request.policy_name,
            decision=request.decision,
            input_data=serialized_input,
        )
        return await _resolve_result(result)

    except HTTPException:
        raise
    except Exception as exc:
        _raise_ai_error("AI decision explanation", exc)
