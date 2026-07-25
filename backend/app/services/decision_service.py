"""Contract-facing decision orchestration service."""

from __future__ import annotations

from time import perf_counter
from typing import Any

from sqlalchemy.orm import Session

from app.repositories.evaluation_repository import EvaluationRepository
from app.schemas.decision import (
    DecisionDetailResponse,
    DecisionEvaluationRequest,
    DecisionEvaluationResponse,
    DecisionListItem,
    EvaluationMetrics,
    ExplanationResponse,
    PolicyEvaluationResponse,
    ResolutionResponse,
    WarningResponse,
    WinningPolicyResponse,
)
from app.services.audit_service import AuditService
from app.services.evaluation_service import EvaluationService
from app.services.explanation_service import ExplanationService


class DecisionService:
    """Coordinates deterministic evaluation and optional AI explanation."""

    def __init__(
        self,
        *,
        db: Session,
        evaluation_service: EvaluationService,
        evaluation_repository: EvaluationRepository,
        audit_service: AuditService,
        explanation_service: ExplanationService,
    ) -> None:
        self._db = db
        self._evaluation_service = evaluation_service
        self._evaluation_repository = evaluation_repository
        self._audit_service = audit_service
        self._explanation_service = explanation_service

    async def evaluate(
        self,
        *,
        request: DecisionEvaluationRequest,
        actor_id: str,
        correlation_id: str,
    ) -> DecisionEvaluationResponse:
        """Execute the complete decision workflow as one transaction."""
        started_at = perf_counter()

        customer_data = request.customer.model_dump(exclude_none=True)
        context_data = request.context.model_dump(exclude_none=True)

        customer_id = (
            request.customer.customer_id
            or f"anonymous:{request.request_id}"
        )

        engine_data = self._build_engine_data(
            customer_data=customer_data,
            context_data=context_data,
        )

        try:
            deterministic_result = self._evaluation_service.evaluate(
                domain=request.domain,
                customer_id=customer_id,
                data=engine_data,
                options=request.options.model_dump(),
                performed_by=actor_id,
                correlation_id=correlation_id,
                request_id=request.request_id,
                write_audit=False,
                commit=False,
            )

            rule_results = deterministic_result.get(
                "rule_results",
                [],
            )

            matched = self._build_policy_results(
                rule_results,
                status="MATCHED",
                include_condition_trace=(
                    request.options.include_condition_trace
                ),
            )

            unmatched = self._build_policy_results(
                rule_results,
                status="UNMATCHED",
                include_condition_trace=(
                    request.options.include_condition_trace
                ),
            )

            skipped = [
                self._build_policy_result(
                    item,
                    include_condition_trace=(
                        request.options.include_condition_trace
                    ),
                )
                for item in rule_results
                if str(item.get("result_status", "")).startswith(
                    "SKIPPED_"
                )
            ]

            if not request.options.include_unmatched_rules:
                unmatched = []

            winning_policy = self._find_winning_policy(
                rule_results=rule_results,
                winning_policy_id=deterministic_result.get(
                    "winning_policy_id"
                ),
            )

            resolution = ResolutionResponse.model_validate(
                deterministic_result["resolution"]
            )

            warnings = self._normalise_warnings(
                deterministic_result.get("warnings", [])
            )

            missing_fields = sorted({
                field
                for policy in skipped
                for field in policy.missing_fields
            })

            if missing_fields:
                warnings.append(
                    WarningResponse(
                        code="MISSING_REQUIRED_FIELDS",
                        message=(
                            "Some active policies could not be evaluated "
                            "because required fields were missing."
                        ),
                        fields=missing_fields,
                    )
                )

            evidence = {
                "decision": deterministic_result["decision"],
                "decision_confidence": deterministic_result[
                    "confidence_score"
                ],
                "winning_policy": (
                    winning_policy.model_dump()
                    if winning_policy
                    else None
                ),
                "matched_policies": [
                    item.model_dump()
                    for item in matched
                ],
                "unmatched_policies": [
                    item.model_dump()
                    for item in unmatched
                ],
                "skipped_policies": [
                    item.model_dump()
                    for item in skipped
                ],
                "missing_fields": missing_fields,
                "resolution": resolution.model_dump(),
                "confidence_factors": deterministic_result.get(
                    "confidence_factors",
                    [],
                ),
            }

            explanation = None
            explanation_latency_ms = 0.0

            if request.options.include_explanation:
                explanation_started_at = perf_counter()

                explanation_outcome = (
                    await self._explanation_service.explain(
                        evidence=evidence,
                        correlation_id=correlation_id,
                    )
                )

                explanation_latency_ms = round(
                    (
                        perf_counter()
                        - explanation_started_at
                    )
                    * 1000,
                    2,
                )

                explanation = ExplanationResponse.model_validate(
                    explanation_outcome.explanation.model_dump(
                        mode="json"
                    )
                )

                warnings.extend(
                    WarningResponse.model_validate(item)
                    for item in explanation_outcome.warnings
                )

            backend_metrics = deterministic_result.get(
                "metrics",
                {},
            )

            condition_count = sum(
                len(item.get("condition_results", []))
                for item in rule_results
            )

            total_latency_ms = round(
                (perf_counter() - started_at) * 1000,
                2,
            )

            policies_evaluated = int(
                backend_metrics.get(
                    "policies_evaluated",
                    len(rule_results),
                )
            )

            metrics = EvaluationMetrics(
                policies_loaded=policies_evaluated,
                policies_evaluated=policies_evaluated,
                policies_matched=len(matched),
                policies_unmatched=len([
                    item
                    for item in rule_results
                    if item.get("result_status") == "UNMATCHED"
                ]),
                policies_skipped=len(skipped),
                condition_count=condition_count,
                conflicts_detected=max(0, len(matched) - 1),
                engine_latency_ms=float(
                    backend_metrics.get(
                        "evaluation_time_ms",
                        0.0,
                    )
                ),
                explanation_latency_ms=explanation_latency_ms,
                total_latency_ms=total_latency_ms,
            )

            response = DecisionEvaluationResponse(
                evaluation_id=deterministic_result["id"],
                request_id=deterministic_result["request_id"],
                decision=deterministic_result["decision"],
                decision_confidence=deterministic_result[
                    "confidence_score"
                ],
                winning_policy=winning_policy,
                matched_policies=matched,
                unmatched_policies=unmatched,
                skipped_policies=skipped,
                resolution=resolution,
                explanation=explanation,
                metrics=metrics,
                warnings=warnings,
                evaluated_at=deterministic_result[
                    "evaluated_at"
                ],
            )

            explanation_data = (
                explanation.model_dump(mode="json")
                if explanation
                else None
            )

            warning_data = [
                item.model_dump(mode="json")
                for item in warnings
            ]

            self._evaluation_repository.update_explanation(
                evaluation_id=response.evaluation_id,
                explanation=explanation_data,
                warnings=warning_data,
            )

            audit_payload = response.model_dump(mode="json")
            audit_payload["domain"] = request.domain
            audit_payload["customer_id"] = customer_id

            self._audit_service.record_decision(
                evaluation=audit_payload,
                actor_id=actor_id,
                correlation_id=correlation_id,
            )

            if any(
                item.code == "AI_EXPLANATION_UNAVAILABLE"
                for item in warnings
            ):
                self._audit_service.record_ai_explanation_failed(
                    evaluation_id=response.evaluation_id,
                    actor_id=actor_id,
                    correlation_id=correlation_id,
                )

            self._db.commit()
            return response

        except Exception:
            self._db.rollback()
            raise

    def get_decision(
        self,
        evaluation_id: str,
    ) -> DecisionDetailResponse:
        """Return a stored decision using the official API contract."""
        stored = self._evaluation_service.get_evaluation(
            evaluation_id
        )

        rule_results = stored.get("rule_results", [])

        matched = self._build_policy_results(
            rule_results,
            status="MATCHED",
            include_condition_trace=True,
        )

        unmatched = self._build_policy_results(
            rule_results,
            status="UNMATCHED",
            include_condition_trace=True,
        )

        skipped = [
            self._build_policy_result(
                item,
                include_condition_trace=True,
            )
            for item in rule_results
            if str(item.get("result_status", "")).startswith(
                "SKIPPED_"
            )
        ]

        winning_policy = self._find_winning_policy(
            rule_results=rule_results,
            winning_policy_id=stored.get(
                "winning_policy_id"
            ),
        )

        explanation = self._parse_stored_explanation(
            stored.get("explanation")
        )

        metrics_data = stored.get("metrics") or {}

        policies_evaluated = int(
            metrics_data.get(
                "policies_evaluated",
                len(rule_results),
            )
        )

        metrics = EvaluationMetrics(
            policies_loaded=policies_evaluated,
            policies_evaluated=policies_evaluated,
            policies_matched=len(matched),
            policies_unmatched=len(unmatched),
            policies_skipped=len(skipped),
            condition_count=sum(
                len(item.get("condition_results", []))
                for item in rule_results
            ),
            conflicts_detected=max(0, len(matched) - 1),
            engine_latency_ms=float(
                metrics_data.get(
                    "evaluation_time_ms",
                    metrics_data.get(
                        "engine_latency_ms",
                        0.0,
                    ),
                )
            ),
            explanation_latency_ms=float(
                metrics_data.get(
                    "explanation_latency_ms",
                    0.0,
                )
            ),
            total_latency_ms=float(
                metrics_data.get(
                    "total_latency_ms",
                    metrics_data.get(
                        "evaluation_time_ms",
                        0.0,
                    ),
                )
            ),
        )

        return DecisionDetailResponse(
            evaluation_id=stored["id"],
            request_id=stored["request_id"],
            domain=stored["domain"],
            customer_id=stored["customer_id"],
            decision=stored["decision"],
            decision_confidence=stored[
                "confidence_score"
            ],
            winning_policy=winning_policy,
            matched_policies=matched,
            unmatched_policies=unmatched,
            skipped_policies=skipped,
            resolution=ResolutionResponse.model_validate(
                stored["resolution"]
            ),
            explanation=explanation,
            metrics=metrics,
            warnings=self._normalise_warnings(
                stored.get("warnings", [])
            ),
            evaluated_at=stored["evaluated_at"],
        )

    def list_decisions(
        self,
        *,
        page: int,
        page_size: int,
        customer_id: str | None = None,
        decision: str | None = None,
        domain: str | None = None,
    ) -> tuple[list[DecisionListItem], int]:
        """Return a paginated list of stored decisions."""
        records, total = (
            self._evaluation_repository.list_evaluations(
                page=page,
                page_size=page_size,
                customer_id=customer_id,
                decision=decision,
                domain=domain,
            )
        )

        items = [
            DecisionListItem(
                evaluation_id=record.id,
                request_id=record.request_id,
                domain=record.domain,
                customer_id=record.customer_id,
                decision=record.decision,
                decision_confidence=(
                    record.decision_confidence
                ),
                winning_policy_id=(
                    record.winning_policy_id
                ),
                evaluated_at=record.evaluated_at,
            )
            for record in records
        ]

        return items, total

    @staticmethod
    def _build_engine_data(
        *,
        customer_data: dict[str, Any],
        context_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Map public API fields to deterministic catalogue paths.

        The public contract remains authoritative. Compatibility aliases are
        added only to the internal engine payload.
        """
        engine_customer = dict(customer_data)

        tenure = customer_data.get("customer_tenure_months")
        if tenure is not None:
            engine_customer["tenure_months"] = tenure

        defaults = customer_data.get("payment_defaults")
        if defaults is not None:
            engine_customer["payment_history_defaults"] = defaults

        segment = customer_data.get("customer_segment")
        if segment:
            engine_customer["plan_type"] = segment.strip().lower()

        account: dict[str, Any] = {}

        balance = customer_data.get("outstanding_balance")
        if balance is not None:
            account["outstanding_balance"] = balance

        account_status = customer_data.get("account_status")
        if account_status:
            account["status"] = account_status.strip().lower()

        return {
            **customer_data,
            **context_data,
            "customer": engine_customer,
            "account": account,
            "context": dict(context_data),
        }

    @staticmethod
    def _build_policy_results(
        rule_results: list[dict[str, Any]],
        *,
        status: str,
        include_condition_trace: bool,
    ) -> list[PolicyEvaluationResponse]:
        return [
            DecisionService._build_policy_result(
                item,
                include_condition_trace=(
                    include_condition_trace
                ),
            )
            for item in rule_results
            if item.get("result_status") == status
        ]

    @staticmethod
    def _build_policy_result(
        item: dict[str, Any],
        *,
        include_condition_trace: bool,
    ) -> PolicyEvaluationResponse:
        payload = dict(item)

        if not include_condition_trace:
            payload["condition_results"] = []

        return PolicyEvaluationResponse.model_validate(
            payload
        )

    @staticmethod
    def _find_winning_policy(
        *,
        rule_results: list[dict[str, Any]],
        winning_policy_id: str | None,
    ) -> WinningPolicyResponse | None:
        if winning_policy_id is None:
            return None

        for item in rule_results:
            if item.get("policy_id") != winning_policy_id:
                continue

            return WinningPolicyResponse(
                id=item["policy_id"],
                name=item["policy_name"],
                priority=item["priority"],
                decision=item["decision"],
                version=item["policy_version"],
            )

        return None

    @staticmethod
    def _normalise_warnings(
        warnings: list[Any] | None,
    ) -> list[WarningResponse]:
        normalised: list[WarningResponse] = []

        for warning in warnings or []:
            if isinstance(warning, dict):
                if "code" in warning and "message" in warning:
                    normalised.append(
                        WarningResponse.model_validate(
                            warning
                        )
                    )
                else:
                    normalised.append(
                        WarningResponse(
                            code="EVALUATION_WARNING",
                            message=str(warning),
                        )
                    )
            else:
                normalised.append(
                    WarningResponse(
                        code="EVALUATION_WARNING",
                        message=str(warning),
                    )
                )

        return normalised

    @staticmethod
    def _parse_stored_explanation(
        explanation: dict[str, Any] | None,
    ) -> ExplanationResponse | None:
        if not explanation:
            return None

        required = {
            "summary",
            "generated_by",
            "fallback_used",
        }

        if not required.issubset(explanation):
            return None

        return ExplanationResponse.model_validate(
            explanation
        )
