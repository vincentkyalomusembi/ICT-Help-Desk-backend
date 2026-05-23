from sqlmodel import SQLModel, Field
from typing import Optional

class Department(SQLModel, table=True):
    __tablename__="departments"
    id: Optional[int] = Field(primary_key=True)
    directorate_id: int = Field(foreign_key="directorates.id")
    name: str = Field(index=True, unique=True)