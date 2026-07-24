from __future__ import annotations

from app.ai.exceptions import AIUnsupportedProviderError
from app.ai.providers.base import LLMProvider
from app.ai.providers.mock_provider import MockProvider
from app.ai.providers.groq_provider import GroqProvider

# These providers will be implemented later.
# Keep imports here so the factory remains the single
# provider selection point.

# from app.ai.providers.openai_provider import OpenAIProvider
# from app.ai.providers.gemini_provider import GeminiProvider
# from app.ai.providers.anthropic_provider import AnthropicProvider
# from app.ai.providers.groq_provider import GroqProvider


def get_llm_provider(settings) -> LLMProvider:
    """
    Returns the configured LLM provider.

    This is the ONLY place that decides which provider
    implementation should be used.
    """

    provider = settings.LLM_PROVIDER.lower()

    if provider == "mock":
        return MockProvider(settings)

    # Uncomment as implementations become available.

    # if provider == "openai":
    #     return OpenAIProvider(settings)

    # if provider == "gemini":
    #     return GeminiProvider(settings)

    # if provider == "anthropic":
    #     return AnthropicProvider(settings)

    if provider == "groq":
        return GroqProvider(settings)

    raise AIUnsupportedProviderError(provider)