from fastapi import APIRouter, HTTPException

from app.ai.ambiguity_detector import AmbiguityDetector
from app.ai.conflict_assistant import ConflictAssistant
from app.ai.explainer import DecisionExplainer
from app.ai.providers.factory import get_llm_provider
from app.ai.test_case_generator import AITestCaseGenerator

router = APIRouter(
    prefix="/api/v1/ai",
    tags=["AI"],
)


@router.post("/policies/generate")
async def generate_policy() -> dict:
    """
    Placeholder endpoint for AI policy generation.

    The integration layer should later:
    - validate request
    - resolve provider
    - invoke AIPolicyGenerator
    """

    raise HTTPException(
        status_code=501,
        detail="AI policy generation not yet integrated.",
    )


@router.post("/policies/clarify")
async def clarify_policy() -> dict:
    """
    Placeholder endpoint for clarification flow.
    """

    raise HTTPException(
        status_code=501,
        detail="Clarification flow not yet integrated.",
    )


@router.post("/policies/check-conflicts")
async def check_conflicts() -> dict:
    """
    Placeholder endpoint for conflict explanation.
    """

    raise HTTPException(
        status_code=501,
        detail="Conflict explanation not yet integrated.",
    )


@router.post("/policies/generate-tests")
async def generate_tests() -> dict:
    """
    Placeholder endpoint for AI-generated test cases.
    """

    raise HTTPException(
        status_code=501,
        detail="Test generation not yet integrated.",
    )