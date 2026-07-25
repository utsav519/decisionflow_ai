"""AI explanation wrapper with deterministic fallback."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

from app.ai.explainer import DecisionExplainer
from app.ai.fallback import build_fallback_explanation
from app.ai.schemas.explanation import ExplanationResult

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ExplanationOutcome:
    """Explanation plus non-fatal warnings."""

    explanation: ExplanationResult
    warnings: list[dict[str, str]]


class ExplanationService:
    """Protect deterministic decisioning from AI-provider failures."""

    def __init__(
        self,
        explainer: DecisionExplainer | None,
    ) -> None:
        self._explainer = explainer

    async def explain(
        self,
        *,
        evidence: dict[str, Any],
        correlation_id: str,
    ) -> ExplanationOutcome:
        fallback = build_fallback_explanation(evidence)

        winning_policy = evidence.get("winning_policy") or {}
        decision = str(
            evidence.get("decision", "MANUAL_REVIEW")
        )
        missing_fields = evidence.get("missing_fields") or []

        # Do not ask AI to fill gaps in incomplete deterministic evidence.
        if (
            not winning_policy
            or missing_fields
            or decision == "MANUAL_REVIEW"
        ):
            return ExplanationOutcome(
                explanation=fallback,
                warnings=[],
            )

        if self._explainer is None:
            return ExplanationOutcome(
                explanation=fallback,
                warnings=[
                    {
                        "code": "AI_EXPLANATION_DISABLED",
                        "message": (
                            "A deterministic explanation was provided because "
                            "AI explanation is disabled."
                        ),
                    }
                ],
            )

        policy_name = winning_policy.get(
            "name",
            "No matching policy",
        )

        try:
            explanation = await self._explainer.explain(
                policy_name=policy_name,
                decision=decision,
                input_data=json.dumps(
                    evidence,
                    sort_keys=True,
                    default=str,
                ),
            )

            return ExplanationOutcome(
                explanation=explanation,
                warnings=[],
            )

        except Exception as exc:
            logger.warning(
                "AI explanation failed correlation_id=%s error_type=%s",
                correlation_id,
                type(exc).__name__,
            )

            return ExplanationOutcome(
                explanation=fallback,
                warnings=[
                    {
                        "code": "AI_EXPLANATION_UNAVAILABLE",
                        "message": (
                            "A deterministic explanation was provided because "
                            "the AI explanation service was unavailable."
                        ),
                    }
                ],
            )
