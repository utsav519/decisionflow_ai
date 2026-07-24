from __future__ import annotations

from app.ai.providers.base import LLMProvider
from app.ai.schemas.conflict import ConflictAnalysisResult


class ConflictAssistant:
    """
    Analyze conflicts between policies.
    """

    def __init__(self, provider: LLMProvider):
        self._provider = provider

    def analyze(
        self,
        policy_a: str,
        policy_b: str,
    ) -> ConflictAnalysisResult:
        prompt = self._build_prompt(
            policy_a,
            policy_b,
        )

        return self._provider.generate_structured(
            prompt=prompt,
            response_model=ConflictAnalysisResult,
        )

    def _build_prompt(
        self,
        policy_a: str,
        policy_b: str,
    ) -> str:
        return (
            "Analyze conflicts between these policies.\n\n"
            f"Policy A:\n{policy_a}\n\n"
            f"Policy B:\n{policy_b}"
        )