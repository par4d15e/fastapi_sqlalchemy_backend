from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.profiles.model import Profile
from app.profiles.schema import ProfileCreate, ProfileUpdate


class ProfileRepository:
    """Profile CRUD"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> Profile | None:
        """根据主键 `id` 获取单个 `Profile`"""
        return await self.session.get(Profile, id)

    async def get_by_name(self, name: str) -> Profile | None:
        """根据名称 `name` 查询 `Profile`"""
        statement = select(Profile).where(Profile.name == name)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_all(self, offset: int = 0, limit: int = 100) -> list[Profile]:
        """分页列出 `Profile` 列表"""
        statement = select(Profile).offset(offset).limit(limit)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create(self, obj_in: ProfileCreate) -> Profile:
        """创建新的 `Profile` 并返回保存后的实例 (包含自增 id)"""
        obj = Profile(**obj_in.model_dump())
        self.session.add(obj)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        await self.session.refresh(obj)
        return obj

    async def update(self, db_obj: Profile, obj_in: ProfileUpdate) -> Profile:
        """使用 `obj_in` 中的字段更新 `db_obj` 并保存更改"""
        obj_data = obj_in.model_dump(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: int) -> bool:
        """删除指定 `id` 的 `Profile`"""
        obj = await self.get_by_id(id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
