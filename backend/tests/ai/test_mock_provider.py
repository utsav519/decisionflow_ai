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


def test_provider_name():
    provider = MockProvider(settings=None)

    assert provider.provider_name == "mock"


def test_model_name():
    provider = MockProvider(settings=None)

    assert provider.model_name == "mock-v1"


def test_generate_text():
    provider = MockProvider(settings=None)

    text = provider.generate_text("hello")

    assert text == "MockProvider deterministic response."


def test_timeout():
    provider = MockProvider(
        settings=None,
        simulate_timeout=True,
    )

    with pytest.raises(AIProviderTimeoutError):
        provider.generate_text("hello")


def test_failure():
    provider = MockProvider(
        settings=None,
        simulate_failure=True,
    )

    with pytest.raises(AIProviderUnavailableError):
        provider.generate_text("hello")


def test_unknown_schema():
    provider = MockProvider(settings=None)

    with pytest.raises(AIOutputInvalidError):
        provider.generate_structured(
            "prompt",
            dict,
        )

def test_generate_explanation():
    provider = MockProvider(settings=None)

    result = provider.generate_structured(
        "Explain decision",
        ExplanationResult,
    )

    assert isinstance(result, ExplanationResult)
    assert result.generated_by == "AI"
    assert result.fallback_used is False
    assert len(result.key_factors) == 3

def test_generate_ambiguity():
    provider = MockProvider(settings=None)

    result = provider.generate_structured(
        "Find ambiguities",
        AmbiguityDetectionResult,
    )

    assert isinstance(result, AmbiguityDetectionResult)
    assert result.has_ambiguity is True
    assert len(result.findings) == 2
    assert result.findings[0].severity == "HIGH"

def test_generate_conflict():
    provider = MockProvider(settings=None)

    result = provider.generate_structured(
        "Analyze conflict",
        ConflictAnalysisResult,
    )

    assert isinstance(result, ConflictAnalysisResult)
    assert result.has_conflict is True
    assert len(result.conflicting_policies) == 2
    assert result.recommended_winner == "P001"