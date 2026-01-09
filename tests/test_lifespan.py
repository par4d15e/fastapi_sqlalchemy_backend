import pytest

from app.core import config, lifespan


@pytest.mark.anyio
async def test_lifespan_calls(monkeypatch):
    called = {"create": False, "dispose": False}

    async def fake_create():
        called["create"] = True

    async def fake_dispose():
        called["dispose"] = True

    monkeypatch.setattr("app.core.lifespan.create_db_and_tables", fake_create)

    class FakeEngine:
        async def dispose(self):
            await fake_dispose()

    monkeypatch.setattr("app.core.lifespan.engine", FakeEngine())

    config.settings.debug = True
    async with lifespan.lifespan(None):
        assert called["create"]
    assert called["dispose"]
