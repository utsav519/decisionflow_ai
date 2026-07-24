"""
Central application settings.

Loads backend, database, and AI configuration from environment
variables or a local .env file.

Constructs DATABASE_URL from individual MySQL components while safely
escaping special characters in credentials.

Spec reference: §8 Configuration Management
"""

from __future__ import annotations

from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-wide configuration loaded from environment variables."""

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    app_name: str = "DecisionFlow AI"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"

    # ------------------------------------------------------------------
    # MySQL
    # ------------------------------------------------------------------

    mysql_host: str = "localhost"
    mysql_port: int = Field(default=3306, gt=0, le=65535)
    mysql_database: str = "decisionflow"
    mysql_user: str = "decisionflow"
    mysql_password: str = "decisionflow"

    # ------------------------------------------------------------------
    # Policy defaults
    # ------------------------------------------------------------------

    default_policy_priority: int = Field(default=100, ge=0)
    max_policy_priority: int = Field(default=1000, ge=0)

    default_page_size: int = Field(default=20, gt=0)
    max_page_size: int = Field(default=100, gt=0)

    # ------------------------------------------------------------------
    # LLM provider
    # ------------------------------------------------------------------

    LLM_PROVIDER: str = Field(
        default="mock",
        description="Configured LLM provider.",
    )

    # ------------------------------------------------------------------
    # Provider models
    # ------------------------------------------------------------------

    GROQ_MODEL: str = Field(
        default="llama-3.3-70b-versatile",
        description="Groq model name.",
    )

    OPENAI_MODEL: str = Field(
        default="gpt-4.1-mini",
        description="OpenAI model name.",
    )

    GEMINI_MODEL: str = Field(
        default="gemini-2.5-flash",
        description="Gemini model name.",
    )

    ANTHROPIC_MODEL: str = Field(
        default="claude-sonnet-4-20250514",
        description="Anthropic model name.",
    )

    # ------------------------------------------------------------------
    # Generation settings
    # ------------------------------------------------------------------

    LLM_TEMPERATURE: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0,
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
    # Provider API keys
    # ------------------------------------------------------------------

    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # ------------------------------------------------------------------
    # AI feature flags
    # ------------------------------------------------------------------

    USE_MOCK_LLM: bool = True

    ENABLE_AI_POLICY_GENERATION: bool = True
    ENABLE_AI_EXPLANATION: bool = True
    ENABLE_AI_TEST_GENERATION: bool = True
    ENABLE_AI_CONFLICT_EXPLANATION: bool = True

    # ------------------------------------------------------------------
    # Pydantic settings
    # ------------------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """Construct a MySQL SQLAlchemy URL with escaped credentials."""
        username = quote_plus(self.mysql_user)
        password = quote_plus(self.mysql_password)

        return (
            f"mysql+pymysql://{username}:{password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return Settings()


settings = get_settings()