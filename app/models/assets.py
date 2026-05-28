from sqlmodel import SQLModel,Field,Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP
import enum
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING,List

if TYPE_CHECKING:
  from .asset_allocation import AssetAllocation

class DeviceType(str, enum.Enum):
    laptop = "Laptop"
    desktop = "Desktop"
    monitor = "Monitor"
    printer = "Printer"
    other = "Other"

class AssetCondition(str, enum.Enum):
    good = "Good"
    fair = "Fair"
    poor = "Poor"
    decommissioned = "Decommissioned"

class Brand(str, enum.Enum):
    dell = "Dell"
    hp = "HP"
    lenovo = "Lenovo"
    apple = "Apple"
    asus = "Asus"
    acer = "Acer"
    huawei = "Huawei"
    other = "Other"

class Asset(SQLModel, table=True):
    __tablename__ = "assets"
assets_id: int = Field(default=None, primary_key=True)
asset_tag: str = Field(max_length=50, index=True, unique=True)
serial_number: str = Field(max_length=100, index=True, unique=True)
device_type: DeviceType
brand: Brand 
condition: AssetCondition = Field(default=AssetCondition.good)
purchase_date: Optional [date] = Field(default=None)
warranty_expiry_date: Optional [date] = Field(default=None)
created_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False))

allocations: List ["AssetAllocation"]  = Relationship(back_populates="asset")