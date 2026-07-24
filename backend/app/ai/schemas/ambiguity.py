from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.ai.schemas.provider import ProviderMetadata


class ClarificationQuestion(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    question: str = Field(..., min_length=1)
    reason: str = Field(..., min_length=1)


class AmbiguityFinding(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    field: str
    severity: Literal["LOW", "MEDIUM", "HIGH"]
    explanation: str
    clarification: ClarificationQuestion


class AmbiguityDetectionResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    has_ambiguity: bool

    findings: list[AmbiguityFinding] = Field(
        default_factory=list,
    )

    provider_metadata: ProviderMetadata | None = None