from __future__ import annotations

from app.ai.providers.base import LLMProvider
from app.ai.schemas.ambiguity import AmbiguityDetectionResult


class AmbiguityDetector:
    """
    Detect ambiguities in a natural language policy.
    """

    def __init__(self, provider: LLMProvider):
        self._provider = provider

    def analyze(
        self,
        policy_text: str,
    ) -> AmbiguityDetectionResult:
        prompt = self._build_prompt(policy_text)

        return self._provider.generate_structured(
            prompt=prompt,
            response_model=AmbiguityDetectionResult,
        )

    def _build_prompt(self, policy_text: str) -> str:
        return (
            "Identify ambiguities in the following policy.\n\n"
            f"{policy_text}"
        )