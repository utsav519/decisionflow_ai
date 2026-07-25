"""Cross-module schemas for deterministic decision evaluation."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DecisionOutcome(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    NO_MATCH = "NO_MATCH"


class CustomerData(BaseModel):
    """Customer fields accepted by the Decision Center."""

    model_config = ConfigDict(extra="forbid")

    customer_id: str | None = Field(
        default=None,
        min_length=1,
        max_length=128,
    )
    customer_tenure_months: int | None = Field(default=None, ge=0)
    credit_score: int | None = Field(default=None, ge=300, le=900)
    payment_defaults: int | None = Field(default=None, ge=0)
    fraud_risk_score: float | None = Field(default=None, ge=0.0, le=1.0)

    monthly_bill_amount: float | None = Field(default=None, ge=0)
    requested_device_price: float | None = Field(default=None, ge=0)
    outstanding_balance: float | None = Field(default=None, ge=0)
    account_status: str | None = Field(default=None, max_length=100)

    customer_segment: str | None = Field(default=None, max_length=100)
    current_plan: str | None = Field(default=None, max_length=200)
    is_existing_customer: bool | None = None
    previous_upgrade_months_ago: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_evaluable_fields(self) -> "CustomerData":
        data = self.model_dump(
            exclude_none=True,
            exclude={"customer_id"},
        )

        if not data:
            raise ValueError(
                "At least one evaluable customer field must be supplied."
            )

        return self


class DecisionContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    channel: str | None = Field(default=None, max_length=100)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    requested_action: str | None = Field(default=None, max_length=100)


class DecisionOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    include_explanation: bool = True
    include_unmatched_rules: bool = True
    include_condition_trace: bool = True


class DecisionEvaluationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str = Field(..., min_length=1, max_length=128)
    domain: str = Field(..., min_length=1, max_length=100)
    customer: CustomerData
    context: DecisionContext = Field(default_factory=DecisionContext)
    options: DecisionOptions = Field(default_factory=DecisionOptions)


class ConditionResultResponse(BaseModel):
    field: str
    operator: str
    expected: Any | None = None
    actual: Any | None = None
    matched: bool
    status: str | None = None
    reason: str | None = None


class PolicyEvaluationResponse(BaseModel):
    policy_id: str
    policy_name: str
    policy_version: int
    priority: int
    decision: DecisionOutcome
    matched: bool
    result_status: str
    condition_results: list[ConditionResultResponse] = Field(
        default_factory=list
    )
    missing_fields: list[str] = Field(default_factory=list)


class WinningPolicyResponse(BaseModel):
    id: str
    name: str
    priority: int
    decision: DecisionOutcome
    version: int


class ResolutionResponse(BaseModel):
    decision: DecisionOutcome
    winning_policy_id: str | None = None
    winning_policy_version: int | None = None
    strategy: str
    reason: str
    tie_breaker_used: bool
    competing_policy_ids: list[str] = Field(default_factory=list)


class ProviderMetadataResponse(BaseModel):
    provider: str
    model: str
    processing_time_ms: int
    fallback_used: bool = False
    retry_count: int = 0
    request_tokens: int | None = None
    response_tokens: int | None = None
    estimated_cost: float | None = None


class ExplanationResponse(BaseModel):
    summary: str
    key_factors: list[str] = Field(default_factory=list)
    winning_policy_reason: str | None = None
    competing_policy_note: str | None = None
    generated_by: str
    fallback_used: bool
    provider_metadata: ProviderMetadataResponse | None = None


class WarningResponse(BaseModel):
    code: str
    message: str
    fields: list[str] | None = None


class EvaluationMetrics(BaseModel):
    policies_loaded: int
    policies_evaluated: int
    policies_matched: int
    policies_unmatched: int
    policies_skipped: int
    condition_count: int
    conflicts_detected: int

    engine_latency_ms: float
    explanation_latency_ms: float
    total_latency_ms: float


class DecisionEvaluationResponse(BaseModel):
    evaluation_id: str
    request_id: str
    decision: DecisionOutcome
    decision_confidence: int = Field(..., ge=0, le=100)

    winning_policy: WinningPolicyResponse | None = None

    matched_policies: list[PolicyEvaluationResponse] = Field(
        default_factory=list
    )
    unmatched_policies: list[PolicyEvaluationResponse] = Field(
        default_factory=list
    )
    skipped_policies: list[PolicyEvaluationResponse] = Field(
        default_factory=list
    )

    resolution: ResolutionResponse
    explanation: ExplanationResponse | None = None
    metrics: EvaluationMetrics
    warnings: list[WarningResponse] = Field(default_factory=list)

    evaluated_at: datetime


class DecisionDetailResponse(DecisionEvaluationResponse):
    domain: str
    customer_id: str


class DecisionListItem(BaseModel):
    evaluation_id: str
    request_id: str
    domain: str
    customer_id: str
    decision: DecisionOutcome
    decision_confidence: int = Field(..., ge=0, le=100)
    winning_policy_id: str | None = None
    evaluated_at: datetime
