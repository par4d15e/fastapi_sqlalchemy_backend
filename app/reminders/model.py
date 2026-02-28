from datetime import datetime
from typing import TYPE_CHECKING, Annotated

from sqlmodel import Field, Index, Relationship, SQLModel, desc

from app.core.base_model import DateTimeMixin

if TYPE_CHECKING:
    from app.profiles.model import Profile


class Reminder(SQLModel, table=True, mixins=[DateTimeMixin]):
    __tablename__ = "reminders"  # type: ignore[assignment]

    __table_args__ = (
        # 单列索引
        Index("idx_reminders_profile_id", "profile_id"),
        Index("idx_reminders_type", "type"),
        Index("idx_reminders_due_date", "due_date"),
        Index("idx_reminders_is_done", "is_done"),
        # 复合索引 - 用于高效查询
        Index(
            "idx_reminders_profile_is_done", "profile_id", "is_done"
        ),  # 查询宠物未完成提醒
        Index(
            "idx_reminders_profile_due_date", "profile_id", "due_date"
        ),  # 查询宠物即将到期提醒
        Index("idx_reminders_profile_type", "profile_id", "type"),  # 按宠物+类型筛选
        Index(
            "idx_reminders_profile_due_is_done", "profile_id", "due_date", "is_done"
        ),  # 核心查询：宠物未完成且未过期
        # 排序索引
        Index("idx_reminders_due_date_asc", "due_date"),  # 按到期时间正序
        Index("idx_reminders_created_at_desc", desc("created_at")),
    )

    id: Annotated[
        int | None,
        Field(default=None, primary_key=True, index=True, description="提醒事项ID"),
    ]
    title: Annotated[str, Field(..., max_length=100, description="提醒事项标题")]
    type: Annotated[str, Field(..., max_length=50, description="提醒事项类型")]
    due_date: Annotated[datetime, Field(..., description="到期时间")]
    is_done: Annotated[
        bool, Field(default=False, nullable=False, description="是否完成")
    ]
    description: Annotated[
        str | None, Field(default=None, max_length=500, description="提醒事项描述")
    ]
    profile_id: Annotated[
        int,
        Field(
            foreign_key="profiles.id", nullable=False, index=True, description="宠物ID"
        ),
    ]

    profile: Annotated["Profile", Relationship(back_populates="reminders")]

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return f"<Reminder(id={self.id}, title={self.title}, type={self.type}, due_date={self.due_date}, is_done={self.is_done})>"
