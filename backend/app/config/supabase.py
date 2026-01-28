"""Supabase client configuration."""
from functools import lru_cache

from supabase import create_client, Client

from .settings import settings


@lru_cache
def get_supabase_client() -> Client:
    """Get cached Supabase client instance."""
    if not settings.supabase_url or not settings.supabase_key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY must be set in environment variables"
        )
    return create_client(settings.supabase_url, settings.supabase_key)
