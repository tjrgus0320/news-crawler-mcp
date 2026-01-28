"""Application settings using pydantic-settings."""
import json
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""

    # CORS
    cors_origins: str = '["http://localhost:5173","http://localhost:3000"]'

    # Scheduler
    scheduler_enabled: bool = True
    crawl_hour: int = 9
    crawl_minute: int = 0
    timezone: str = "Asia/Seoul"

    # Crawling
    max_articles_per_category: int = 30

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from JSON string."""
        try:
            return json.loads(self.cors_origins)
        except json.JSONDecodeError:
            return ["http://localhost:5173", "http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
