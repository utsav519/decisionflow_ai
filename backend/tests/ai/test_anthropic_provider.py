from app.ai.providers.anthropic_provider import AnthropicProvider


class DummySettings:
    ANTHROPIC_API_KEY = "test-key"

    ANTHROPIC_MODEL = "claude-sonnet-4-20250514"

    LLM_MAX_OUTPUT_TOKENS = 2500


def test_provider_name():
    provider = AnthropicProvider(DummySettings())

    assert provider.provider_name == "anthropic"


def test_model_name():
    provider = AnthropicProvider(DummySettings())

    assert provider.model_name == "claude-sonnet-4-20250514"