from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import uuid
import enum

if TYPE_CHECKING:
    from .users import User

class AuditAction(str, enum.Enum):
    """Enum for audit log action types."""
    TICKET_CREATED = "TICKET_CREATED"
    TICKET_UPDATED = "TICKET_UPDATED"
    TICKET_ASSIGNED = "TICKET_ASSIGNED"
    TICKET_CLOSED = "TICKET_CLOSED"
    ASSET_ALLOCATED = "ASSET_ALLOCATED"
    ASSET_DEALLOCATED = "ASSET_DEALLOCATED"
    USER_CREATED = "USER_CREATED"
    USER_UPDATED = "USER_UPDATED"
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILED = "LOGIN_FAILED"
    LOGOUT = "LOGOUT"
    PERMISSION_CHANGED = "PERMISSION_CHANGED"
    PASSWORD_RESET = "PASSWORD_RESET"

class AuditLog(SQLModel, table=True):
    """Audit log model for tracking all system actions."""
    __tablename__ = "audit_logs"
    
    log_id: Optional[int] = Field(default=None, primary_key=True)
    staff_id: Optional[uuid.UUID] = Field(default=None, foreign_key="staff.auth_user_id")
    action: AuditAction = Field(nullable=False, index=True)
    table_name: str = Field(max_length=50, nullable=False, index=True)
    record_id: Optional[int] = Field(default=None)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    mac_address: Optional[str] = Field(default=None, max_length=17)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(TIMESTAMP(timezone=True), server_default="now()")
    )
    user: Optional["User"] = Relationship(back_populates="audit_logs")

class AuditLogCreate(SQLModel):
    """Schema for creating audit log entries."""
    staff_id: Optional[uuid.UUID] = None
    action: str
    table_name: str
    record_id: Optional[int] = None
    ip_address: Optional[str] = None

class AuditLogResponse(SQLModel):
    """Response schema for audit log entries."""
    log_id: int
    staff_id: Optional[uuid.UUID]
    action: str
    table_name: str
    record_id: Optional[int]
    ip_address: Optional[str]
    mac_address: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True      