"""
Decision confidence calculator.

Produces a deterministic 0-100 confidence score based on observable factors.
Pure function — no DB, no AI, no randomness.

Spec reference: §23 Confidence Calculator
"""

from __future__ import annotations

from app.engine.result_models import (
    ConfidenceFactor,
    DecisionConfidenceResult,
    EngineEvaluationResult,
    ResolutionResult,
)


def calculate_confidence(
    evaluation: EngineEvaluationResult,
    resolution: ResolutionResult,
) -> DecisionConfidenceResult:
    """Calculate a decision confidence score from evaluation + resolution.

    Scoring factors:
      +40  A policy matched (vs. fallback)
      +20  Only one policy matched (no ambiguity)
      -10  Per competing policy beyond the first
      +15  No skipped policies (all data was present)
      +10  No evaluation warnings
      +15  High priority winner (top of stack)
      -20  Tie-breaker was needed (fragile decision)

    Clamped to [0, 100].

    Args:
        evaluation: Output from evaluate_policies.
        resolution: Output from resolve.

    Returns:
        DecisionConfidenceResult with score and explanation factors.
    """
    factors: list[ConfidenceFactor] = []
    score = 0

    # Factor 1: Did any policy match?
    if resolution.winning_policy_id is not None:
        score += 40
        factors.append(ConfidenceFactor(
            name="policy_matched",
            impact=40,
            description="At least one policy matched the input data.",
        ))
    else:
        factors.append(ConfidenceFactor(
            name="no_match_fallback",
            impact=0,
            description="No policies matched. Using MANUAL_REVIEW fallback.",
        ))

    # Factor 2: Single match vs. multiple
    num_matched = len(evaluation.matched)
    if num_matched == 1:
        score += 20
        factors.append(ConfidenceFactor(
            name="single_match",
            impact=20,
            description="Exactly one policy matched — no ambiguity.",
        ))
    elif num_matched > 1:
        penalty = (num_matched - 1) * 10
        score -= penalty
        factors.append(ConfidenceFactor(
            name="multiple_matches",
            impact=-penalty,
            description=f"{num_matched} policies matched. Ambiguity penalty applied.",
        ))

    # Factor 3: No skipped policies
    if len(evaluation.skipped) == 0:
        score += 15
        factors.append(ConfidenceFactor(
            name="no_skipped",
            impact=15,
            description="All policies were fully evaluable (no missing fields).",
        ))
    else:
        penalty = min(len(evaluation.skipped) * 5, 15)
        score -= penalty
        factors.append(ConfidenceFactor(
            name="skipped_policies",
            impact=-penalty,
            description=f"{len(evaluation.skipped)} policies were skipped due to missing/invalid data.",
        ))

    # Factor 4: No warnings
    if len(evaluation.warnings) == 0:
        score += 10
        factors.append(ConfidenceFactor(
            name="no_warnings",
            impact=10,
            description="Evaluation completed without warnings.",
        ))

    # Factor 5: High priority winner
    if resolution.winning_policy_id and num_matched > 0:
        score += 15
        factors.append(ConfidenceFactor(
            name="priority_resolved",
            impact=15,
            description="Winner was determined by priority ordering.",
        ))

    # Factor 6: Tie-breaker penalty
    if resolution.tie_breaker_used:
        score -= 20
        factors.append(ConfidenceFactor(
            name="tie_breaker_used",
            impact=-20,
            description="Tie-breaker (policy ID) was needed — fragile decision.",
        ))

    # Clamp to [0, 100]
    final_score = max(0, min(100, score))

    return DecisionConfidenceResult(score=final_score, factors=factors)
