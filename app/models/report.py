from datetime import datetime
from typing import Optional, Dict, List
from huggingface_hub import User
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from sqlalchemy.orm import Mapped

class Report(SQLModel, table=True):
    __tablename__ = "report"
    id: Optional[int] = Field(default=None, primary_key=True)
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    filename: str
    content_type: str
    text: str
    entities: Dict[str, List[str]] = Field(sa_column=Column(JSON), default_factory=dict)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Mapped[Optional[User]] = Relationship(back_populates="reports")