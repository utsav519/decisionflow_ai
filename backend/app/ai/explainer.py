from __future__ import annotations

from app.ai.providers.base import LLMProvider
from app.ai.schemas.explanation import ExplanationResult


class Explainer:
    """
    Generate a human-readable explanation for a policy decision.
    """

    def __init__(self, provider: LLMProvider):
        self._provider = provider

    def explain(
        self,
        policy_name: str,
        decision: str,
        input_data: str,
    ) -> ExplanationResult:
        """
        Generate an explanation for the supplied policy decision.
        """
        prompt = self._build_prompt(
            policy_name=policy_name,
            decision=decision,
            input_data=input_data,
        )

        return self._provider.generate_structured(
            prompt=prompt,
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