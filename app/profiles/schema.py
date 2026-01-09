from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class ProfileBase(BaseModel):
    name: Annotated[str, Field(..., max_length=100, description="姓名")]
    gender: Annotated[str, Field(..., max_length=20, description="性别")]
    variety: Annotated[str, Field(..., max_length=100, description="品种")]
    birthday: date | None = None


class ProfileCreate(ProfileBase):
    """用于创建宠物档案"""

    pass


class ProfileRead(ProfileBase):
    """用于读取宠物档案"""

    id: int
    model_config = ConfigDict(from_attributes=True)


class ProfileUpdate(ProfileBase):
    """用于更新宠物档案"""

    name: Annotated[str | None, Field(None, max_length=100, description="姓名")]
    gender: Annotated[str | None, Field(None, max_length=20, description="性别")]
    variety: Annotated[str | None, Field(None, max_length=100, description="品种")]
    birthday: date | None = None
