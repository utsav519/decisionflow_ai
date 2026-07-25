"""
Analytics repository — read-only aggregation queries for dashboards.

Composes data from policies, evaluations, and rule results.

Spec reference: §31 Analytics
"""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.evaluation import Evaluation
from app.models.policy import Policy

logger = logging.getLogger(__name__)


class AnalyticsRepository:
    """Read-only aggregation queries powering the analytics dashboard."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_policy_counts_by_status(self) -> dict[str, int]:
        """Return {status: count} for all policies."""
        rows = (
            self.db.query(Policy.status, func.count(Policy.id))
            .group_by(Policy.status)
            .all()
        )
        return {status: count for status, count in rows}

    def get_total_policies(self) -> int:
        return self.db.query(func.count(Policy.id)).scalar() or 0

    def get_total_evaluations(self) -> int:
        return self.db.query(func.count(Evaluation.id)).scalar() or 0

    def get_avg_confidence(self) -> float:
        result = self.db.query(func.avg(Evaluation.decision_confidence)).scalar()
        return round(float(result), 1) if result else 0.0

    def get_decision_distribution(self) -> dict[str, int]:
        """Return evaluation counts grouped by decision type."""
        rows = (
            self.db.query(Evaluation.decision, func.count(Evaluation.id))
            .group_by(Evaluation.decision)
            .all()
        )
        return {decision: count for decision, count in rows}

    def get_evaluation_trends(self, days: int = 30) -> list[dict[str, Any]]:
        """Return daily evaluation counts for trending."""
        rows = (
            self.db.query(
                func.date(Evaluation.evaluated_at).label("eval_date"),
                func.count(Evaluation.id).label("count"),
            )
            .group_by(func.date(Evaluation.evaluated_at))
            .order_by(func.date(Evaluation.evaluated_at).asc())
            .limit(days)
            .all()
        )
        return [{"date": str(row.eval_date), "count": row.count} for row in rows]

    def get_decision_trends(self, days: int = 30) -> dict[str, list[dict[str, Any]]]:
        """Return daily counts per decision type for trend charts."""
        rows = (
            self.db.query(
                func.date(Evaluation.evaluated_at).label("eval_date"),
                Evaluation.decision,
                func.count(Evaluation.id).label("count"),
            )
            .group_by(func.date(Evaluation.evaluated_at), Evaluation.decision)
            .order_by(func.date(Evaluation.evaluated_at).asc())
            .limit(days * 3)  # up to 3 decision types per day
            .all()
        )
        trends: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            decision = row.decision
            if decision not in trends:
                trends[decision] = []
            trends[decision].append({"date": str(row.eval_date), "count": row.count})
        return trends

    def get_top_policies(self, limit: int = 5) -> list[dict[str, Any]]:
        """Return top N policies by match count from evaluations."""
        rows = (
            self.db.query(
                Evaluation.winning_policy_id,
                func.count(Evaluation.id).label("match_count"),
            )
            .filter(Evaluation.winning_policy_id.is_not(None))
            .group_by(Evaluation.winning_policy_id)
            .order_by(func.count(Evaluation.id).desc())
            .limit(limit)
            .all()
        )

        results = []
        for pid, match_count in rows:
            policy = self.db.query(Policy).filter(Policy.id == pid).first()
            results.append({
                "policy_id": pid,
                "name": policy.name if policy else "Unknown",
                "match_count": match_count,
                "decision": policy.decision if policy else "Unknown",
            })
        return results
