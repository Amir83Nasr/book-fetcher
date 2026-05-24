"""Application configuration using pydantic-settings.

Why pydantic-settings?
- Automatic .env file loading
- Type validation (port must be int, not string)
- Centralized config management
- IDE autocompletion
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra env vars
    )

    # PostgreSQL
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "bookdb"
    DB_USER: str = "postgres"
    DB_PASS: str = "secret"
    DB_MIN_CONN: int = 2
    DB_MAX_CONN: int = 10

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_CACHE_TTL: int = 300  # seconds

    # Application
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_RELOAD: bool = True


# Singleton instance - import this everywhere
settings = Settings()
