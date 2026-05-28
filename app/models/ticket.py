import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .users import User
    from .ict_personnel import IctPersonnel

class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"

class TicketCategory(str, Enum):
    hardware = "hardware"
    software = "software"
    network = "network"
    access_permissions = "Access & Permissions"
    security_incidents = "security Incidents"
    other = "other"

class Ticket(SQLModel, table=True):
    __tablename__ = "Tickets"

    id: int = Field(primary_key=True)
    staff_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), ForeignKey("staff.auth_user_id"), nullable=False)
    )
    assigned_to: int = Field(foreign_key="ict_personnel.id")
    title: str = Field(index=True)
    description: str = Field(nullable=False)
    category: TicketCategory = Field(
        sa_column=Column(SAEnum(TicketCategory), nullable=False)
    )
    status: TicketStatus = Field(
        sa_column=Column(SAEnum(TicketStatus), nullable=False, default=TicketStatus.open)
    )
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    )
    resolved_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )

    users: Optional["User"] = Relationship(back_populates="tickets")
    ict_personnel: Optional["IctPersonnel"] = Relationship(back_populates="tickets")