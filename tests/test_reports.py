import pytest
from io import BytesIO
import base64

# 1×1 PNG
PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJ"
    "RU5ErkJggg=="
)

@pytest.mark.asyncio
async def test_upload_report_flow(client):
    # Sign up
    await client.post("/api/auth/signup", json={"username": "bob", "password": "pass123"})
    # Log in
    resp = await client.post(
        "/api/auth/token",
        data={"username": "bob", "password": "pass123"}
    )
    token = resp.json()["access_token"]

    # Upload
    img_bytes = base64.b64decode(PNG_BASE64)
    files = {"file": ("test.png", img_bytes, "image/png")}
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.post("/api/reports/upload", headers=headers, files=files)
    assert resp.status_code == 200
    data = resp.json()
    assert data["filename"] == "test.png"
    assert data["content_type"] == "image/png"
    assert data["owner_id"] == 1

    # Health
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
