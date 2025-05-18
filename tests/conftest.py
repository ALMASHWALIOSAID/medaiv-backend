import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel
from app.core.db import engine
from app.main import app

@pytest.fixture(scope="module", autouse=True)
def prepare_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
