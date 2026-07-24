from __future__ import annotations

from app.ai.providers.base import LLMProvider
from app.ai.schemas.ambiguity import AmbiguityDetectionResult
from app.ai.prompts.ambiguity_detection import SYSTEM_PROMPT


class AmbiguityDetector:
    """
    Detect ambiguities in a natural language policy.
    """

    def __init__(self, provider: LLMProvider):
        self._provider = provider

    async def analyze(
        self,
        policy_text: str,
    ) -> AmbiguityDetectionResult:

        user_prompt = self._build_prompt(policy_text)

        return await self._provider.generate_structured(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=AmbiguityDetectionResult,
        )

    def _build_prompt(self, policy_text: str) -> str:
        return (
            "Identify ambiguities in the following policy.\n\n"
            f"{policy_text}"
        )