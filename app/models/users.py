from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime


if TYPE_CHECKING:
    from .directorate import Directorate
    from .department import Department
    from .ict_personnel import IctPersonnel
    from .ticket import Ticket
    from .audit_logs import AuditLog
    from .asset_allocation import AssetAllocation

class UserRole(str, enum.Enum):
    admin = "ADMIN"
    staff = "STAFF"
    technician = "TECHNICIAN"

class User(SQLModel, table=True):
    __tablename__ = "staff"
    auth_user_id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    )
    personal_no: str = Field(index=True, unique=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    directorate_id: int = Field(foreign_key="directorates.id")
    department_id: int = Field(foreign_key="departments.id")
    office_number:str = Field(nullable=False)
    office_location: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.staff)
    failed_attempts: int = Field(default=0)
    is_activated: bool = Field(default=False)
    is_active: bool = Field(default=True)
    banned_until: Optional[datetime] = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=True)
    )
    directorate: Optional["Directorate"] = Relationship(back_populates="users") 
    department: Optional["Department"] = Relationship(back_populates="users")
    audit_logs: list["AuditLog"] = Relationship(back_populates="user")
    ict_profile: Optional["IctPersonnel"] = Relationship(back_populates="staff")
    tickets: List["Ticket"] = Relationship(back_populates="users")
    asset_allocations: List["AssetAllocation"] = Relationship(back_populates="staff")
