"""Wrapper around AI explanation and deterministic fallback logic.

The concrete AI interfaces will be connected after the AI module handoff.
"""


class ExplanationService:
    async def explain(self, *, evidence, correlation_id: str):
        raise NotImplementedError(
            "ExplanationService will be implemented after AI integration."
        )
