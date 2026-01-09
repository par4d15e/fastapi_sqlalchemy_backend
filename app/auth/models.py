"""令牌与验证码模型定义 - SQLAlchemy 2.0 类型化映射"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import Base, DateTimeMixin

if TYPE_CHECKING:
    from app.users.model import User  # for type checkers only


class RefreshToken(Base, DateTimeMixin):
    """刷新令牌模型

    用于管理用户刷新令牌，支持：
    - 多设备登录（每个设备一个令牌）
    - 令牌撤销
    - 令牌过期管理
    """

    __tablename__ = "refresh_tokens"

    id: Mapped[int | None] = mapped_column(Integer, primary_key=True, index=True)

    # Associated user
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # 令牌信息
    token: Mapped[str] = mapped_column(
        String(500), unique=True, index=True, nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    # 设备信息（可选）
    device_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    device_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # web, mobile, desktop
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # 状态
    is_revoked: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, index=True
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # 最近使用时间
    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User", backref="refresh_tokens")

    def __repr__(self) -> str:
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, is_revoked={self.is_revoked})>"

    def is_valid(self) -> bool:
        """检查令牌是否有效"""
        if self.is_revoked:
            return False
        return datetime.now(timezone.utc) < self.expires_at

    def revoke(self) -> None:
        """撤销令牌"""
        self.is_revoked = True
        self.revoked_at = datetime.now(timezone.utc)


class VerificationCode(Base, DateTimeMixin):
    """验证码模型

    用于管理邮件验证码和密码重置码，支持：
    - 验证码过期管理
    - 验证码使用次数限制
    - 验证码类型区分
    """

    __tablename__ = "verification_codes"

    id: Mapped[int | None] = mapped_column(Integer, primary_key=True, index=True)

    # Associated user
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # 验证码信息
    code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    code_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    # 使用状态
    is_used: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, index=True
    )
    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=5, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", backref="verification_codes")

    def __repr__(self) -> str:
        return f"<VerificationCode(id={self.id}, user_id={self.user_id}, code_type={self.code_type})>"

    def is_valid(self) -> bool:
        """检查验证码是否有效"""
        if self.is_used:
            return False
        if self.attempts >= self.max_attempts:
            return False
        return datetime.now(timezone.utc) < self.expires_at

    def increment_attempts(self) -> None:
        """增加尝试次数"""
        self.attempts += 1

    def mark_as_used(self) -> None:
        """标记为已使用"""
        self.is_used = True
        self.used_at = datetime.now(timezone.utc)
