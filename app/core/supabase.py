from supabase import create_client, Client
from typing import Optional
from app.core.config import settings

def get_auth_supabase_client() -> Optional[Client]:
    if settings.SUPABASE_URL and (settings.SUPABASE_ANON_KEY or settings.SUPABASE_SERVICE_ROLE_KEY):
        return create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY or settings.SUPABASE_SERVICE_ROLE_KEY,
        )
    return None

def get_admin_supabase_client() -> Optional[Client]:
    if settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY:
        return create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY,
        )
    return None


# Backward-compatible alias for code that expects a single client.
supabase = get_auth_supabase_client()