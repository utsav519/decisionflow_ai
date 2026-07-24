"""
Engine-specific result models.

Pure data classes used by the evaluator, resolver, and confidence calculator.
Zero DB dependencies — these are the internal engine contracts.

Spec reference: §19 Evaluator Output Contract
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.schemas.policy import DecisionType


@dataclass(frozen=True)
class ConditionResult:
    """Result of evaluating a single condition against input data."""

    field: str
    operator: str
    expected: Any
    actual: Any
    matched: bool
    status: str  # MATCHED | UNMATCHED | MISSING_FIELD | INVALID_VALUE | ERROR
    reason: str | None = None


@dataclass(frozen=True)
class PolicyEvaluationResult:
    """Result of evaluating one policy against input data."""

    policy_id: str
    policy_name: str
    policy_version: int
    priority: int
    decision: str
    matched: bool
    condition_results: list[ConditionResult]
    missing_fields: list[str]
    result_status: str  # MATCHED | UNMATCHED | SKIPPED_MISSING_FIELD | SKIPPED_INVALID_DATA
    reason: str | None = None


@dataclass(frozen=True)
class EngineEvaluationResult:
    """Complete output from the evaluator — groups policies by match result."""

    matched: list[PolicyEvaluationResult]
    unmatched: list[PolicyEvaluationResult]
    skipped: list[PolicyEvaluationResult]
    evaluation_time_ms: float = 0.0
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ResolutionResult:
    """Output from the priority resolver."""

    decision: str  # APPROVE | REJECT | MANUAL_REVIEW
    winning_policy_id: str | None
    winning_policy_version: int | None
    strategy: str
    reason: str
    tie_breaker_used: bool
    competing_policy_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ConfidenceFactor:
    """One factor contributing to the confidence score."""

    name: str
    impact: int  # positive or negative points
    description: str


@dataclass(frozen=True)
class DecisionConfidenceResult:
    """Output from the confidence calculator."""

    score: int  # 0-100
    factors: list[ConfidenceFactor] = field(default_factory=list)
