"""usermodeldefinition"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import Base, DateTimeMixin


class User(Base, DateTimeMixin):
    """
    用户模型 - 完整的 JWT 认证

    包含完整的认证功能：
    - 邮箱验证
    - 密码重置
    - 支持多设备登录（通过 RefreshToken 表）
    """

    __tablename__ = "users"

    # 基础字段
    id: Mapped[int | None] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # 状态
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Email whether already validated",
    )

    # 最后登录时间
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
