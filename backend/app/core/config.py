"""
Central application settings.

Reads from environment variables and .env file.
Constructs DATABASE_URL from individual MySQL components
to handle special characters in passwords safely.

Spec reference: §8 Configuration Management
"""

from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-wide configuration loaded from environment."""

    app_name: str = "DecisionFlow AI"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"

    # MySQL connection components
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_database: str = "decisionflow"
    mysql_user: str = "decisionflow"
    mysql_password: str = "decisionflow"

    # Policy defaults
    default_policy_priority: int = 100
    max_policy_priority: int = 1000
    default_page_size: int = 20
    max_page_size: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """Construct MySQL URL with properly escaped password."""
        password = quote_plus(self.mysql_password)
        return (
            f"mysql+pymysql://{self.mysql_user}:{password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
