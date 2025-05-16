from datetime import datetime
from typing import Dict, List

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel

class Report(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    filename: str = Field(nullable=False)
    content_type: str = Field(nullable=False)
    text: str = Field(nullable=False)
    entities: Dict[str, List[str]] = Field(
        sa_column=Column(JSON, nullable=False),
        default_factory=dict
    )
