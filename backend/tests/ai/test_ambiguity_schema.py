import pytest
from pydantic import ValidationError

from app.ai.schemas.ambiguity import (
    AmbiguityDetectionResult,
    AmbiguityFinding,
    ClarificationQuestion,
)
from app.ai.schemas.provider import ProviderMetadata


def metadata():
    return ProviderMetadata(
        provider="mock",
        model="mock-v1",
        processing_time_ms=10,
    )


def test_valid_result():
    result = AmbiguityDetectionResult(
        has_ambiguity=True,
        findings=[
            AmbiguityFinding(
                field="credit_score",
                severity="HIGH",
                explanation="Credit score threshold is unclear.",
                clarification=ClarificationQuestion(
                    question="Should the threshold be inclusive?",
                    reason="Boundary is ambiguous.",
                ),
            )
        ],
        provider_metadata=metadata(),
    )

    assert result.has_ambiguity is True
    assert len(result.findings) == 1


def test_invalid_severity():
    with pytest.raises(ValidationError):
        AmbiguityFinding(
            field="credit_score",
            severity="CRITICAL",
            explanation="Invalid severity.",
            clarification=ClarificationQuestion(
                question="Q?",
                reason="R",
            ),
        )


def test_optional_metadata():
    result = AmbiguityDetectionResult(
        has_ambiguity=False,
    )

    assert result.provider_metadata is None