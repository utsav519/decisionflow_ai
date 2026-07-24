"""
Evaluation service — orchestrates the full evaluation pipeline.

Flow: Receive request → fetch active policies → run engine →
      resolve → score confidence → persist → return response.

Spec reference: §29 Evaluation Pipeline
"""

from __future__ import annotations

import logging
import time
from typing import Any

from sqlalchemy.orm import Session

from app.core.ids import new_correlation_id
from app.engine.confidence import calculate_confidence
from app.engine.evaluator import evaluate_policies
from app.engine.resolver import resolve
from app.repositories.audit_repository import AuditRepository
from app.repositories.evaluation_repository import EvaluationRepository
from app.repositories.policy_repository import PolicyRepository

logger = logging.getLogger(__name__)


class EvaluationService:
    """Orchestrates the decision evaluation pipeline."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.policy_repo = PolicyRepository(db)
        self.eval_repo = EvaluationRepository(db)
        self.audit_repo = AuditRepository(db)

    def evaluate(
        self,
        domain: str,
        customer_id: str,
        data: dict[str, Any],
        options: dict[str, Any] | None = None,
        performed_by: str = "api",
        correlation_id: str | None = None,
    ) -> dict[str, Any]:
        """Execute the full evaluation pipeline.

        1. Fetch active policies for the domain.
        2. Run the rule engine evaluator.
        3. Resolve winning decision.
        4. Calculate confidence score.
        5. Persist the evaluation and rule results.
        6. Return structured response.
        """
        correlation_id = correlation_id or new_correlation_id()
        request_id = new_correlation_id()  # unique per request
        start_time = time.perf_counter()

        # 1. Fetch active policies
        policies = self.policy_repo.get_active_by_domain(domain)
        policy_dicts = [self._policy_to_engine_dict(p) for p in policies]

        # 2. Run evaluator
        evaluation_result = evaluate_policies(policy_dicts, data)

        # 3. Resolve decision
        resolution_result = resolve(evaluation_result)

        # 4. Calculate confidence
        confidence_result = calculate_confidence(evaluation_result, resolution_result)

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # 5. Build resolution dict for persistence
        resolution_dict = {
            "decision": resolution_result.decision,
            "winning_policy_id": resolution_result.winning_policy_id,
            "winning_policy_version": resolution_result.winning_policy_version,
            "strategy": resolution_result.strategy,
            "reason": resolution_result.reason,
            "tie_breaker_used": resolution_result.tie_breaker_used,
            "competing_policy_ids": resolution_result.competing_policy_ids,
        }

        confidence_dict = {
            "score": confidence_result.score,
            "factors": [
                {"name": f.name, "impact": f.impact, "reason": f.reason}
                for f in confidence_result.factors
            ],
        }

        metrics_dict = {
            "evaluation_time_ms": elapsed_ms,
            "policies_evaluated": len(policy_dicts),
            "policies_matched": len(evaluation_result.matched),
            "policies_unmatched": len(evaluation_result.unmatched),
            "policies_skipped": len(evaluation_result.skipped),
        }

        # 6. Persist evaluation
        eval_record = self.eval_repo.create_evaluation({
            "request_id": request_id,
            "domain": domain,
            "customer_id": customer_id,
            "request_data": data,
            "decision": resolution_result.decision,
            "confidence_score": confidence_result.score,
            "winning_policy_id": resolution_result.winning_policy_id,
            "winning_policy_version": resolution_result.winning_policy_version,
            "resolution": resolution_dict,
            "explanation": confidence_dict,
            "metrics": metrics_dict,
            "warnings": evaluation_result.warnings,
            "correlation_id": correlation_id,
            "created_by": performed_by,
        })

        # Persist per-policy rule results
        all_policy_results = []
        for pr in evaluation_result.matched + evaluation_result.unmatched + evaluation_result.skipped:
            all_policy_results.append({
                "policy_id": pr.policy_id,
                "policy_version": pr.policy_version,
                "policy_name": pr.policy_name,
                "priority": pr.priority,
                "decision": pr.decision,
                "result_status": pr.result_status,
                "matched": pr.matched,
                "condition_results": [
                    {
                        "field": cr.field,
                        "operator": cr.operator,
                        "expected": cr.expected,
                        "actual": cr.actual,
                        "matched": cr.matched,
                        "status": cr.status,
                        "reason": cr.reason,
                    }
                    for cr in pr.condition_results
                ],
                "missing_fields": pr.missing_fields,
            })

        self.eval_repo.create_rule_results(eval_record.id, all_policy_results)

        # Audit log
        self.audit_repo.create({
            "action": "EVALUATION_EXECUTED",
            "entity_type": "EVALUATION",
            "entity_id": eval_record.id,
            "performed_by": performed_by,
            "summary": (
                f"Evaluation {eval_record.id}: decision={resolution_result.decision} "
                f"confidence={confidence_result.score} "
                f"winning_policy={resolution_result.winning_policy_id}"
            ),
            "request_snapshot": {
                "domain": domain,
                "customer_id": customer_id,
                "data_keys": list(data.keys()),
            },
            "result_snapshot": {
                "decision": resolution_result.decision,
                "confidence": confidence_result.score,
                "winning_policy_id": resolution_result.winning_policy_id,
            },
            "correlation_id": correlation_id,
        })

        self.db.commit()

        # 7. Return response
        return {
            "id": eval_record.id,
            "request_id": request_id,
            "decision": resolution_result.decision,
            "confidence_score": confidence_result.score,
            "confidence_factors": confidence_dict["factors"],
            "winning_policy_id": resolution_result.winning_policy_id,
            "winning_policy_version": resolution_result.winning_policy_version,
            "resolution": resolution_dict,
            "metrics": metrics_dict,
            "warnings": evaluation_result.warnings,
            "evaluated_at": eval_record.evaluated_at.isoformat(),
            "correlation_id": correlation_id,
        }

    def get_evaluation(self, eval_id: str) -> dict[str, Any]:
        """Retrieve a stored evaluation with its rule results."""
        evaluation = self.eval_repo.get_evaluation_by_id(eval_id)
        if not evaluation:
            from app.core.exceptions import ApplicationError
            raise ApplicationError(
                code="EVALUATION_NOT_FOUND",
                message="The requested evaluation does not exist.",
                status_code=404,
                details=[{"path": "evaluation_id", "received": eval_id}],
            )

        rule_results = self.eval_repo.get_rule_results(eval_id)

        return {
            "id": evaluation.id,
            "request_id": evaluation.request_id,
            "domain": evaluation.domain,
            "customer_id": evaluation.customer_id,
            "decision": evaluation.decision,
            "confidence_score": evaluation.decision_confidence,
            "winning_policy_id": evaluation.winning_policy_id,
            "winning_policy_version": evaluation.winning_policy_version,
            "resolution": evaluation.resolution_json,
            "explanation": evaluation.explanation_json,
            "metrics": evaluation.metrics_json,
            "warnings": evaluation.warnings_json or [],
            "evaluated_at": evaluation.evaluated_at.isoformat(),
            "correlation_id": evaluation.correlation_id,
            "rule_results": [
                {
                    "policy_id": rr.policy_id,
                    "policy_name": rr.policy_name,
                    "policy_version": rr.policy_version,
                    "priority": rr.priority,
                    "decision": rr.decision,
                    "matched": rr.matched,
                    "result_status": rr.result_status,
                    "condition_results": rr.condition_results_json or [],
                    "missing_fields": rr.missing_fields_json or [],
                }
                for rr in rule_results
            ],
        }

    def _policy_to_engine_dict(self, policy) -> dict[str, Any]:
        """Convert a Policy ORM object to the dict the engine expects."""
        return {
            "id": policy.id,
            "name": policy.name,
            "current_version": policy.current_version,
            "priority": policy.priority,
            "decision": policy.decision,
            "conditions_json": policy.conditions_json,
        }
