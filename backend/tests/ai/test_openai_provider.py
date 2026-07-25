from app.ai.providers.openai_provider import OpenAIProvider


class DummySettings:
    OPENAI_API_KEY = "test-key"

    OPENAI_MODEL = "gpt-4.1-mini"

    LLM_MAX_OUTPUT_TOKENS = 2500


def test_provider_name():
    provider = OpenAIProvider(DummySettings())

    assert provider.provider_name == "openai"


def test_model_name():
    provider = OpenAIProvider(DummySettings())

    assert provider.model_name == "gpt-4.1-mini"