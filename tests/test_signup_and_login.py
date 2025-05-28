import pytest
import uuid

@pytest.mark.asyncio
async def test_signup_and_login(client):
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "secret"

    # signup
    resp = await client.post("/api/auth/signup", json={"username": username, "password": password})
    assert resp.status_code == 201, resp.text

    # login
    resp = await client.post("/api/auth/token", data={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    token = resp.json()["access_token"]

    # get current user
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.get("/api/auth/users/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["username"] == username
