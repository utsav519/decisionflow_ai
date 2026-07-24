import pytest

from app.ai.explainer import Explainer
from app.ai.providers.mock_provider import MockProvider
from app.ai.schemas.explanation import ExplanationResult


@pytest.mark.asyncio
async def test_generate_explanation():
    provider = MockProvider(settings=None)
    explainer = Explainer(provider)

    result = await explainer.explain(
        policy_name="Approve Premium Customer",
        decision="APPROVE",
        input_data="credit_score=780, fraud_risk=10",
    )

    assert isinstance(result, ExplanationResult)
    assert result.generated_by == "AI"
    assert result.fallback_used is False
    assert "Loan approved" in result.summary