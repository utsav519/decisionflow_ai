"""
Evaluation schemas for executing requests against the rule engine.

Spec reference: §19 Evaluator Output Contract
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.policy import DecisionType


class EvaluationRequest(BaseModel):
    domain: str = Field(..., description="Business domain (e.g. 'telecom', 'finance')")
    customer_id: str = Field(..., description="Unique customer identifier")
    data: dict[str, Any] = Field(..., description="Payload to evaluate")
    options: dict[str, Any] | None = Field(default_factory=dict, description="Optional evaluation flags")


class MatchStatus(str, Enum):
    MATCHED = "MATCHED"
    UNMATCHED = "UNMATCHED"
    MISSING_FIELD = "MISSING_FIELD"
    INVALID_VALUE = "INVALID_VALUE"
    ERROR = "ERROR"


class ConditionTrace(BaseModel):
    """Trace of a single condition evaluation."""
    field: str
    operator: str
    expected: Any | None
    actual: Any | None
    matched: bool
    status: MatchStatus
    reason: str | None = None


class ResolutionResult(BaseModel):
    """Details how multiple policy matches were resolved."""
    decision: DecisionType
    winning_policy: str | None
    strategy: str
    reason: str
    tie_breaker_used: bool
    competing_policy_ids: list[str]


class EvaluationResponse(BaseModel):
    """Final result of an evaluation returned to API clients."""
    id: str
    request_id: str
    decision: DecisionType
    confidence_score: int = Field(..., ge=0, le=100)
    winning_policy_id: str | None
    winning_policy_version: int | None
    resolution: ResolutionResult
    metrics: dict[str, Any]
    warnings: list[str]
    evaluated_at: datetime
    correlation_id: str

    model_config = ConfigDict(from_attributes=True)
