from __future__ import annotations

from typing import Any, Type, TypeVar

from pydantic import BaseModel

from app.ai.schemas.explanation import ExplanationResult
from app.ai.schemas.provider import ProviderMetadata

from app.ai.exceptions import (
    AIOutputInvalidError,
    AIProviderTimeoutError,
    AIProviderUnavailableError,
)
from app.ai.providers.base import LLMProvider

T = TypeVar("T", bound=BaseModel)

class MockProvider(LLMProvider):
    """
    Deterministic mock implementation of LLMProvider.

    Used for:
    - Development
    - Offline demos
    - Unit testing
    """

    def __init__(
        self,
        settings: Any,
        *,
        simulate_timeout: bool = False,
        simulate_failure: bool = False,
    ):
        self._settings = settings
        self._simulate_timeout = simulate_timeout
        self._simulate_failure = simulate_failure

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def model_name(self) -> str:
        return "mock-v1"

    def _check_simulation(self) -> None:
        """
        Simulate provider failures for testing.
        """
        if self._simulate_failure:
            raise AIProviderUnavailableError(
                "Mock provider unavailable."
            )

        if self._simulate_timeout:
            raise AIProviderTimeoutError(
                "Mock provider timed out."
            )

    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
    ) -> T:
        """
        Return a deterministic structured response.

        Currently, no schemas are registered. This will be implemented
        in the next step.
        """
        self._check_simulation()

        if response_model is ExplanationResult:
            return self._build_explanation_result()  # type: ignore[return-value]

        raise AIOutputInvalidError(
            f"No mock response registered for {response_model.__name__}."
        )

    def generate_text(
        self,
        prompt: str,
    ) -> str:
        """
        Return a deterministic text response.
        """
        self._check_simulation()

        return "MockProvider deterministic response."

    def _provider_metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            provider=self.provider_name,
            model=self.model_name,
            processing_time_ms=5,
            fallback_used=False,
            retry_count=0,
            request_tokens=50,
            response_tokens=100,
            estimated_cost=0.0,
        )

    def _build_explanation_result(self) -> ExplanationResult:
        return ExplanationResult(
            summary="Loan approved because the applicant satisfies all policy conditions.",
            key_factors=[
                "Credit score exceeds minimum threshold.",
                "Fraud risk is acceptable.",
                "Income verification succeeded.",
            ],
            winning_policy_reason="Highest priority matching policy was selected.",
            competing_policy_note=None,
            generated_by="AI",
            fallback_used=False,
            provider_metadata=self._provider_metadata(),
        )

