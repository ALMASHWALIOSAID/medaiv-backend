from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

# register models so metadata knows about them
import app.models.user  # noqa
import app.models.report  # noqa

engine = create_engine(settings.DATABASE_URL, echo=settings.SQLALCHEMY_ECHO)

def get_session():
    with Session(engine) as session:
        yield session