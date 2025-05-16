# tests/test_api.py
import os
import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel import Session, select

from app.main import app
from app.core.config import engine
from app.models.user import User
from app.core.security import hash_password
from app.core.db import get_session

@pytest.fixture(autouse=True, scope="module")
def prepare_db():
    # Create fresh tables
    from sqlmodel import SQLModel
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    # Seed a test user
    with Session(engine) as session:
        user = User(username="testuser", hashed_password=hash_password("testpass"))
        session.add(user)
        session.commit()

    yield
    # Teardown if you like
    SQLModel.metadata.drop_all(engine)

@pytest.mark.asyncio
async def test_protected_upload(monkeypatch):
    # Monkey‐patch OCR/NLP in the router module to avoid heavy calls
    monkeypatch.setattr(
        "app.api.router.run_ocr", lambda b, ct: "hello"
    )
    monkeypatch.setattr(
        "app.api.router.extract_entities", lambda t, method=None: {"GREETING": ["hello"]}
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Get token
        r = await ac.post(
            "/api/token",
            data={"username": "testuser", "password": "testpass"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token = r.json()["access_token"]

        # Call upload with a supported content type
        files = {"file": ("dummy.pdf", b"dummy", "application/pdf")}
        headers = {"Authorization": f"Bearer {token}"}
        r = await ac.post("/api/reports/upload?nlp_method=spacy", headers=headers, files=files)
        assert r.status_code == 200
        body = r.json()
        assert body["text"] == "hello"
        assert body["entities"] == {"GREETING": ["hello"]}
