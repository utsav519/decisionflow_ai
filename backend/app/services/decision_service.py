"""Central decision orchestration.

The full implementation will be completed after the backend and AI module
handoffs provide stable service interfaces.
"""

from typing import Any


class DecisionService:
    """Coordinates deterministic decisioning and AI-assisted explanation."""

    async def evaluate(
        self,
        *,
        request: Any,
        actor_id: str,
        correlation_id: str,
    ) -> Any:
        raise NotImplementedError(
            "DecisionService will be implemented after backend and AI integration."
        )
