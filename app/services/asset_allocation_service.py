from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.asset_allocation import AssetAllocation
from app.schemas.assets import AssetAllocationCreate
from datetime import datetime
from app.services.audit_service import AuditService


class AssetAllocationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_allocation(self, payload: AssetAllocationCreate, staff_id: Optional[str] = None) -> AssetAllocation:
        alloc = AssetAllocation(
            asset_id=payload.asset_id,
            staff_id=payload.staff_id,
            allocation_date=payload.allocation_date,
            return_date=payload.return_date,
            notes=payload.notes,
        )
        self.db.add(alloc)
        await self.db.commit()
        await self.db.refresh(alloc)

        audit = AuditService(self.db)
        await audit.log_action(action="ASSET_ALLOCATED", table_name="asset_allocations", staff_id=staff_id, record_id=alloc.id)

        return alloc

    async def list_allocations(self, limit: int = 100) -> List[AssetAllocation]:
        query = select(AssetAllocation).order_by(desc(AssetAllocation.allocation_date)).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_allocation(self, allocation_id: int) -> Optional[AssetAllocation]:
        query = select(AssetAllocation).where(AssetAllocation.id == allocation_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def return_allocation(self, allocation_id: int, return_date, staff_id: Optional[str] = None) -> Optional[AssetAllocation]:
        alloc = await self.get_allocation(allocation_id)
        if not alloc:
            return None
        alloc.return_date = return_date
        self.db.add(alloc)
        await self.db.commit()
        await self.db.refresh(alloc)

        audit = AuditService(self.db)
        await audit.log_action(action="ASSET_RETURNED", table_name="asset_allocations", staff_id=staff_id, record_id=alloc.id)

        return alloc
