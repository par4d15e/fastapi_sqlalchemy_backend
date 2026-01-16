from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class FoodBase(BaseModel):
    name: Annotated[str, Field(..., max_length=100, description="名称")]
    brand: Annotated[str, Field(..., max_length=100, description="品牌")]
    kcals_per_g: Annotated[float | None, Field(None, ge=0, description="卡路里/克")]
    price: Annotated[float | None, Field(None, ge=0, description="价格")]
    weight: Annotated[float | None, Field(None, ge=0, description="重量")]


class FoodCreate(FoodBase):
    pass


class FoodUpdate(BaseModel):
    name: Annotated[str | None, Field(None, max_length=100, description="名称")]
    brand: Annotated[str | None, Field(None, max_length=100, description="品牌")]
    kcals_per_g: Annotated[float | None, Field(None, ge=0, description="卡路里/克")]
    price: Annotated[float | None, Field(None, ge=0, description="价格")]
    weight: Annotated[float | None, Field(None, ge=0, description="重量")]


class FoodResponse(FoodBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
