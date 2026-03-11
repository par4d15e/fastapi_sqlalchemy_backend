import uuid
from enum import IntEnum
from typing import TYPE_CHECKING, Annotated

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Index, Relationship, SQLModel, desc, text

from app.core.base_model import DateTimeMixin

# 防止循环导入
if TYPE_CHECKING:
    from app.auth.model import Code, RefreshToken, Social_Account

# 定义用户角色的枚举类型


class RoleType(IntEnum):
    user = 1
    admin = 2


class User(SQLModel, table=True, mixins=[DateTimeMixin]):
    """用户表 - 存储系统用户的基本信息"""

    __tablename__ = "users"  # type: ignore[assignment]

    __table_args__ = (
        # 复合索引
        Index("idx_users_is_active_email", "is_active", "email"),  # 按是否激活+邮箱筛选
        Index(
            "idx_users_is_active_username", "is_active", "username"
        ),  # 按是否激活+用户名筛选
        Index(
            "idx_users_is_verified_email", "is_verified", "email"
        ),  # 按是否验证+邮箱筛选
        Index(
            "idx_users_is_verified_username", "is_verified", "username"
        ),  # 按是否验证+用户名筛选
        Index(
            "idx_users_is_deleted_email", "is_deleted", "email"
        ),  # 按是否删除+邮箱筛选
        Index(
            "idx_users_is_deleted_username", "is_deleted", "username"
        ),  # 按是否删除+用户名筛选
        # 排序索引
        Index("idx_users_created_at_desc", desc("created_at")),
        Index("idx_users_updated_at_desc", desc("updated_at")),
    )

    uid: Annotated[
        uuid.UUID | None,
        Field(
            default=None,
            sa_column=Column(
                pg.UUID(as_uuid=True),
                server_default=text("gen_random_uuid()"),
                primary_key=True,
            ),
        ),
    ] = None
    username: Annotated[
        str | None, Field(default=None, nullable=True, max_length=30, unique=True)
    ] = None  # 优化长度
    email: Annotated[
        str | None, Field(default=None, nullable=False, max_length=100, unique=True)
    ] = None  # 优化长度
    password_hash: Annotated[str | None, Field(default=None, max_length=255)] = None
    role: Annotated[RoleType, Field(default=RoleType.user, nullable=False)] = (
        RoleType.user
    )
    bio: Annotated[
        str | None, Field(default="这个人很懒，什么都没有留下。", max_length=300)
    ] = None  # 优化长度
    ip_address: Annotated[str | None, Field(default=None, max_length=45)] = None
    longitude: Annotated[float | None, Field(default=None)] = None
    latitude: Annotated[float | None, Field(default=None)] = None
    city: Annotated[str | None, Field(default=None, max_length=50)] = None  # 优化长度
    is_active: Annotated[bool, Field(default=False, nullable=False)] = False
    is_verified: Annotated[bool, Field(default=False, nullable=False)] = False
    is_deleted: Annotated[bool, Field(default=False, nullable=False)] = False

    # 关系字段定义
    # 1. 一对一关系：用户头像

    # 2. 一对多关系：用户创建的内容（可以级联删除）
    refresh_tokens: Annotated[
        list["RefreshToken"],
        Relationship(passive_deletes=True),
    ] = []

    codes: Annotated[
        list["Code"],
        Relationship(passive_deletes=True),
    ] = []

    social_accounts: Annotated[
        list["Social_Account"],
        Relationship(passive_deletes=True),
    ] = []

    # 3. 一对多关系：重要业务数据（不应级联删除，支持软删除）

    # 4. 重要业务关系：绝对不能级联删除

    def __repr__(self):
        return f"<User(id={self.uid}, username={self.username})>"
