from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .ticket import Ticket


class Specialization(str, enum.Enum):
    hardware = "HARDWARE"
    networking = "NETWORKING"
    software_and_systems = "SOFTWARE_AND_SYSTEMS"
    security = "SECURITY"


class Availability(str, enum.Enum):
    available = "AVAILABLE"
    busy = "BUSY"
    off_duty = "OFF_DUTY"
    on_leave = "ON_LEAVE"


class IctPersonnel(SQLModel, table=True):
    __tablename__ = "ict_personnel"

    id: Optional[int] = Field(default=None, primary_key=True)
    staff_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), ForeignKey("staff.auth_user_id"), unique=True, nullable=False)
    )
    specialization: Specialization = Field(default=Specialization.hardware)
    availability: Availability = Field(default=Availability.available)
    phone_extension: Optional[str] = Field(default=None, max_length=10)
    is_active: bool = Field(default=True)

    staff: Optional["User"] = Relationship(back_populates="ict_profile")
    assigned_tickets: List["Ticket"] = Relationship(back_populates="assignee")