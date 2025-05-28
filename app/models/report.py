# app/models/report.py

from typing import Optional, TYPE_CHECKING, Dict, List
from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    content_type: str
    text: str

    # tell SQLModel "this is a JSON column in SQLite, default to {}"
    entities: Dict[str, List[str]] = Field(default_factory=dict, sa_column=Column(JSON))
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="reports")

