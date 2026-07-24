"""
Policy Pydantic schemas.

Contains schemas for creating, updating, and returning policies.
Includes condition nodes (rules tree) and nested metadata.

Spec reference: §15 Policy Management
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class PolicyStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    ARCHIVED = "ARCHIVED"


class DecisionType(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class SourceType(str, Enum):
    AI_GENERATED = "AI_GENERATED"
    MANUAL = "MANUAL"
    IMPORTED = "IMPORTED"
    SEEDED = "SEEDED"


class Condition(BaseModel):
    field: str = Field(..., description="Field path to evaluate (e.g. 'customer.credit_score')")
    operator: str = Field(..., description="Operator ID (e.g. 'greater_than')")
    value: Any | None = Field(None, description="Value to compare against")


class ConditionGroup(BaseModel):
    # 'all' and 'any' must be mutually exclusive in validation, but they are defined as optional lists
    all: list["ConditionNode"] | None = Field(None, description="All conditions must pass (AND)")
    any: list["ConditionNode"] | None = Field(None, description="Any condition must pass (OR)")


# ConditionNode can be a single rule or a nested group
ConditionNode = Condition | ConditionGroup


class AIMetadata(BaseModel):
    generated: bool = Field(False)
    ai_confidence: int | None = Field(None, ge=0, le=100)
    warnings: list[str] | None = Field(None)
    ambiguities: list[str] | None = Field(None)
    model: str | None = Field(None)


class PolicyCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=120)
    description: str | None = Field(None)
    domain: str = Field(..., min_length=2, max_length=50)
    priority: int = Field(..., ge=1)
    decision: DecisionType = Field(...)
    conditions: ConditionGroup = Field(...)
    reason: str | None = Field(None)
    source: SourceType = Field(default=SourceType.MANUAL)
    ai_metadata: AIMetadata | None = Field(None)

    model_config = ConfigDict(extra="forbid")


class PolicyUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=120)
    description: str | None = Field(None)
    priority: int | None = Field(None, ge=1)
    decision: DecisionType | None = Field(None)
    conditions: ConditionGroup | None = Field(None)
    reason: str | None = Field(None)

    model_config = ConfigDict(extra="forbid")


class PolicyResponse(BaseModel):
    id: str
    version: int
    name: str
    description: str | None
    domain: str
    status: PolicyStatus
    priority: int
    decision: DecisionType
    conditions: ConditionGroup
    reason: str | None
    source: SourceType
    ai_metadata: AIMetadata | None
    created_by: str | None
    approved_by: str | None
    created_at: datetime
    updated_at: datetime
    activated_at: datetime | None
    disabled_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class PolicyListItem(BaseModel):
    id: str
    version: int
    name: str
    domain: str
    status: PolicyStatus
    priority: int
    decision: DecisionType
    created_by: str | None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PolicyStateTransition(BaseModel):
    reason: str | None = Field(None, description="Reason for the state change")
    approval_comment: str | None = Field(None, description="Comment from the approver (if activating)")


# Rebuild forward references for ConditionGroup
ConditionGroup.model_rebuild()
