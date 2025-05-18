from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import Mapped

class UserBase(SQLModel):
    username: str

class User(UserBase, table=True):
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    disabled: bool = Field(default=False)
    reports: Mapped[List["Report"]] = Relationship(back_populates="owner")  # type: ignore