from __future__ import annotations

from datetime import datetime
from enum import IntEnum
from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlmodel import (
    Field,
    Index,
    Relationship,
    SQLModel,
    desc,
)

# 防止循环导入
if TYPE_CHECKING:
    from app.auth.model import Code, RefreshToken, Social_Account

# 定义用户角色的枚举类型


class RoleType(IntEnum):
    user = 1
    admin = 2


class User(SQLModel, table=True):
    """用户表 - 存储系统用户的基本信息"""

    __tablename__ = "users"  # type: ignore[assignment]

    __table_args__ = (
        # 核心查询索引
        Index("idx_users_id", "id"),
        Index("idx_users_email", "email"),
        Index("idx_users_username", "username"),
        # 复合业务索引
        Index(
            "idx_users_get_user_by_email",
            "email",
            "is_active",
            "is_verified",
            "is_deleted",
        ),  # auth_crud.py: get_user_by_email
        Index(
            "idx_users_get_user_by_id", "id", "is_active", "is_verified", "is_deleted"
        ),  # auth_crud.py: get_user_by_id
        Index(
            "idx_users_get_user_by_username", "username", "is_active", "is_verified"
        ),  # auth_crud.py: get_user_by_username
        # 时间排序索引
        Index("idx_users_created_at_desc", desc("created_at")),
        Index("idx_users_updated_at_desc", desc("updated_at")),
    )

    id: int | None = Field(default=None, primary_key=True)
    username: str | None = Field(nullable=True, max_length=30, unique=True)  # 优化长度
    email: str = Field(nullable=False, max_length=100, unique=True)  # 优化长度
    password_hash: str | None = Field(max_length=255)
    role: RoleType = Field(nullable=False, default=RoleType.user)
    bio: str | None = Field(
        default="这个人很懒，什么都没有留下。", max_length=300
    )  # 优化长度
    ip_address: str | None = Field(default=None, max_length=45)
    longitude: float | None = Field(default=None)
    latitude: float | None = Field(default=None)
    city: str | None = Field(default=None, max_length=50)  # 优化长度
    is_active: bool = Field(default=False, nullable=False)
    is_verified: bool = Field(default=False, nullable=False)
    is_deleted: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(
        nullable=False,
        sa_type=TIMESTAMP,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
    )
    updated_at: datetime | None = Field(
        default=None,
        nullable=True,
        sa_type=TIMESTAMP,
        sa_column_kwargs={"onupdate": text("CURRENT_TIMESTAMP")},
    )

    # 关系字段定义
    # 1. 一对一关系：用户头像

    # 2. 一对多关系：用户创建的内容（可以级联删除）
    refresh_tokens: list["RefreshToken"] = Relationship(
        sa_relationship_kwargs={
            "uselist": True,
            "lazy": "select",
        }
    )

    codes: list["Code"] = Relationship(
        sa_relationship_kwargs={
            "uselist": True,
            "lazy": "select",
        }
    )

    social_accounts: list["Social_Account"] = Relationship(
        sa_relationship_kwargs={
            "uselist": True,
            "lazy": "select",
        }
    )

    # 3. 一对多关系：重要业务数据（不应级联删除，支持软删除）

    # 4. 重要业务关系：绝对不能级联删除

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, role={self.role.name}, is_active={self.is_active})>"
