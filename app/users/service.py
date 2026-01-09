from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import AlreadyExistsException, NotFoundException
from app.users.model import User
from app.users.repo import user_repository
from app.users.schema import UserCreate, UserUpdate


class UserService:
    """User 服务层：封装业务逻辑并调用 repository"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await user_repository.get_by_id(self._session, user_id)

    async def get_by_username(self, username: str) -> Optional[User]:
        return await user_repository.get_by_username(self._session, username)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await user_repository.get_by_email(self._session, email)

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await user_repository.get_all(self._session, skip, limit)

    async def create(self, payload: UserCreate) -> User:
        # 检查用户名或邮箱重复
        if await user_repository.get_by_username(self._session, payload.username):
            raise AlreadyExistsException("Username already exists")
        if await user_repository.get_by_email(self._session, payload.email):
            raise AlreadyExistsException("Email already exists")
        return await user_repository.create(self._session, payload)

    async def update(self, user_id: int, payload: UserUpdate) -> User:
        result = await user_repository.update(self._session, user_id, payload)
        if not result:
            raise NotFoundException("User not found")
        return result

    async def delete(self, user_id: int) -> bool:
        deleted = await user_repository.delete(self._session, user_id)
        if not deleted:
            raise NotFoundException("User not found")
        return True

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        return await user_repository.authenticate(self._session, username, password)

    async def verify_email(self, user_id: int) -> User:
        result = await user_repository.verify_email(self._session, user_id)
        if not result:
            raise NotFoundException("User not found")
        return result

    async def change_password(self, user_id: int, new_password: str) -> User:
        result = await user_repository.change_password(
            self._session, user_id, new_password
        )
        if not result:
            raise NotFoundException("User not found")
        return result
