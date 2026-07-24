from app.ai.providers.gemini_provider import GeminiProvider


class DummySettings:
    GEMINI_API_KEY = "test-key"

    GEMINI_MODEL = "gemini-2.5-flash"

    LLM_MAX_OUTPUT_TOKENS = 2500


def test_provider_name():
    provider = GeminiProvider(DummySettings())

    assert provider.provider_name == "gemini"


def test_model_name():
    provider = GeminiProvider(DummySettings())

    assert provider.model_name == "gemini-2.5-flash"