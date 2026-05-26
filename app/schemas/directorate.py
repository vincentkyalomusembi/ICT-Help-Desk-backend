from pydantic import BaseModel

class DirectorateResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True