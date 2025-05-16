# app/models/schemas.py

from pydantic import BaseModel
from typing import Optional, Dict, List

class ReportEntities(BaseModel):
    entities: Dict[str, List[str]]

class OCRResponse(BaseModel):
    text: str
    entities: Dict[str, List[str]]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str
