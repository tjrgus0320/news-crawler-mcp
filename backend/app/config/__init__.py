"""Configuration module."""
from .settings import settings
from .supabase import get_supabase_client

__all__ = ["settings", "get_supabase_client"]
