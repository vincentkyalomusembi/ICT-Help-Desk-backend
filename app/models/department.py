from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING   
if TYPE_CHECKING:
    from .users import User
    from .directorate import Directorate


class Department(SQLModel, table=True):
    __tablename__="departments"
    id: Optional[int] = Field(primary_key=True)
    directorate_id: int = Field(foreign_key="directorates.id")
    name: str = Field(index=True, unique=True)

    users:List["User"] = Relationship(back_populates="department")  
    directorate: Optional["Directorate"]=Relationship(back_populates="department")