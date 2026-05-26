from pydantic import BaseModel, EmailStr
from uuid import UUID
from app.models.users import UserRole


class UserCreate(BaseModel):
    personal_no: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone_number: str
    directorate_id: int
    department_id: int
    office_number: str
    office_location: str

class UserResponse(BaseModel):
    auth_user_id: UUID
    personal_no: str
    first_name: str
    last_name: str
    email: EmailStr
    directorate_id: int
    department_id: int
    office_number: str
    office_location: str
    role: UserRole
    is_activated: bool
    is_active: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    office_number: str | None = None
    office_location: str | None = None
    directorate_id: int | None = None
    department_id: int | None = None