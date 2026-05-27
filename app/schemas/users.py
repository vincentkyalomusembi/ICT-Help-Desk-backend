from pydantic import BaseModel, ConfigDict, EmailStr
from app.models import UserRole
from uuid import UUID
class UserCreate(BaseModel):
    personal_no: str
    email: EmailStr
    first_name: str
    last_name: str 
    phone: str
    directorate_id: int 
    department_id: int 
    office_number:str 
    office_location: str
    password: str


class UserResponse(BaseModel):
    auth_user_id: UUID
    personal_no: str
    email: EmailStr
    first_name: str
    last_name: str 
    phone: str
    directorate_id: int 
    department_id: int 
    office_number:str 
    office_location: str
    role: UserRole
    is_activated: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    directorate_id: int | None = None
    department_id: int | None = None
    office_number:str | None = None
    office_location: str | None = None
