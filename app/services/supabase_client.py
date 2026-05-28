from typing import Any, Dict, List, Optional
import asyncio

from app.core.supabase import supabase


async def get_assets() -> List[Dict[str, Any]]:
    """Fetch all rows from the `assets` table in Supabase."""
    if not supabase:
        raise RuntimeError("Supabase client not configured")

    def _fetch():
        res = supabase.table("assets").select("*").execute()
        # supabase-py returns a dict-like response with `data` key
        return getattr(res, "data", res.get("data") if isinstance(res, dict) else None) or []

    return await asyncio.to_thread(_fetch)


async def get_asset_allocations() -> List[Dict[str, Any]]:
    """Fetch all rows from the `asset_allocations` table in Supabase."""
    if not supabase:
        raise RuntimeError("Supabase client not configured")

    def _fetch():
        res = supabase.table("asset_allocations").select("*").execute()
        return getattr(res, "data", res.get("data") if isinstance(res, dict) else None) or []

    return await asyncio.to_thread(_fetch)
