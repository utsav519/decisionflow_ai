"""
Resolver tests — Spec §43 requirements.

8 required test scenarios:
  1. Highest priority wins
  2. REJECT wins a same-priority tie
  3. MANUAL_REVIEW wins over APPROVE at same priority
  4. Higher version wins after same priority and same decision
  5. Policy ID resolves the final tie
  6. No match returns MANUAL_REVIEW fallback
  7. Resolution reason is present
  8. Result is deterministic across repeated calls
"""

import pytest

from app.engine.resolver import resolve
from app.engine.result_models import EngineEvaluationResult, PolicyEvaluationResult


def _make_match(
    pid="pol_1",
    name="Policy 1",
    version=1,
    priority=100,
    decision="APPROVE",
):
    return PolicyEvaluationResult(
        policy_id=pid,
        policy_name=name,
        policy_version=version,
        priority=priority,
        decision=decision,
        matched=True,
        condition_results=[],
        missing_fields=[],
        result_status="MATCHED",
    )


def _make_eval(matched=None):
    return EngineEvaluationResult(
        matched=matched or [],
        unmatched=[],
        skipped=[],
    )


class TestResolver:
    """Spec §43: 8 required resolver test scenarios."""

    # 1. Highest priority wins
    def test_highest_priority_wins(self):
        evaluation = _make_eval([
            _make_match(pid="pol_low", priority=50, decision="APPROVE"),
            _make_match(pid="pol_high", priority=200, decision="APPROVE"),
        ])
        result = resolve(evaluation)
        assert result.winning_policy_id == "pol_high"
        assert result.decision == "APPROVE"

    # 2. REJECT wins a same-priority tie
    def test_reject_wins_same_priority(self):
        evaluation = _make_eval([
            _make_match(pid="pol_a", priority=100, decision="APPROVE"),
            _make_match(pid="pol_r", priority=100, decision="REJECT"),
        ])
        result = resolve(evaluation)
        assert result.winning_policy_id == "pol_r"
        assert result.decision == "REJECT"

    # 3. MANUAL_REVIEW wins over APPROVE at same priority
    def test_manual_review_wins_over_approve(self):
        evaluation = _make_eval([
            _make_match(pid="pol_a", priority=100, decision="APPROVE"),
            _make_match(pid="pol_m", priority=100, decision="MANUAL_REVIEW"),
        ])
        result = resolve(evaluation)
        assert result.winning_policy_id == "pol_m"
        assert result.decision == "MANUAL_REVIEW"

    # 4. Higher version wins after same priority and same decision
    def test_higher_version_wins(self):
        evaluation = _make_eval([
            _make_match(pid="pol_a", priority=100, decision="APPROVE", version=1),
            _make_match(pid="pol_b", priority=100, decision="APPROVE", version=3),
        ])
        result = resolve(evaluation)
        assert result.winning_policy_id == "pol_b"

    # 5. Policy ID resolves the final tie
    def test_policy_id_tie_breaker(self):
        evaluation = _make_eval([
            _make_match(pid="pol_bbb", priority=100, decision="APPROVE", version=1),
            _make_match(pid="pol_aaa", priority=100, decision="APPROVE", version=1),
        ])
        result = resolve(evaluation)
        assert result.winning_policy_id == "pol_aaa"
        assert result.tie_breaker_used is True

    # 6. No match returns MANUAL_REVIEW fallback
    def test_no_match_fallback(self):
        evaluation = _make_eval([])
        result = resolve(evaluation)
        assert result.decision == "MANUAL_REVIEW"
        assert result.winning_policy_id is None
        assert result.strategy == "no_match_fallback"

    # 7. Resolution reason is present
    def test_reason_is_present(self):
        evaluation = _make_eval([
            _make_match(pid="pol_1", priority=100, decision="APPROVE"),
        ])
        result = resolve(evaluation)
        assert result.reason is not None
        assert len(result.reason) > 0

    # 8. Result is deterministic across repeated calls
    def test_deterministic(self):
        evaluation = _make_eval([
            _make_match(pid="pol_a", priority=100, decision="APPROVE", version=2),
            _make_match(pid="pol_b", priority=100, decision="REJECT", version=1),
            _make_match(pid="pol_c", priority=200, decision="MANUAL_REVIEW"),
        ])
        results = [resolve(evaluation) for _ in range(20)]
        decisions = set(r.decision for r in results)
        winners = set(r.winning_policy_id for r in results)
        assert len(decisions) == 1, f"Non-deterministic decisions: {decisions}"
        assert len(winners) == 1, f"Non-deterministic winners: {winners}"
