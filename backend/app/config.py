"""Application settings. Values come from env vars (prefix APP_) or defaults.

No provider API keys live here -- keys arrive per request from the client.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = "Deep Research Studio API"
    version: str = "0.1.0"
    log_level: str = "INFO"

    # Comma-separated list of allowed CORS origins ("*" allows all).
    cors_origins: str = "*"

    # Seconds allowed for a single provider call.
    request_timeout: float = 120.0

    # Research defaults (overridable per request where noted).
    default_max_subquestions: int = 4
    search_max_results: int = 5

    # Default model per provider (client may override per request).
    openai_default_model: str = "gpt-5.1"
    anthropic_default_model: str = "claude-opus-5-5"
    kimi_default_model: str = "kimi-k2-0905-preview"
    kimi_base_url: str = "https://api.moonshot.ai/v1"

    @property
    def origins_list(self) -> list[str]:
        items = [o.strip() for o in self.cors_origins.split(",") if o.strip()]
        return items or ["*"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
