import pytest

@pytest.mark.asyncio
async def test_signup_and_login(client):
    # signup
    resp = await client.post(
        "/api/auth/signup",
        json={"username": "alice", "password": "secret"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "alice"

    # login
    resp = await client.post(
        "/api/auth/token",
        data={"username": "alice", "password": "secret"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]

    # users/me
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.get("/api/auth/users/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["username"] == "alice"
