from sqlmodel import Enum, SQLModel, Field, Relationship, func
from sqlalchemy import Column, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from .users import User
    from .ict_personnel import IctPersonnel

class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class TicketCategory(str, Enum):
    hardware = "hardware"
    software = "software"
    network = "network"
    Access_Permissions = "Access & Permissions"
    security_Incidents = "security Incidents"
    other = "other"



class Ticket(SQLModel, table=True):
    __tablename__ = "Tickets"
    id: int = Field(primary_key=True)
    staff_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), nullable=False),
        foreign_key="staff.auth_user_id"
    )
    assigned_to: int = Field(nullable=False, foreign_key="ict_personnel.id")
    title: str = Field(index=True)
    description: str = Field(nullable=False)
    category: TicketCategory = Field(nullable=False)
    status: TicketStatus = Field(default=TicketStatus.open)
    created_at: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
        )
    
    resolved_at: datetime = Field(default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
        )
    
    users: Optional["User"] = Relationship(back_populates="tickets")
    ict_personnel: Optional["IctPersonnel"] = Relationship(back_populates="tickets")