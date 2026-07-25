from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.dependencies import get_decision_service
from app.api.v1.decisions import router
from app.schemas.decision import (
    DecisionDetailResponse,
    DecisionEvaluationResponse,
    EvaluationMetrics,
    ResolutionResponse,
)


def build_evaluation_response() -> DecisionEvaluationResponse:
    return DecisionEvaluationResponse(
        evaluation_id="eval_test_001",
        request_id="req_test_001",
        decision="APPROVE",
        decision_confidence=95,
        winning_policy=None,
        matched_policies=[],
        unmatched_policies=[],
        skipped_policies=[],
        resolution=ResolutionResponse(
            decision="APPROVE",
            winning_policy_id=None,
            winning_policy_version=None,
            strategy="single_match",
            reason="Test resolution.",
            tie_breaker_used=False,
            competing_policy_ids=[],
        ),
        explanation=None,
        metrics=EvaluationMetrics(
            policies_loaded=1,
            policies_evaluated=1,
            policies_matched=1,
            policies_unmatched=0,
            policies_skipped=0,
            condition_count=2,
            conflicts_detected=0,
            engine_latency_ms=2.0,
            explanation_latency_ms=0.0,
            total_latency_ms=3.0,
        ),
        warnings=[],
        evaluated_at=datetime.now(timezone.utc),
    )


class FakeDecisionService:
    async def evaluate(
        self,
        *,
        request,
        actor_id: str,
        correlation_id: str,
    ) -> DecisionEvaluationResponse:
        assert request.request_id == "req_test_001"
        assert actor_id == "route_test_user"
        assert correlation_id == "cor_route_test_001"

        return build_evaluation_response()

    def get_decision(
        self,
        evaluation_id: str,
    ) -> DecisionDetailResponse:
        assert evaluation_id == "eval_test_001"

        data = build_evaluation_response().model_dump()

        return DecisionDetailResponse(
            **data,
            domain="telecom",
            customer_id="CUST-001",
        )


def create_client() -> TestClient:
    test_app = FastAPI()
    test_app.include_router(router)

    fake_service = FakeDecisionService()

    test_app.dependency_overrides[get_decision_service] = (
        lambda: fake_service
    )

    return TestClient(test_app)


def test_evaluate_decision_route() -> None:
    client = create_client()

    response = client.post(
        "/api/v1/decisions/evaluate",
        headers={
            "X-Correlation-ID": "cor_route_test_001",
            "X-User-ID": "route_test_user",
        },
        json={
            "request_id": "req_test_001",
            "domain": "telecom",
            "customer": {
                "customer_id": "CUST-001",
                "credit_score": 790,
                "fraud_risk_score": 0.12,
            },
            "context": {
                "channel": "ADMIN_PORTAL",
                "currency": "INR",
                "requested_action": "DEVICE_UPGRADE",
            },
            "options": {
                "include_explanation": True,
                "include_unmatched_rules": True,
                "include_condition_trace": True,
            },
        },
    )

    assert response.status_code == 201
    assert (
        response.headers["X-Correlation-ID"]
        == "cor_route_test_001"
    )

    payload = response.json()

    assert payload["success"] is True
    assert payload["correlation_id"] == "cor_route_test_001"
    assert payload["data"]["evaluation_id"] == "eval_test_001"
    assert payload["data"]["decision"] == "APPROVE"
    assert payload["data"]["decision_confidence"] == 95


def test_get_decision_route() -> None:
    client = create_client()

    response = client.get(
        "/api/v1/decisions/eval_test_001",
        headers={
            "X-Correlation-ID": "cor_route_get_001",
        },
    )

    assert response.status_code == 200
    assert (
        response.headers["X-Correlation-ID"]
        == "cor_route_get_001"
    )

    payload = response.json()

    assert payload["success"] is True
    assert payload["correlation_id"] == "cor_route_get_001"
    assert payload["data"]["evaluation_id"] == "eval_test_001"
    assert payload["data"]["domain"] == "telecom"
    assert payload["data"]["customer_id"] == "CUST-001"


def test_evaluate_decision_validation_error() -> None:
    client = create_client()

    response = client.post(
        "/api/v1/decisions/evaluate",
        json={
            "request_id": "req_invalid_001",
            "domain": "telecom",
            "customer": {
                "customer_id": "CUST-INVALID",
                "fraud_risk_score": 1.5,
            },
        },
    )

    assert response.status_code == 422
