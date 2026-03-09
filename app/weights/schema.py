from datetime import datetime, timezone
from typing import Annotated

from sqlmodel import Field, SQLModel


class WeightRecordCreate(SQLModel):
    """创建体重记录"""

    profile_id: Annotated[int, Field(..., description="宠物ID")]
    weight_g: Annotated[int, Field(..., gt=0, description="体重 (克)")]
    measured_at: Annotated[
        datetime | None,
        Field(default_factory=lambda: datetime.now(tz=timezone.utc), description="测量时间"),
    ] = None


class WeightRecordUpdate(SQLModel):
    """更新体重记录（部分可选）"""

    weight_g: Annotated[int | None, Field(None, gt=0, description="体重 (克)")] = None
    measured_at: Annotated[datetime | None, Field(None, description="测量时间")] = None


class WeightRecordResponse(SQLModel):
    """体重记录响应"""

    id: int
    profile_id: Annotated[int, Field(..., description="宠物ID")]
    weight_g: Annotated[int, Field(..., description="体重 (克)")]
    measured_at: Annotated[datetime, Field(..., description="测量时间")]
