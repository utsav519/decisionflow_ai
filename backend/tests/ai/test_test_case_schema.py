import pytest
from pydantic import ValidationError

from app.ai.schemas.provider import ProviderMetadata
from app.ai.schemas.test_case import (
    GeneratedTestCase,
    TestCaseGenerationResult,
)


def build_metadata() -> ProviderMetadata:
    return ProviderMetadata(
        provider="mock",
        model="mock-v1",
        processing_time_ms=5,
    )


def test_generated_test_case_valid():
    test_case = GeneratedTestCase(
        name="Positive Test",
        category="POSITIVE",
        input={
            "credit_score": 750,
            "fraud_risk_score": 0.4,
        },
        expected_match=True,
        expected_decision="APPROVE",
        rationale="Valid approval case.",
    )

    assert test_case.name == "Positive Test"
    assert test_case.category == "POSITIVE"
    assert test_case.expected_match is True
    assert test_case.expected_decision == "APPROVE"


def test_generated_test_case_invalid_category():
    with pytest.raises(ValidationError):
        GeneratedTestCase(
            name="Bad Category",
            category="INVALID",
            input={},
            expected_match=False,
            expected_decision="REJECT",
            rationale="Should fail.",
        )


def test_generated_test_case_empty_name():
    with pytest.raises(ValidationError):
        GeneratedTestCase(
            name="",
            category="NEGATIVE",
            input={},
            expected_match=False,
            expected_decision="REJECT",
            rationale="Should fail.",
        )


def test_test_case_generation_result():
    result = TestCaseGenerationResult(
        generated_test_cases=[
            GeneratedTestCase(
                name="Boundary",
                category="BOUNDARY",
                input={"credit_score": 750},
                expected_match=True,
                expected_decision="APPROVE",
                rationale="Boundary test.",
            )
        ],
        provider_metadata=build_metadata(),
    )

    assert len(result.generated_test_cases) == 1
    assert result.provider_metadata.provider == "mock"


def test_serialization():
    tc = GeneratedTestCase(
        name="Serialize",
        category="POSITIVE",
        input={"x": 1},
        expected_match=True,
        expected_decision="APPROVE",
        rationale="Serialization test.",
    )

    data = tc.model_dump()

    assert data["name"] == "Serialize"
    assert data["category"] == "POSITIVE"
    assert data["expected_match"] is True