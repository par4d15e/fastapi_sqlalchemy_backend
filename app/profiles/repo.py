from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.profiles.model import Profile
from app.profiles.schema import ProfileCreate, ProfileUpdate


class ProfileRepository:
    """Profile CRUD operations (async) - SQLAlchemy"""

    @staticmethod
    async def get_by_id(db: AsyncSession, id: int) -> Profile | None:
        """根据主键 `id` 获取单个 `Profile`"""
        return await db.get(Profile, id)

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> Profile | None:
        """根据名称 `name` 查询 `Profile`"""
        statement = select(Profile).where(Profile.name == name)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    async def list_all(
        db: AsyncSession, offset: int = 0, limit: int = 100
    ) -> list[Profile]:
        """分页列出 `Profile` 列表"""
        statement = select(Profile).offset(offset).limit(limit)
        result = await db.execute(statement)
        return list(result.scalars().all())

    @staticmethod
    async def create(db: AsyncSession, obj_in: ProfileCreate) -> Profile:
        """创建新的 `Profile` 并返回保存后的实例（包含自增 id）"""
        obj = Profile(**obj_in.model_dump())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    @staticmethod
    async def update(
        db: AsyncSession, db_obj: Profile, obj_in: ProfileUpdate
    ) -> Profile:
        """使用 `obj_in` 中的字段更新 `db_obj` 并保存更改"""
        obj_data = obj_in.model_dump(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, id: int) -> bool:
        """删除指定 `id` 的 `Profile`"""
        obj = await ProfileRepository.get_by_id(db, id)
        if not obj:
            return False
        await db.delete(obj)
        await db.commit()
        return True


# Create global instance
profile_repository = ProfileRepository()
