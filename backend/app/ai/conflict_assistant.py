from __future__ import annotations

from app.ai.providers.base import LLMProvider
from app.ai.schemas.conflict import ConflictAnalysisResult
from app.ai.prompts.conflict_explanation import SYSTEM_PROMPT


class ConflictAssistant:
    """
    Analyze conflicts between policies.
    """

    def __init__(self, provider: LLMProvider):
        self._provider = provider

    async def analyze(
        self,
        policy_a: str,
        policy_b: str,
    ) -> ConflictAnalysisResult:

        user_prompt = self._build_prompt(
            policy_a,
            policy_b,
        )

        return await self._provider.generate_structured(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
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