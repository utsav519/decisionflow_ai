from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables (.env).

    Example:
        LLM_PROVIDER=groq
        GROQ_API_KEY=gsk_xxxxxxxxx
    """

    # ------------------------------------------------------------------
    # LLM Configuration
    # ------------------------------------------------------------------

    LLM_PROVIDER: str = Field(
        default="mock",
        description="Configured LLM provider.",
    )

    LLM_MODEL: str = Field(
        default="llama-3.3-70b-versatile",
        description="Model name to use.",
    )

    LLM_TEMPERATURE: float = Field(
        default=0.0,
        ge=0,
        le=2,
    )

    LLM_TIMEOUT_SECONDS: int = Field(
        default=20,
        gt=0,
    )

    LLM_MAX_OUTPUT_TOKENS: int = Field(
        default=2500,
        gt=0,
    )

    LLM_MAX_RETRIES: int = Field(
        default=2,
        ge=0,
    )

    # ------------------------------------------------------------------
    # Provider Keys
    # ------------------------------------------------------------------

    GROQ_API_KEY: str = ""

    OPENAI_API_KEY: str = ""

    GEMINI_API_KEY: str = ""

    ANTHROPIC_API_KEY: str = ""

    # ------------------------------------------------------------------
    # Feature Flags
    # ------------------------------------------------------------------

    USE_MOCK_LLM: bool = True

    ENABLE_AI_POLICY_GENERATION: bool = True

    ENABLE_AI_EXPLANATION: bool = True

    ENABLE_AI_TEST_GENERATION: bool = True

    ENABLE_AI_CONFLICT_EXPLANATION: bool = True

    # ------------------------------------------------------------------
    # Pydantic Settings
    # ------------------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    This ensures configuration is loaded only once.
    """
    return Settings()


settings = get_settings()