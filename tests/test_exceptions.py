import pytest


@pytest.mark.anyio
async def test_404_for_missing(client):
    r = await client.get("/profile/nonexistent")
    assert r.status_code == 404
    body = r.json()
    assert "detail" in body
