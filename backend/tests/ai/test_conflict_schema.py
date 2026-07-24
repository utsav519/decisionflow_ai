import pytest
from pydantic import ValidationError

from app.ai.schemas.conflict import (
    ConflictAnalysisResult,
    ConflictReason,
    ConflictingPolicy,
)
from app.ai.schemas.provider import ProviderMetadata


def metadata():
    return ProviderMetadata(
        provider="mock",
        model="mock-v1",
        processing_time_ms=10,
    )


def test_valid_conflict():
    result = ConflictAnalysisResult(
        has_conflict=True,
        conflicting_policies=[
            ConflictingPolicy(
                policy_id="P1",
                policy_name="Reject High Risk",
                priority=100,
                decision="REJECT",
            ),
            ConflictingPolicy(
                policy_id="P2",
                policy_name="Approve Premium",
                priority=50,
                decision="APPROVE",
            ),
        ],
        reasons=[
            ConflictReason(
                description="Both policies match the same input.",
                severity="HIGH",
            )
        ],
        recommended_winner="P1",
        explanation="Higher priority policy wins.",
        provider_metadata=metadata(),
    )

    assert result.has_conflict
    assert len(result.conflicting_policies) == 2
    assert result.recommended_winner == "P1"


def test_invalid_severity():
    with pytest.raises(ValidationError):
        ConflictReason(
            description="Invalid",
            severity="CRITICAL",
        )


def test_optional_metadata():
    result = ConflictAnalysisResult(
        has_conflict=False,
        explanation="No conflict detected.",
    )

    assert result.provider_metadata is None