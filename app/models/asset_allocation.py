from sqlmodel import SQLModel, Field,Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql
import UUID
import uuid
from datetime import date
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .assets import Asset
    from .users import User


class AssetAllocation(SQLModel, table=True):
    __tablename__ = "asset_allocations"
    allocation_id: Optional[int] = Field(primary_key=True)
    asset_id: int = Field(foreign_key="assets.assets_id")
    staff_id: int = uuid.UUID = Field(
        sa_column= Column(UUID(as_uuid=True), nullable=False, unique=True)
        )
    allocation_date: date
    return_date: Optional[date] = Field(default=None)
    notes: Optional[str] = Field(default=None)
       

    asset: Optional["Asset"] = Relationship(back_populates="asset_allocations")
    staff: Optional["User"] = Relationship(back_populates="asset_allocations")