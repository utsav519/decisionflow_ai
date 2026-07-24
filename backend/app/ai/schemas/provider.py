from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ProviderMetadata(BaseModel):
    """
    Common metadata returned by every LLM provider.

    This model hides provider-specific SDK details and provides a
    unified structure for downstream services.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    provider: str = Field(
        ...,
        description="LLM provider name (openai, gemini, groq, mock, etc.)",
    )

    model: str = Field(
        ...,
        description="Model used for inference.",
    )

    processing_time_ms: int = Field(
        ...,
        ge=0,
        description="Total processing time in milliseconds.",
    )

    fallback_used: bool = Field(
        default=False,
        description="Whether deterministic fallback was used.",
    )

    retry_count: int = Field(
        default=0,
        ge=0,
        description="Number of retry attempts.",
    )

    request_tokens: int | None = Field(
        default=None,
        ge=0,
        description="Prompt tokens consumed (if available).",
    )

    response_tokens: int | None = Field(
        default=None,
        ge=0,
        description="Completion tokens consumed (if available).",
    )

    estimated_cost: float | None = Field(
        default=None,
        ge=0,
        description="Estimated request cost in USD.",
    )