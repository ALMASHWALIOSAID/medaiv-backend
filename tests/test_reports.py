import pytest
import base64

PNG_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="

@pytest.mark.asyncio
async def test_upload_report_flow(client):
    # signup + login (reuse signup URL fix above)
    await client.post("/api/signup", json={"username": "bob", "password": "pass123"})
    resp = await client.post("/api/token", data={"username": "bob", "password": "pass123"})
    token = resp.json()["access_token"]

    # upload
    img_bytes = base64.b64decode(PNG_BASE64)
    files = {"file": ("test.png", img_bytes, "image/png")}
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.post("/api/reports/upload", headers=headers, files=files)
    assert resp.status_code == 200
    data = resp.json()
    assert data["filename"] == "test.png"
    assert data["content_type"] == "image/png"
    assert data["owner_id"] == 1

    # health
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
