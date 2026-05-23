from sqlmodel import SQLModel, Field
from typing import Optional

class Directorate(SQLModel, table=True):
    __tablename__="directorates"
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(index=True, unique=True)

    