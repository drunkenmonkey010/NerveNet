from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    Values are loaded from environment variables and the local .env file.
    Environment variables take precedence over .env values.
    """

    app_name: str = "NerveNet"
    app_env: str = "development"
    app_version: str = "0.1.0"

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    database_url: str

    log_level: str = "INFO"

    data_storage_path: str = "./data"
    model_storage_path: str = "./models"

    blockchain_provider: str = "local"

    redis_url: str | None = None

    llm_provider: str | None = None
    llm_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached application settings object.

    Caching ensures that we don't repeatedly parse configuration
    throughout the lifetime of the application.
    """

    return Settings()