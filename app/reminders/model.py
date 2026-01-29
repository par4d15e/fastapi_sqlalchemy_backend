from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import Base, DateTimeMixin
from app.profiles.model import Profile


class Reminder(Base, DateTimeMixin):
    __tablename__ = "reminders"
    __table_args__ = {"comment": "提醒事项"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="提醒事项ID")
    title: Mapped[str] = mapped_column(String(100), nullable=False, comment="提醒事项标题")
    type: Mapped[str] = mapped_column(String(50), nullable=False, comment="提醒事项类型")
    due_date: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="到期时间"
    )
    is_done: Mapped[bool] = mapped_column(
        Boolean(False), nullable=False, comment="是否完成"
    )
    description: Mapped[str] = mapped_column(
        String(500), nullable=True, comment="提醒事项描述"
    )
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profiles.id"), nullable=False, index=True, comment="宠物ID"
    )
    profile: Mapped["Profile"] = relationship("Profile", back_populates="reminders")
