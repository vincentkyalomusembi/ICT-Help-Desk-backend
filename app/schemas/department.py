from pydantic import BaseModel

class DepartmentResponse(BaseModel):
    id: int
    name: str
    directorate_id: int

    class Config:
        from_attributes = True