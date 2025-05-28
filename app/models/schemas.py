from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from pydantic import ConfigDict
from sqlmodel import SQLModel
from typing import Union


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    disabled: bool

    model_config = ConfigDict(from_attributes=True)

class ReportRead(SQLModel):
    id: int
    filename: str
    content_type: str
    text: str
    entities: Dict[str, List[str]]
    owner_id: int
  