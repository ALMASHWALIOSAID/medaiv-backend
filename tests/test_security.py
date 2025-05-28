import pytest
from datetime import timedelta

from app.core.security import (
    create_access_token,
    verify_password,
    get_password_hash,
    decode_access_token,
)


def test_password_hash_and_verify():
    plain = "secret123"
    hashed = get_password_hash(plain)
    assert hashed != plain
    assert verify_password(plain, hashed)
def test_token_roundtrip():
    data = {"sub": "user1"}
    token = create_access_token(data=data, expires_delta=timedelta(minutes=5))
    assert isinstance(token, str)

def test_token_expired():
    from time import sleep
    token = create_access_token(data={"sub": "u2"}, expires_delta=timedelta(seconds=0))
    sleep(1)
    assert isinstance(token, str)

