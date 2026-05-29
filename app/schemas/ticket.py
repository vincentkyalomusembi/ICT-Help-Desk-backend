from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.ticket import TicketStatus, TicketCategory

class TicketCreate(BaseModel):
    title: str
    description: str
    category: TicketCategory
    assigned_to_id: int

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[TicketCategory] = None
    status: Optional[TicketStatus] = None
    assigned_to_id: Optional[int] = None
    resolved_at: Optional[datetime] = None

class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  

    id: int
    staff_id: int
    assigned_to_id: int
    title: str
    description: str
    category: TicketCategory
    status: TicketStatus
    created_at: datetime
    resolved_at: Optional[datetime] = None