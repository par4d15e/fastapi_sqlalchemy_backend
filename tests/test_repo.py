import pytest

from app.profiles import repo
from app.profiles.schema import ProfileCreate


@pytest.mark.anyio
async def test_create_and_get(session_factory):
    async with session_factory() as session:
        p_in = ProfileCreate(name="alice", gender="female", variety="v1", birthday=None)
        created = await repo.create(session, p_in)
        assert created.id is not None
        got = await repo.get_by_name(session, "alice")
        assert got and got.id == created.id
