from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import date
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .assets import Asset
    from .users import User


class AssetAllocation(SQLModel, table=True):
    __tablename__ = "asset_allocations"

    id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="assets.id")
    staff_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), ForeignKey("staff.auth_user_id"), nullable=False)
    )
    allocation_date: date
    return_date: Optional[date] = Field(default=None)
    notes: Optional[str] = Field(default=None)

    asset: Optional["Asset"] = Relationship(back_populates="allocations")
    staff: Optional["User"] = Relationship(back_populates="asset_allocations")