from typing import Any, TypeVar

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

T = TypeVar("T", bound=SQLModel)


class RepoUtil:
    """通用 CRUD 工具类，提供基于 SQLModel 的静态方法"""

    @staticmethod
    async def create(session: AsyncSession, entity: T) -> T:
        """保存一个已实例化的 SQLModel 对象"""
        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return entity

    @staticmethod
    async def create_from_model(
        session: AsyncSession, model_cls: type[T], schema: SQLModel
    ) -> T:
        """从 Pydantic/SQLModel schema 创建数据库记录"""
        data = schema.model_dump(exclude_unset=True, exclude_none=True)
        entity = model_cls(**data)
        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return entity

    @staticmethod
    async def get_by_id(
        session: AsyncSession, model_cls: type[T], entity_id: int
    ) -> T | None:
        return await session.get(model_cls, entity_id)

    @staticmethod
    async def get_all(session: AsyncSession, model_cls: type[T]) -> list[T]:
        result = await session.exec(select(model_cls))
        return list(result.all())

    @staticmethod
    async def update(session: AsyncSession, entity: T, data: dict[str, Any]) -> T:
        """将 data 字典中的字段更新到 entity 上"""
        for key, value in data.items():
            setattr(entity, key, value)
        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return entity

    @staticmethod
    async def delete(session: AsyncSession, entity: T) -> bool:
        await session.delete(entity)
        await session.commit()
        return True
