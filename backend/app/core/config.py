from enum import StrEnum
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvironment(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    """
    Application configuration.

    All configuration values are loaded from the .env file.
    """

    # ======================================
    # Application
    # ======================================

    app_name: str = Field(..., alias="APP_NAME")
    app_version: str = Field(..., alias="APP_VERSION")
    app_env: AppEnvironment = Field(..., alias="APP_ENV")
    app_debug: bool = Field(..., alias="APP_DEBUG")


    # ======================================
    # API
    # ======================================


    api_prefix: str = Field(..., alias="API_PREFIX")

    # ======================================
    # Logging
    # ======================================

    log_level: LogLevel = Field(..., alias="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    Using lru_cache ensures that the .env file is read only once
    during the application lifetime.
    """
    return Settings()


settings = get_settings()
