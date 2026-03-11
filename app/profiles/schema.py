from datetime import date
from typing import Annotated

from sqlmodel import Field, SQLModel


class ProfileCreate(SQLModel):
    """创建宠物档案"""

    name: Annotated[str, Field(..., max_length=100, description="姓名")]
    gender: Annotated[str, Field(..., max_length=20, description="性别")]
    variety: Annotated[str, Field(..., max_length=100, description="品种")]
    birthday: Annotated[date | None, Field(None, description="生日")] = None
    meals_per_day: Annotated[int, Field(2, ge=1, description="每日餐数")] = 2
    neutered: Annotated[bool, Field(False, description="是否绝育")] = False
    activity_level: Annotated[
        str, Field("medium", max_length=20, description="活动水平: low/medium/high")
    ] = "medium"
    is_obese: Annotated[bool, Field(False, description="是否肥胖")] = False


class ProfileUpdate(SQLModel):
    """更新宠物档案（部分可选）"""

    name: Annotated[str | None, Field(None, max_length=100, description="姓名")] = None
    gender: Annotated[str | None, Field(None, max_length=20, description="性别")] = None
    variety: Annotated[str | None, Field(None, max_length=100, description="品种")] = (
        None
    )
    birthday: Annotated[date | None, Field(None, description="生日")] = None
    meals_per_day: Annotated[int | None, Field(None, ge=1, description="每日餐数")] = (
        None
    )
    neutered: Annotated[bool | None, Field(None, description="是否绝育")] = None
    activity_level: Annotated[
        str | None, Field(None, max_length=20, description="活动水平: low/medium/high")
    ] = None
    is_obese: Annotated[bool | None, Field(None, description="是否肥胖")] = None


class ProfileResponse(SQLModel):
    """宠物档案响应"""

    name: Annotated[str, Field(..., max_length=100, description="姓名")]
    gender: Annotated[str, Field(..., max_length=20, description="性别")]
    variety: Annotated[str, Field(..., max_length=100, description="品种")]
    birthday: Annotated[date | None, Field(None, description="生日")] = None
    meals_per_day: Annotated[int, Field(2, ge=1, description="每日餐数")] = 2
    neutered: Annotated[bool, Field(False, description="是否绝育")] = False
    activity_level: Annotated[
        str, Field("medium", max_length=20, description="活动水平: low/medium/high")
    ] = "medium"
    is_obese: Annotated[bool, Field(False, description="是否肥胖")] = False
    id: int
