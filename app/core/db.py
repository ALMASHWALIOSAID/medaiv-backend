# app/core/db.py
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
from app.core.config import settings

if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.SQLALCHEMY_ECHO,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.SQLALCHEMY_ECHO,
    )

def get_session():
    with Session(engine) as session:
        yield session