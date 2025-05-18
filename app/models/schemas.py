from pydantic import BaseModel
from typing import Optional, Dict, List

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    disabled: bool

    class Config:
        orm_mode = True

class ReportRead(BaseModel):
    id: int
    filename: str
    content_type: str
    text: str
    entities: Dict[str, List[str]]
    owner_id: int

    class Config:
        orm_mode = True