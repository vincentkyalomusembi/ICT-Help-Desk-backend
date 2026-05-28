from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session
from app.services.asset_service import AssetService
from app.services.asset_allocation_service import AssetAllocationService
from app.schemas.assets import (
    AssetCreate,
    AssetResponse,
    AssetAllocationCreate,
    AssetAllocationResponse,
)
from app.models.assets import Asset

router = APIRouter(prefix="/api/assets", tags=["assets"])


@router.post("/", response_model=AssetResponse, status_code=201)
async def create_asset(payload: AssetCreate, db: AsyncSession = Depends(get_session)):
    service = AssetService(db)
    asset = await service.create_asset(payload)
    if not asset:
        raise HTTPException(status_code=400, detail="Unable to create asset")
    return asset


@router.get("/", response_model=list[AssetResponse])
async def list_assets(limit: int = 100, db: AsyncSession = Depends(get_session)):
    service = AssetService(db)
    return await service.list_assets(limit=limit)


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: int, db: AsyncSession = Depends(get_session)):
    service = AssetService(db)
    asset = await service.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.delete("/{asset_id}")
async def delete_asset(asset_id: int, db: AsyncSession = Depends(get_session)):
    service = AssetService(db)
    await service.delete_asset(asset_id)
    return {"detail": "deleted"}


@router.post("/allocations", response_model=AssetAllocationResponse, status_code=201)
async def allocate_asset(payload: AssetAllocationCreate, db: AsyncSession = Depends(get_session)):
    service = AssetAllocationService(db)
    alloc = await service.create_allocation(payload)
    if not alloc:
        raise HTTPException(status_code=400, detail="Unable to allocate asset")
    return alloc


@router.get("/allocations", response_model=list[AssetAllocationResponse])
async def list_allocations(limit: int = 100, db: AsyncSession = Depends(get_session)):
    service = AssetAllocationService(db)
    return await service.list_allocations(limit=limit)


@router.post("/allocations/{allocation_id}/return", response_model=AssetAllocationResponse)
async def return_allocation(allocation_id: int, return_date: str, db: AsyncSession = Depends(get_session)):
    service = AssetAllocationService(db)
    alloc = await service.return_allocation(allocation_id, return_date)
    if not alloc:
        raise HTTPException(status_code=404, detail="Allocation not found")
    return alloc
