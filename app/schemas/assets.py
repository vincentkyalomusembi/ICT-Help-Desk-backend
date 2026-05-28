from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.assets import DeviceType, AssetCondition, Brand


class AssetCreate(BaseModel):
    asset_tag: str
    serial_number: str
    device_type: DeviceType
    brand: Brand
    condition: Optional[AssetCondition] = AssetCondition.good
    purchase_date: Optional[date] = None
    warranty_expiry_date: Optional[date] = None


class AssetResponse(BaseModel):
    id: int
    asset_tag: str
    serial_number: str
    device_type: DeviceType
    brand: Brand
    condition: AssetCondition
    purchase_date: Optional[date]
    warranty_expiry_date: Optional[date]
    created_at: datetime

    model_config = {"from_attributes": True}


class AssetAllocationCreate(BaseModel):
    asset_id: int
    staff_id: str
    allocation_date: date
    return_date: Optional[date] = None
    notes: Optional[str] = None


class AssetAllocationResponse(BaseModel):
    id: int
    asset_id: int
    staff_id: str
    allocation_date: date
    return_date: Optional[date]
    notes: Optional[str]

    model_config = {"from_attributes": True}
