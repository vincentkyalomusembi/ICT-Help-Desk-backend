from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.assets import Asset
from app.schemas.assets import AssetCreate
from datetime import datetime
from app.services.audit_service import AuditService


class AssetService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_asset(self, payload: AssetCreate, staff_id: Optional[str] = None) -> Asset:
        asset = Asset(
            asset_tag=payload.asset_tag,
            serial_number=payload.serial_number,
            device_type=payload.device_type,
            brand=payload.brand,
            condition=payload.condition,
            purchase_date=payload.purchase_date,
            warranty_expiry_date=payload.warranty_expiry_date,
            created_at=datetime.utcnow(),
        )
        self.db.add(asset)
        await self.db.commit()
        await self.db.refresh(asset)

        # log audit
        audit = AuditService(self.db)
        await audit.log_action(
            action="ASSET_CREATED", table_name="assets", staff_id=staff_id, record_id=asset.id
        )

        return asset

    async def list_assets(self, limit: int = 100) -> List[Asset]:
        query = select(Asset).order_by(desc(Asset.created_at)).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_asset(self, asset_id: int) -> Optional[Asset]:
        query = select(Asset).where(Asset.id == asset_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def delete_asset(self, asset_id: int, staff_id: Optional[str] = None) -> None:
        asset = await self.get_asset(asset_id)
        if not asset:
            return None
        await self.db.delete(asset)
        await self.db.commit()
        audit = AuditService(self.db)
        await audit.log_action(action="ASSET_DELETED", table_name="assets", staff_id=staff_id, record_id=asset_id)
