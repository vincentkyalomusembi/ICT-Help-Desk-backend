from sqlmodel import SQLModel, Field, Relationship, func
from sqlalchemy import Column, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import uuid
import enum

if TYPE_CHECKING:
    from .users import User
    from .ict_personnel import IctPersonnel

class TicketStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"

class TicketCategory(str, enum.Enum):
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
    assigned_to_id: int = Field(
        sa_column=Column(ForeignKey("ict_personnel.id"), nullable=False)
    )
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
        sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now()),
    )

    resolved_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), onupdate=func.now()),
    )

    staff: Optional["User"] = Relationship(back_populates="tickets")
    assigned_to: Optional["IctPersonnel"] = Relationship(back_populates="assigned_tickets")