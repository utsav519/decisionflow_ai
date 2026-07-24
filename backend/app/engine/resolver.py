"""
Priority resolver.

When multiple policies match, resolves a single deterministic decision.

Resolution order (spec §22):
  1. Highest priority number wins.
  2. REJECT beats MANUAL_REVIEW beats APPROVE at same priority.
  3. Higher version number wins after same priority and same decision.
  4. Lexicographically smallest policy ID breaks the final tie.

If no policies match, falls back to MANUAL_REVIEW.

Pure function — no DB, no AI.
"""

from __future__ import annotations

import logging

from app.engine.result_models import (
    EngineEvaluationResult,
    PolicyEvaluationResult,
    ResolutionResult,
)

logger = logging.getLogger(__name__)

# Decision weight for tie-breaking: higher = wins
_DECISION_WEIGHT = {
    "REJECT": 3,
    "MANUAL_REVIEW": 2,
    "APPROVE": 1,
}


def _sort_key(result: PolicyEvaluationResult) -> tuple:
    """Generate a deterministic sort key for a matched policy.

    Sort descending by:
      1. priority (higher first)
      2. decision weight (REJECT > MANUAL_REVIEW > APPROVE)
      3. version (higher first)
    Then ascending by:
      4. policy_id (lex smallest first — tie-breaker)
    """
    return (
        -result.priority,
        -_DECISION_WEIGHT.get(result.decision, 0),
        -result.policy_version,
        result.policy_id,
    )


def resolve(evaluation: EngineEvaluationResult) -> ResolutionResult:
    """Resolve a single winning decision from matched policies.

    Args:
        evaluation: The output of the evaluator with matched/unmatched/skipped.

    Returns:
        ResolutionResult with the winning policy, decision, and reasoning.
    """
    matched = evaluation.matched

    if not matched:
        return ResolutionResult(
            decision="MANUAL_REVIEW",
            winning_policy_id=None,
            winning_policy_version=None,
            strategy="no_match_fallback",
            reason="No policies matched the input data. Falling back to MANUAL_REVIEW.",
            tie_breaker_used=False,
            competing_policy_ids=[],
        )

    if len(matched) == 1:
        winner = matched[0]
        return ResolutionResult(
            decision=winner.decision,
            winning_policy_id=winner.policy_id,
            winning_policy_version=winner.policy_version,
            strategy="single_match",
            reason=f"Only one policy matched: '{winner.policy_name}'.",
            tie_breaker_used=False,
            competing_policy_ids=[winner.policy_id],
        )

    # Multiple matches — sort by resolution rules
    sorted_matches = sorted(matched, key=_sort_key)
    winner = sorted_matches[0]
    competing_ids = [r.policy_id for r in sorted_matches]

    # Determine what kind of tie-breaking was needed
    runner_up = sorted_matches[1]
    tie_breaker_used = False
    strategy = "priority"
    reason_parts = [f"Winner: '{winner.policy_name}' (priority={winner.priority})."]

    if winner.priority == runner_up.priority:
        if _DECISION_WEIGHT.get(winner.decision, 0) != _DECISION_WEIGHT.get(runner_up.decision, 0):
            strategy = "decision_precedence"
            reason_parts.append(
                f"{winner.decision} beats {runner_up.decision} at same priority."
            )
        elif winner.policy_version != runner_up.policy_version:
            strategy = "version"
            reason_parts.append(
                f"Higher version (v{winner.policy_version}) wins over v{runner_up.policy_version}."
            )
        else:
            strategy = "policy_id"
            tie_breaker_used = True
            reason_parts.append(
                f"Tie broken by policy ID: '{winner.policy_id}' < '{runner_up.policy_id}'."
            )

    return ResolutionResult(
        decision=winner.decision,
        winning_policy_id=winner.policy_id,
        winning_policy_version=winner.policy_version,
        strategy=strategy,
        reason=" ".join(reason_parts),
        tie_breaker_used=tie_breaker_used,
        competing_policy_ids=competing_ids,
    )


class PriorityResolver:
    """Wrapper class for integration compatibility."""

    @staticmethod
    def resolve(matched_policies: list[PolicyEvaluationResult]) -> ResolutionResult:
        # Create a dummy EngineEvaluationResult with just the matched policies
        dummy_evaluation = EngineEvaluationResult(
            matched=matched_policies,
            unmatched=[],
            skipped=[],
            evaluation_time_ms=0.0,
            warnings=[]
        )
        return resolve(dummy_evaluation)
