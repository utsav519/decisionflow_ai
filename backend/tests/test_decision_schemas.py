import pytest
from pydantic import ValidationError

from app.schemas.decision import DecisionEvaluationRequest


def test_valid_decision_request() -> None:
    request = DecisionEvaluationRequest.model_validate({
        "request_id": "req_schema_001",
        "domain": "telecom",
        "customer": {
            "customer_id": "CUST-001",
            "customer_tenure_months": 36,
            "credit_score": 790,
            "payment_defaults": 0,
            "fraud_risk_score": 0.12,
        },
        "context": {
            "channel": "ADMIN_PORTAL",
            "currency": "INR",
            "requested_action": "DEVICE_UPGRADE",
        },
    })

    assert request.request_id == "req_schema_001"
    assert request.customer.credit_score == 790
    assert request.options.include_explanation is True


def test_rejects_invalid_fraud_risk_score() -> None:
    with pytest.raises(ValidationError):
        DecisionEvaluationRequest.model_validate({
            "request_id": "req_schema_002",
            "domain": "telecom",
            "customer": {
                "customer_id": "CUST-002",
                "fraud_risk_score": 1.5,
            },
        })


def test_rejects_negative_payment_defaults() -> None:
    with pytest.raises(ValidationError):
        DecisionEvaluationRequest.model_validate({
            "request_id": "req_schema_003",
            "domain": "telecom",
            "customer": {
                "customer_id": "CUST-003",
                "payment_defaults": -1,
            },
        })


def test_requires_evaluable_customer_field() -> None:
    with pytest.raises(ValidationError):
        DecisionEvaluationRequest.model_validate({
            "request_id": "req_schema_004",
            "domain": "telecom",
            "customer": {
                "customer_id": "CUST-004",
            },
        })


def test_rejects_unknown_customer_field() -> None:
    with pytest.raises(ValidationError):
        DecisionEvaluationRequest.model_validate({
            "request_id": "req_schema_005",
            "domain": "telecom",
            "customer": {
                "customer_id": "CUST-005",
                "customer_loyalty_aura": 90,
            },
        })
