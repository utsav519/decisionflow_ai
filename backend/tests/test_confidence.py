"""
Confidence calculator tests.

Validates that the confidence score is deterministic, clamped to [0, 100],
and that the factors list explains the score breakdown.
"""

import pytest

from app.engine.confidence import calculate_confidence
from app.engine.result_models import (
    DecisionConfidenceResult,
    EngineEvaluationResult,
    PolicyEvaluationResult,
    ResolutionResult,
)


def _make_match(pid="pol_1", priority=100, decision="APPROVE"):
    return PolicyEvaluationResult(
        policy_id=pid,
        policy_name="Test",
        policy_version=1,
        priority=priority,
        decision=decision,
        matched=True,
        condition_results=[],
        missing_fields=[],
        result_status="MATCHED",
    )


def _make_skip(pid="pol_skip"):
    return PolicyEvaluationResult(
        policy_id=pid,
        policy_name="Skipped",
        policy_version=1,
        priority=50,
        decision="APPROVE",
        matched=False,
        condition_results=[],
        missing_fields=["missing_field"],
        result_status="SKIPPED_MISSING_FIELD",
    )


class TestConfidence:
    def test_perfect_single_match(self):
        """Single match, no skips, no warnings → high confidence."""
        evaluation = EngineEvaluationResult(
            matched=[_make_match()],
            unmatched=[],
            skipped=[],
            warnings=[],
        )
        resolution = ResolutionResult(
            decision="APPROVE",
            winning_policy_id="pol_1",
            winning_policy_version=1,
            strategy="single_match",
            reason="Only one policy matched.",
            tie_breaker_used=False,
            competing_policy_ids=["pol_1"],
        )
        result = calculate_confidence(evaluation, resolution)
        assert result.score == 100  # 40+20+15+10+15 = 100
        assert len(result.factors) > 0

    def test_no_match_fallback(self):
        """No match → low confidence."""
        evaluation = EngineEvaluationResult(
            matched=[], unmatched=[], skipped=[], warnings=[],
        )
        resolution = ResolutionResult(
            decision="MANUAL_REVIEW",
            winning_policy_id=None,
            winning_policy_version=None,
            strategy="no_match_fallback",
            reason="No match",
            tie_breaker_used=False,
        )
        result = calculate_confidence(evaluation, resolution)
        assert result.score <= 30

    def test_tie_breaker_reduces_confidence(self):
        """Tie-breaker used → penalty applied."""
        evaluation = EngineEvaluationResult(
            matched=[_make_match("pol_a"), _make_match("pol_b")],
            unmatched=[], skipped=[], warnings=[],
        )
        resolution = ResolutionResult(
            decision="APPROVE",
            winning_policy_id="pol_a",
            winning_policy_version=1,
            strategy="policy_id",
            reason="Tie broken by ID",
            tie_breaker_used=True,
            competing_policy_ids=["pol_a", "pol_b"],
        )
        result = calculate_confidence(evaluation, resolution)
        assert result.score < 100

    def test_skipped_policies_reduce_confidence(self):
        """Skipped policies → lower confidence."""
        evaluation = EngineEvaluationResult(
            matched=[_make_match()],
            unmatched=[],
            skipped=[_make_skip()],
            warnings=["Policy skipped"],
        )
        resolution = ResolutionResult(
            decision="APPROVE",
            winning_policy_id="pol_1",
            winning_policy_version=1,
            strategy="single_match",
            reason="Single match",
            tie_breaker_used=False,
            competing_policy_ids=["pol_1"],
        )
        result = calculate_confidence(evaluation, resolution)
        # Should be less than perfect due to skips and warnings
        assert result.score < 100

    def test_score_clamped_0_to_100(self):
        """Score never goes below 0 or above 100."""
        evaluation = EngineEvaluationResult(
            matched=[_make_match(f"pol_{i}") for i in range(20)],
            unmatched=[], skipped=[_make_skip(f"skip_{i}") for i in range(10)],
            warnings=["w1", "w2"],
        )
        resolution = ResolutionResult(
            decision="APPROVE",
            winning_policy_id="pol_0",
            winning_policy_version=1,
            strategy="priority",
            reason="Winner",
            tie_breaker_used=True,
            competing_policy_ids=[f"pol_{i}" for i in range(20)],
        )
        result = calculate_confidence(evaluation, resolution)
        assert 0 <= result.score <= 100

    def test_deterministic(self):
        """Same inputs always produce the same score."""
        evaluation = EngineEvaluationResult(
            matched=[_make_match("pol_1"), _make_match("pol_2")],
            unmatched=[], skipped=[], warnings=[],
        )
        resolution = ResolutionResult(
            decision="APPROVE",
            winning_policy_id="pol_1",
            winning_policy_version=1,
            strategy="priority",
            reason="Priority wins",
            tie_breaker_used=False,
            competing_policy_ids=["pol_1", "pol_2"],
        )
        scores = [calculate_confidence(evaluation, resolution).score for _ in range(20)]
        assert len(set(scores)) == 1, f"Non-deterministic scores: {set(scores)}"

    def test_factors_explain_score(self):
        """Factors list should sum to approximately the final score."""
        evaluation = EngineEvaluationResult(
            matched=[_make_match()], unmatched=[], skipped=[], warnings=[],
        )
        resolution = ResolutionResult(
            decision="APPROVE",
            winning_policy_id="pol_1",
            winning_policy_version=1,
            strategy="single_match",
            reason="Single match",
            tie_breaker_used=False,
            competing_policy_ids=["pol_1"],
        )
        result = calculate_confidence(evaluation, resolution)
        factor_sum = sum(f.impact for f in result.factors)
        # Score is clamped, but unclamped sum should match
        assert factor_sum == result.score or (result.score == 100 and factor_sum >= 100)
