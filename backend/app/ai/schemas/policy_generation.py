from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.ai.schemas.provider import ProviderMetadata
from app.ai.schemas.test_case import GeneratedTestCase


class GeneratedCondition(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    field: str
    operator: str
    value: object


class GeneratedConditionGroup(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    logical_operator: Literal["AND", "OR"] = "AND"
    conditions: list[GeneratedCondition] = Field(default_factory=list)


class GeneratedPolicy(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    policy_name: str
    priority: int
    decision: str
    condition_group: GeneratedConditionGroup


class AmbiguityItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    field: str
    reason: str
    suggested_clarification: str


class AssumptionItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    description: str


class AIWarning(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    message: str


class AIPolicyGenerationInput(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    policy_text: str = Field(..., min_length=5)
    domain: str
    preferred_decision: str | None = None
    preferred_priority: int | None = None
    generate_test_cases: bool = True
    active_policies: list[dict] = Field(default_factory=list)


class AIPolicyGenerationResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    generated_policy: GeneratedPolicy

    ai_confidence: float = Field(..., ge=0, le=1)

    validation_status: Literal[
        "VALID",
        "WARNING",
        "FAILED",
    ]

    warnings: list[AIWarning] = Field(default_factory=list)

    ambiguities: list[AmbiguityItem] = Field(default_factory=list)

    assumptions: list[AssumptionItem] = Field(default_factory=list)

    suggested_test_cases: list[GeneratedTestCase] = Field(default_factory=list)

    provider_metadata: ProviderMetadata