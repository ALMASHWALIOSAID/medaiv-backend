import io
import pytest

@pytest.mark.asyncio
async def test_upload_report_flow(client):
    await client.post("/api/auth/signup", json={"username": "bob", "password": "pass123"})
    resp = await client.post("/api/auth/token", data={"username": "bob", "password": "pass123"})
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    fake_txt = io.BytesIO(b"Hello world")
    files = {"file": ("hello.txt", fake_txt, "text/plain")}
    resp = await client.post("/api/reports/", headers=headers, files=files)
    assert resp.status_code == 201, resp.text
    report = resp.json()
    assert report["filename"] == "hello.txt"
    assert "entities" in report
    rid = report["id"]

    # fetch list of reports
    resp = await client.get("/api/reports/", headers=headers)
    assert resp.status_code == 200, resp.text
    lst = resp.json()
    assert any(r["id"] == rid for r in lst)

    # fetch detail
    resp = await client.get(f"/api/reports/{rid}", headers=headers)
    assert resp.status_code == 200, resp.text
    detail = resp.json()
    assert detail["id"] == rid
    assert detail["text"].lower().startswith("hello")

@pytest.mark.asyncio
async def test_upload_unsupported_file_type(client):
    await client.post("/api/auth/signup", json={"username": "badfile", "password": "pass123"})
    resp = await client.post("/api/auth/token", data={"username": "badfile", "password": "pass123"})
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    fake_exe = io.BytesIO(b"MZ")
    files = {"file": ("program.exe", fake_exe, "application/x-msdownload")}
    resp = await client.post("/api/reports/", headers=headers, files=files)
    assert resp.status_code == 415
    assert resp.json()["detail"] == "Unsupported file type"

@pytest.mark.asyncio
async def test_get_missing_report(client):
    await client.post("/api/auth/signup", json={"username": "notfound", "password": "pass123"})
    resp = await client.post("/api/auth/token", data={"username": "notfound", "password": "pass123"})
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = await client.get("/api/reports/99999", headers=headers)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Report not found"
