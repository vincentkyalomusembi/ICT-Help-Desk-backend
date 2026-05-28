from fastapi import APIRouter, HTTPException

from app.services.supabase_client import get_assets, get_asset_allocations

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("/", summary="List assets")
async def list_assets():
    try:
        data = await get_assets()
        return {"data": data}
    except RuntimeError:
        raise HTTPException(status_code=503, detail="Supabase not configured")


@router.get("/allocations", summary="List asset allocations")
async def list_allocations():
    try:
        data = await get_asset_allocations()
        return {"data": data}
    except RuntimeError:
        raise HTTPException(status_code=503, detail="Supabase not configured")
