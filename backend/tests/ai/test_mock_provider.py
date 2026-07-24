import pytest

from app.ai.exceptions import (
    AIOutputInvalidError,
    AIProviderTimeoutError,
    AIProviderUnavailableError,
)
from app.ai.providers.mock_provider import MockProvider

from app.ai.schemas.explanation import ExplanationResult
from app.ai.schemas.ambiguity import AmbiguityDetectionResult
from app.ai.schemas.conflict import ConflictAnalysisResult
from app.ai.schemas.policy_generation import (
    AIPolicyGenerationResult,
)


def test_provider_name():
    provider = MockProvider(settings=None)

    assert provider.provider_name == "mock"


def test_model_name():
    provider = MockProvider(settings=None)

    assert provider.model_name == "mock-v1"


@pytest.mark.asyncio
async def test_generate_text():
    provider = MockProvider(settings=None)

    text = await provider.generate_text(
        system_prompt="You are an AI assistant.",
        user_prompt="hello",
    )

    assert text == "MockProvider deterministic response."


@pytest.mark.asyncio
async def test_timeout():
    provider = MockProvider(
        settings=None,
        simulate_timeout=True,
    )

    with pytest.raises(AIProviderTimeoutError):
        await provider.generate_text(
            system_prompt="system",
            user_prompt="hello",
        )


@pytest.mark.asyncio
async def test_failure():
    provider = MockProvider(
        settings=None,
        simulate_failure=True,
    )

    with pytest.raises(AIProviderUnavailableError):
        await provider.generate_text(
            system_prompt="system",
            user_prompt="hello",
        )


@pytest.mark.asyncio
async def test_unknown_schema():
    provider = MockProvider(settings=None)

    with pytest.raises(AIOutputInvalidError):
        await provider.generate_structured(
            system_prompt="system",
            user_prompt="prompt",
            response_model=dict,
        )


@pytest.mark.asyncio
async def test_generate_explanation():
    provider = MockProvider(settings=None)

    result = await provider.generate_structured(
        system_prompt="system",
        user_prompt="Explain decision",
        response_model=ExplanationResult,
    )

    assert isinstance(result, ExplanationResult)
    assert result.generated_by == "AI"
    assert result.fallback_used is False
    assert len(result.key_factors) == 3


@pytest.mark.asyncio
async def test_generate_ambiguity():
    provider = MockProvider(settings=None)

    result = await provider.generate_structured(
        system_prompt="system",
        user_prompt="Find ambiguities",
        response_model=AmbiguityDetectionResult,
    )

    assert isinstance(result, AmbiguityDetectionResult)
    assert result.has_ambiguity is True
    assert len(result.findings) == 2
    assert result.findings[0].severity == "HIGH"


@pytest.mark.asyncio
async def test_generate_conflict():
    provider = MockProvider(settings=None)

    result = await provider.generate_structured(
        system_prompt="system",
        user_prompt="Analyze conflict",
        response_model=ConflictAnalysisResult,
    )

    assert isinstance(result, ConflictAnalysisResult)
    assert result.has_conflict is True
    assert len(result.conflicting_policies) == 2
    assert result.recommended_winner == "P001"


@pytest.mark.asyncio
async def test_generate_policy():
    provider = MockProvider(settings=None)

    result = await provider.generate_structured(
        system_prompt="system",
        user_prompt="Generate policy",
        response_model=AIPolicyGenerationResult,
    )

    assert isinstance(result, AIPolicyGenerationResult)
    assert result.validation_status == "VALID"
    assert result.ai_confidence > 0.9
    assert result.generated_policy.policy_name == "Approve Premium Customer"
    assert len(result.generated_policy.condition_group.conditions) == 3