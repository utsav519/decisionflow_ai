from __future__ import annotations

from app.ai.schemas.explanation import ExplanationResult


def build_fallback_explanation(
    evaluation_result: dict,
    style: str = "BUSINESS",
) -> ExplanationResult:
    """
    Build a deterministic explanation without using an LLM.
    """

    decision = evaluation_result.get("decision", "MANUAL_REVIEW")

    decision_text = {
        "APPROVE": "approved",
        "REJECT": "rejected",
        "MANUAL_REVIEW": "sent for manual review",
    }.get(decision, str(decision).lower())
    winning_policy = evaluation_result.get("winning_policy")
    missing_fields = evaluation_result.get("missing_fields", [])
    matched_policies = evaluation_result.get("matched_policies", [])

    key_factors: list[str] = []

    if missing_fields:
        summary = (
            "The request requires manual review because required fields "
            f"were missing: {', '.join(missing_fields)}."
        )

        key_factors.append("Missing required input fields")

    elif winning_policy:
        policy_name = winning_policy.get("name", "Unknown Policy")

        summary = (
            f'The request was {decision_text} because policy "{policy_name}" '
            "matched and had the highest priority."
        )

        key_factors.append(f"Winning policy: {policy_name}")

        if len(matched_policies) > 1:
            key_factors.append(
                "Highest-priority conflict resolution applied."
            )

    else:
        summary = (
            "The request requires manual review because no active policy "
            "fully matched the supplied data."
        )

        key_factors.append("No matching active policy")

    return ExplanationResult(
        summary=summary,
        key_factors=key_factors,
        winning_policy_reason=(
            winning_policy.get("name")
            if winning_policy
            else None
        ),
        competing_policy_note=(
            "Highest-priority resolution applied."
            if len(matched_policies) > 1
            else None
        ),
        generated_by="DETERMINISTIC_FALLBACK",
        fallback_used=True,
        provider_metadata=None,
    )