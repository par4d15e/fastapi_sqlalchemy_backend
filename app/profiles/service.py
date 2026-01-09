from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import AlreadyExistsException, NotFoundException
from app.profiles.model import Profile
from app.profiles.repo import profile_repository
from app.profiles.schema import ProfileCreate, ProfileUpdate


class ProfileService:
    """Profile 服务层：封装业务逻辑并调用 repository"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_name(self, name: str) -> Profile | None:
        return await profile_repository.get_by_name(self._session, name)

    async def get_by_id(self, id: int) -> Profile | None:
        return await profile_repository.get_by_id(self._session, id)

    async def list_all(self, offset: int = 0, limit: int = 100) -> list[Profile]:
        return await profile_repository.list_all(self._session, offset, limit)

    async def create(self, payload: ProfileCreate) -> Profile:
        existing = await profile_repository.get_by_name(self._session, payload.name)
        if existing:
            raise AlreadyExistsException("Profile name exists")
        return await profile_repository.create(self._session, payload)

    async def update(self, id: int, payload: ProfileUpdate) -> Profile:
        db_obj = await profile_repository.get_by_id(self._session, id)
        if not db_obj:
            raise NotFoundException("Profile not found")
        return await profile_repository.update(self._session, db_obj, payload)

    async def delete(self, id: int) -> bool:
        deleted = await profile_repository.delete(self._session, id)
        if not deleted:
            raise NotFoundException("Profile not found")
        return True
