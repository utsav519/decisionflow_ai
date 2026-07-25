from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.ai.schemas.provider import ProviderMetadata


class ExplanationResult(BaseModel):
    """
    Structured explanation returned by the Explainer.

    This model is used for:
    - Business explanation
    - Technical explanation
    - Customer-friendly explanation
    - Audit explanation

    The deterministic rule engine remains authoritative.
    This model only explains an already-produced decision.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    summary: str = Field(
        ...,
        min_length=1,
        description="Human-readable explanation of the final decision.",
    )

    key_factors: list[str] = Field(
        default_factory=list,
        description="Important factors contributing to the decision.",
    )

    winning_policy_reason: str | None = Field(
        default=None,
        description="Reason the winning policy was selected.",
    )

    competing_policy_note: str | None = Field(
        default=None,
        description="Optional note about competing policies.",
    )

    generated_by: Literal[
        "AI",
        "DETERMINISTIC_FALLBACK",
    ] = Field(
        ...,
        description="Indicates whether the explanation came from AI or fallback.",
    )

    fallback_used: bool = Field(
        default=False,
        description="Whether deterministic fallback was used.",
    )

    provider_metadata: ProviderMetadata | None = Field(
        default=None,
        description="Metadata from the AI provider. None for deterministic fallback.",
    )