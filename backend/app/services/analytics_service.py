"""
Analytics service — composes dashboard metrics from repositories.

Spec reference: §31 Analytics
"""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.orm import Session

from app.repositories.analytics_repository import AnalyticsRepository

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Composes analytics metrics for the dashboard API."""

    def __init__(self, db: Session) -> None:
        self.repo = AnalyticsRepository(db)

    def get_dashboard(self) -> dict[str, Any]:
        """Return the full analytics dashboard payload."""
        # Summary metrics
        policy_counts = self.repo.get_policy_counts_by_status()
        total_policies = self.repo.get_total_policies()
        active_policies = policy_counts.get("ACTIVE", 0)
        total_evaluations = self.repo.get_total_evaluations()
        avg_confidence = self.repo.get_avg_confidence()

        # Decision distribution
        distribution = self.repo.get_decision_distribution()

        # Trends
        eval_trends = self.repo.get_evaluation_trends(days=30)
        decision_trends = self.repo.get_decision_trends(days=30)

        # Top policies
        top_policies = self.repo.get_top_policies(limit=5)

        return {
            "summary": {
                "total_policies": total_policies,
                "active_policies": active_policies,
                "total_evaluations": total_evaluations,
                "avg_confidence": avg_confidence,
                "policy_status_breakdown": policy_counts,
            },
            "distribution": {
                "approve": distribution.get("APPROVE", 0),
                "reject": distribution.get("REJECT", 0),
                "manual_review": distribution.get("MANUAL_REVIEW", 0),
            },
            "trends": {
                "evaluations": eval_trends,
                **{k: v for k, v in decision_trends.items()},
            },
            "top_policies": top_policies,
        }

    def get_summary(self, domain: str | None = None) -> dict[str, Any]:
        """Return summary metrics for the dashboard."""
        return self.get_dashboard()["summary"]

    def get_decision_distribution(self, domain: str | None = None) -> dict[str, Any]:
        """Return decision distribution metrics."""
        return self.get_dashboard()["distribution"]

    def get_decision_trend(self, domain: str | None = None) -> dict[str, Any]:
        """Return decision trend metrics."""
        return self.get_dashboard()["trends"]

    def get_top_policies(self, domain: str | None = None) -> list[dict[str, Any]]:
        """Return top policies."""
        return self.get_dashboard()["top_policies"]
