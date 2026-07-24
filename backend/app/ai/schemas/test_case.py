from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.ai.schemas.provider import ProviderMetadata


class GeneratedTestCase(BaseModel):
    """
    Represents a single AI-generated test case for a policy.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    name: str = Field(
        ...,
        min_length=1,
        description="Human-readable name of the test case.",
    )

    category: Literal[
        "POSITIVE",
        "NEGATIVE",
        "BOUNDARY",
        "MISSING_FIELD",
        "CONFLICT",
    ]

    input: dict = Field(
        default_factory=dict,
        description="Input payload used for policy evaluation.",
    )

    expected_match: bool

    expected_decision: str = Field(
        ...,
        description="Expected decision for the supplied input.",
    )

    rationale: str = Field(
        ...,
        min_length=1,
        description="Reason why this test case exists.",
    )


class TestCaseGenerationResult(BaseModel):
    """
    Result returned by AITestCaseGenerator.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    generated_test_cases: list[GeneratedTestCase] = Field(
        default_factory=list,
    )

    provider_metadata: ProviderMetadata