import asyncio

from app.ai.explainer import Explainer
from app.ai.providers.mock_provider import MockProvider
from app.core.config import get_settings
from app.services.decision_service import DecisionService
from app.services.explanation_service import ExplanationService


def test_contract_fields_map_to_seed_policy_paths() -> None:
    result = DecisionService._build_engine_data(
        customer_data={
            "customer_tenure_months": 36,
            "payment_defaults": 0,
            "customer_segment": "PREMIUM",
            "outstanding_balance": 0,
            "account_status": "CURRENT",
        },
        context_data={},
    )

    assert result["customer"]["tenure_months"] == 36
    assert result["customer"]["payment_history_defaults"] == 0
    assert result["customer"]["plan_type"] == "premium"
    assert result["account"]["outstanding_balance"] == 0
    assert result["account"]["status"] == "current"


class ExplainerMustNotRun:
    async def explain(self, *args, **kwargs):
        raise AssertionError(
            "AI must not run when deterministic evidence is incomplete."
        )


def test_missing_fields_use_deterministic_fallback() -> None:
    service = ExplanationService(
        explainer=ExplainerMustNotRun(),
    )

    outcome = asyncio.run(
        service.explain(
            evidence={
                "decision": "MANUAL_REVIEW",
                "winning_policy": None,
                "matched_policies": [],
                "missing_fields": ["customer.credit_score"],
            },
            correlation_id="cor_test_fallback",
        )
    )

    assert outcome.explanation.generated_by == (
        "DETERMINISTIC_FALLBACK"
    )
    assert outcome.explanation.fallback_used is True


def test_mock_explanation_respects_rejection() -> None:
    provider = MockProvider(get_settings())
    explainer = Explainer(provider)

    result = asyncio.run(
        explainer.explain(
            policy_name="Fraud rejection",
            decision="REJECT",
            input_data="{}",
        )
    )

    assert result.generated_by == "AI"
    assert "rejected" in result.summary.lower()
    assert "approved" not in result.summary.lower()
