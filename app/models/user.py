# app/models/user.py

from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, index=True, unique=True)
    hashed_password: str = Field(nullable=False)
    disabled: bool = Field(default=False)
