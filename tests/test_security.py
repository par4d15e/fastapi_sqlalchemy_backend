import os
import sys
import time
from datetime import timedelta

# Ensure project root is on sys.path for direct invocation
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.core import security


def test_password_hash_and_verify():
    pw = "s3cr3t-pw"
    h = security.hash_password(pw)
    assert isinstance(h, str) and len(h) > 0
    assert security.verify_password(pw, h) is True
    assert security.verify_password("wrong", h) is False


def test_token_create_and_decode():
    payload = {"sub": "user1"}
    token = security.create_access_token(payload)
    assert isinstance(token, str)
    decoded = security.decode_access_token(token)
    assert decoded["sub"] == "user1"


def test_token_expiration():
    payload = {"sub": "user2"}
    token = security.create_access_token(payload, expires_delta=timedelta(seconds=1))
    # should be valid immediately
    _ = security.decode_access_token(token)
    time.sleep(1.1)
    try:
        security.decode_access_token(token)
        assert False, "expected TokenError for expired token"
    except security.TokenError:
        pass
