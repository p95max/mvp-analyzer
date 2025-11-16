"""Application configuration using Pydantic settings."""

from functools import lru_cache
from typing import Literal, Optional

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
    )

    app_env: Literal["local", "dev", "prod"] = Field(default="local", alias="APP_ENV")
    log_level: str = Field(default="info", alias="LOG_LEVEL")

    external_api_base_url: AnyHttpUrl = Field(
        default="https://jsonplaceholder.typicode.com",
        alias="EXTERNAL_API_BASE_URL",
    )

    cache_ttl_seconds: int = Field(default=600, alias="CACHE_TTL_SECONDS")
    ai_max_sample_items: int = Field(default=20, alias="AI_MAX_SAMPLE_ITEMS")

    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")


@lru_cache
def get_settings() -> Settings:
    return Settings()
