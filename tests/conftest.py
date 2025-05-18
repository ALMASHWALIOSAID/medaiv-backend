import os
import sys

# ensure the project root is on sys.path so "import app" works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from app.core.db import engine
from app.main import app

# automatically create/drop the DB schema once per test session
@pytest.fixture(scope="module", autouse=True)
def prepare_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

# async client against your FastAPI app in-memory
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
