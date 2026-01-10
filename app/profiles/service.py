from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import AlreadyExistsException, NotFoundException
from app.profiles.model import Profile
from app.profiles.repository import ProfileRepository
from app.profiles.schema import ProfileCreate, ProfileUpdate


class ProfileService:
    """Profile 服务层：封装业务逻辑并调用 repository"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repo = ProfileRepository(session)

    async def get_by_name(self, name: str) -> Profile | None:
        return await self._repo.get_by_name(name)

    async def get_by_id(self, id: int) -> Profile | None:
        return await self._repo.get_by_id(id)

    async def list_all(self, offset: int = 0, limit: int = 100) -> list[Profile]:
        return await self._repo.list_all(offset, limit)

    async def create(self, payload: ProfileCreate) -> Profile:
        existing = await self._repo.get_by_name(payload.name)
        if existing:
            raise AlreadyExistsException("Profile name exists")
        return await self._repo.create(payload)

    async def update(self, id: int, payload: ProfileUpdate) -> Profile:
        db_obj = await self._repo.get_by_id(id)
        if not db_obj:
            raise NotFoundException("Profile not found")
        return await self._repo.update(db_obj, payload)

    async def delete(self, id: int) -> bool:
        deleted = await self._repo.delete(id)
        if not deleted:
            raise NotFoundException("Profile not found")
        return True
