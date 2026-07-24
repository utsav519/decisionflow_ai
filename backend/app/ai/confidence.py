from __future__ import annotations

from app.ai.schemas.policy_generation import AIWarning


class AIPolicyConfidenceCalculator:
    """
    Calculates a deterministic confidence score for AI-generated policies.

    Confidence reflects how safely a natural-language policy
    was converted into a structured policy candidate.
    """

    def calculate(
        self,
        *,
        policy_text: str,
        generated_policy: dict | None,
        ambiguities: list,
        assumptions: list[str],
        warnings: list[AIWarning],
        local_validation_errors: list[dict],
        provider_fallback: bool = False,
    ) -> int:
        score = 100

        # -----------------------------
        # Ambiguity penalties
        # -----------------------------
        for ambiguity in ambiguities:
            severity = getattr(ambiguity, "severity", "WARNING")

            if severity == "BLOCKING":
                score -= 25
            elif severity == "WARNING":
                score -= 10

        # -----------------------------
        # Validation errors
        # -----------------------------
        for error in local_validation_errors:
            code = error.get("code", "")

            if code == "UNSUPPORTED_FIELD":
                score -= 30

            elif code == "UNSUPPORTED_OPERATOR":
                score -= 25

            elif code == "MISSING_THRESHOLD":
                score -= 20

            else:
                score -= 20

        # -----------------------------
        # Warnings
        # -----------------------------
        warning_codes = {
            warning.code
            for warning in warnings
            if hasattr(warning, "code")
        }

        if "INFERRED_DECISION" in warning_codes:
            score -= 15

        if "INFERRED_PRIORITY" in warning_codes:
            score -= 5

        # -----------------------------
        # Assumptions
        # -----------------------------
        score -= min(len(assumptions) * 3, 15)

        # -----------------------------
        # Provider fallback
        # -----------------------------
        if provider_fallback:
            score -= 10

        # -----------------------------
        # Missing generated policy
        # -----------------------------
        if generated_policy is None:
            score = min(score, 40)

        return max(0, min(score, 100))