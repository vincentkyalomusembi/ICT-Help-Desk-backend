from sqlmodel import SQLModel, Field, Relationship  
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .department import Department

class Directorate(SQLModel, table=True):
    __tablename__="directorates"
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(index=True, unique=True)

    users:List["User"] = Relationship(back_populates="directorate")
    department:List["Department"]=Relationship(back_populates="directorate")
    