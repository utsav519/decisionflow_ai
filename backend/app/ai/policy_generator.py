from __future__ import annotations

from app.ai.providers.base import LLMProvider
from app.ai.schemas.policy_generation import (
    AIPolicyGenerationInput,
    AIPolicyGenerationResult,
)


class PolicyGenerator:
    """
    Service responsible for generating structured policies from
    natural language descriptions.
    """

    def __init__(self, provider: LLMProvider):
        self._provider = provider

    def generate(
        self,
        request: AIPolicyGenerationInput,
    ) -> AIPolicyGenerationResult:
        """
        Generate a policy using the configured AI provider.
        """

        prompt = self._build_prompt(request)

        return self._provider.generate_structured(
            prompt=prompt,
            response_model=AIPolicyGenerationResult,
        )

    def _build_prompt(
        self,
        request: AIPolicyGenerationInput,
    ) -> str:
        return (
            "Generate a structured policy from the following description.\n\n"
            f"Domain: {request.domain}\n"
            f"Policy:\n{request.policy_text}"
        )