from pydantic import BaseModel, ConfigDict

class DepartmentResponse(BaseModel):
    id: int
    name: str
    directorate_id: int

    model_config = ConfigDict(from_attributes=True)