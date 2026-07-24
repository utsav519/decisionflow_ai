from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.ai.schemas.provider import ProviderMetadata


class ConflictingPolicy(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    policy_id: str
    policy_name: str
    priority: int
    decision: str


class ConflictReason(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    description: str = Field(..., min_length=1)
    severity: Literal["LOW", "MEDIUM", "HIGH"]


class ConflictAnalysisResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    has_conflict: bool

    conflicting_policies: list[ConflictingPolicy] = Field(
        default_factory=list,
    )

    reasons: list[ConflictReason] = Field(
        default_factory=list,
    )

    recommended_winner: str | None = None

    explanation: str

    provider_metadata: ProviderMetadata | None = None