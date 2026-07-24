"""
Analytics schemas for dashboard APIs.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SummaryMetrics(BaseModel):
    total_policies: int = 0
    active_policies: int = 0
    total_evaluations: int = 0
    avg_confidence: float = 0.0


class DecisionDistribution(BaseModel):
    approve: int = 0
    reject: int = 0
    manual_review: int = 0


class TrendPoint(BaseModel):
    date: str
    count: int


class TopPolicy(BaseModel):
    policy_id: str
    name: str
    match_count: int
    decision: str


class AnalyticsResponse(BaseModel):
    summary: SummaryMetrics
    distribution: DecisionDistribution
    trends: dict[str, list[TrendPoint]]
    top_policies: list[TopPolicy]
