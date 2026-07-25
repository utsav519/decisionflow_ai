"""
Evaluation repository — data access for evaluations and rule results.

Persists engine execution outcomes and per-policy traces.

Spec reference: §29 Evaluation Persistence
"""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.ids import new_evaluation_id, new_rule_result_id
from app.models.evaluation import Evaluation
from app.models.evaluation_rule_result import EvaluationRuleResult

logger = logging.getLogger(__name__)


class EvaluationRepository:
    """CRUD operations on evaluations and evaluation_rule_results."""

    def __init__(self, db: Session) -> None:
        self.db = db

    # ─── Evaluations ──────────────────────────────────

    def save(self, data: dict[str, Any]) -> Evaluation:
        """Alias for create_evaluation to satisfy integration handoff."""
        return self.create_evaluation(data)

    def create_evaluation(self, data: dict[str, Any]) -> Evaluation:
        """Insert a new evaluation record."""
        evaluation = Evaluation(
            id=new_evaluation_id(),
            request_id=data["request_id"],
            domain=data["domain"],
            customer_id=data["customer_id"],
            request_json=data["request_data"],
            decision=data["decision"],
            decision_confidence=data["confidence_score"],
            winning_policy_id=data.get("winning_policy_id"),
            winning_policy_version=data.get("winning_policy_version"),
            resolution_json=data.get("resolution"),
            explanation_json=data.get("explanation"),
            metrics_json=data.get("metrics"),
            warnings_json=data.get("warnings"),
            correlation_id=data["correlation_id"],
            created_by=data.get("created_by"),
        )
        self.db.add(evaluation)
        self.db.flush()
        return evaluation

    def create_rule_results(
        self,
        evaluation_id: str,
        policy_results: list[dict[str, Any]],
    ) -> list[EvaluationRuleResult]:
        """Insert per-policy rule results for an evaluation."""
        records = []
        for pr in policy_results:
            rr = EvaluationRuleResult(
                id=new_rule_result_id(),
                evaluation_id=evaluation_id,
                policy_id=pr["policy_id"],
                policy_version=pr["policy_version"],
                policy_name=pr["policy_name"],
                priority=pr["priority"],
                decision=pr["decision"],
                result_status=pr["result_status"],
                matched=pr["matched"],
                condition_results_json=pr.get("condition_results"),
                missing_fields_json=pr.get("missing_fields"),
                reason=pr.get("reason"),
            )
            self.db.add(rr)
            records.append(rr)
        self.db.flush()
        return records

    def update_explanation(
        self,
        evaluation_id: str,
        explanation: dict[str, Any] | None,
        warnings: list[Any] | None = None,
    ) -> Evaluation | None:
        """Update explanation and warnings for a stored evaluation."""
        evaluation = self.get_evaluation_by_id(evaluation_id)

        if evaluation is None:
            return None

        evaluation.explanation_json = explanation

        if warnings is not None:
            evaluation.warnings_json = warnings

        self.db.flush()
        return evaluation

    def get_evaluation_by_id(self, eval_id: str) -> Evaluation | None:
        """Fetch a single evaluation."""
        return self.db.query(Evaluation).filter(Evaluation.id == eval_id).first()

    def get_rule_results(self, evaluation_id: str) -> list[EvaluationRuleResult]:
        """Fetch all rule results for a given evaluation."""
        return (
            self.db.query(EvaluationRuleResult)
            .filter(EvaluationRuleResult.evaluation_id == evaluation_id)
            .order_by(EvaluationRuleResult.priority.desc())
            .all()
        )

    def list_evaluations(
        self,
        page: int = 1,
        page_size: int = 20,
        customer_id: str | None = None,
        decision: str | None = None,
        domain: str | None = None,
    ) -> tuple[list[Evaluation], int]:
        """Paginated list of evaluations with optional filters."""
        query = self.db.query(Evaluation)
        if customer_id:
            query = query.filter(Evaluation.customer_id == customer_id)
        if decision:
            query = query.filter(Evaluation.decision == decision)
        if domain:
            query = query.filter(Evaluation.domain == domain)

        total = query.count()
        evals = (
            query.order_by(Evaluation.evaluated_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return evals, total

    # ─── Aggregations for Analytics ───────────────────

    def count_total_evaluations(self) -> int:
        return self.db.query(func.count(Evaluation.id)).scalar() or 0

    def avg_confidence(self) -> float:
        result = self.db.query(func.avg(Evaluation.decision_confidence)).scalar()
        return round(float(result), 1) if result else 0.0

    def count_by_decision(self) -> dict[str, int]:
        rows = (
            self.db.query(Evaluation.decision, func.count(Evaluation.id))
            .group_by(Evaluation.decision)
            .all()
        )
        return {decision: count for decision, count in rows}

    def top_winning_policies(self, limit: int = 5) -> list[dict[str, Any]]:
        """Return the most-matched policies across evaluations."""
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
        return [
            {"policy_id": pid, "match_count": cnt}
            for pid, cnt in rows
        ]

    def daily_evaluation_counts(self, days: int = 30) -> list[dict[str, Any]]:
        """Return evaluation counts grouped by day."""
        rows = (
            self.db.query(
                func.date(Evaluation.evaluated_at).label("eval_date"),
                func.count(Evaluation.id).label("count"),
            )
            .group_by(func.date(Evaluation.evaluated_at))
            .order_by(func.date(Evaluation.evaluated_at).desc())
            .limit(days)
            .all()
        )
        return [
            {"date": str(row.eval_date), "count": row.count}
            for row in rows
        ]
