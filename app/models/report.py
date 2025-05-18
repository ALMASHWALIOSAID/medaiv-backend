from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import JSON
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from app.models.user import User

class Report(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    filename: str
    content_type: str
    text: str
    entities: Optional[dict] = Field(default=None, sa_column=Field(JSON))  # Corrected line

    owner_id: int = Field(default=None, foreign_key="user.id")
    owner: Mapped[Optional["User"]] = relationship(back_populates="reports")
