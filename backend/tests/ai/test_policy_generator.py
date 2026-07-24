from app.ai.policy_generator import PolicyGenerator
from app.ai.providers.mock_provider import MockProvider
from app.ai.schemas.policy_generation import (
    AIPolicyGenerationInput,
    AIPolicyGenerationResult,
)


def test_generate_policy():
    provider = MockProvider(settings=None)
    generator = PolicyGenerator(provider)

    request = AIPolicyGenerationInput(
        policy_text="Approve customers with credit score above 750.",
        domain="Loan",
    )

    result = generator.generate(request)

    assert isinstance(result, AIPolicyGenerationResult)
    assert result.generated_policy.policy_name == "Approve Premium Customer"
    assert result.validation_status == "VALID"