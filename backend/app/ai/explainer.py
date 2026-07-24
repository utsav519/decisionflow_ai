from __future__ import annotations

from app.ai.providers.base import LLMProvider
from app.ai.schemas.explanation import ExplanationResult
from app.ai.prompts.decision_explanation import SYSTEM_PROMPT


class Explainer:
    """
    Generate a human-readable explanation for a policy decision.
    """

    def __init__(self, provider: LLMProvider):
        self._provider = provider

    async def explain(
        self,
        policy_name: str,
        decision: str,
        input_data: str,
    ) -> ExplanationResult:

        user_prompt = self._build_prompt(
            policy_name=policy_name,
            decision=decision,
            input_data=input_data,
        )

        return await self._provider.generate_structured(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=ExplanationResult,
        )

    def _build_prompt(
        self,
        *,
        policy_name: str,
        decision: str,
        input_data: str,
    ) -> str:
        return (
            "Explain why the following policy decision was made.\n\n"
            f"Policy: {policy_name}\n"
            f"Decision: {decision}\n"
            f"Input Data:\n{input_data}"
        )