from datetime import datetime

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import MetaData, func
from sqlmodel import Field, SQLModel

# 保持原有的命名约定 (用于 Alembic / metadata.create_all)
database_naming_convention = {
    # 普通索引：idx_表名_列名（PG无原生自动命名，这是通用最佳实践）
    "ix": "idx_%(table_name)s_%(column_0_label)s",
    # 唯一约束：uk_表名_列名（匹配PG UNIQUE约束自动索引命名）
    "uq": "uk_%(table_name)s_%(column_0_name)s",
    # 检查约束：表名_约束名_check（PG默认无自动命名,手动保持风格一致）
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    # 外键约束：fk_表名_列名（匹配PG FOREIGN KEY自动索引命名）
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    # 主键约束：pk_表名_列名（匹配PG PRIMARY KEY自动索引命名）
    "pk": "pk_%(table_name)s_%(column_0_name)s",
}

# 将命名约定应用到 sqlmodel 的全局 metadata
SQLModel.metadata = MetaData(naming_convention=database_naming_convention)


class DateTimeMixin(SQLModel):
    """
    PostgreSQL 专用的 created_at / updated_at 实现 (使用数据库端 `now()`)
    使用 sa_type + sa_column_kwargs 避免多模型继承时 Column 对象被共享的问题。
    """

    created_at: datetime | None = Field(
        default=None,
        sa_type=pg.TIMESTAMP(timezone=True),  # type: ignore[arg-type]
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
        index=True,
        description="创建时间（数据库自动生成）",
    )

    updated_at: datetime | None = Field(
        default=None,
        sa_type=pg.TIMESTAMP(timezone=True),  # type: ignore[arg-type]
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
        nullable=False,
        description="更新时间（数据库自动生成/刷新）",
    )
