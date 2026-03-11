from typing import Annotated

from sqlmodel import Field, SQLModel


class NutritionFoodItem(SQLModel):
    """单个候选食品"""

    food_id: Annotated[int, Field(..., description="食品ID")]
    ratio: Annotated[float, Field(1.0, gt=0, description="配比权重")] = 1.0
    fixed_grams: Annotated[
        float | None,
        Field(None, ge=0, description="固定克数（可选，优先满足）"),
    ] = None
    kcals_per_g_override: Annotated[
        float | None,
        Field(None, gt=0, description="覆盖的卡路里密度(kcal/g)"),
    ] = None
    protein_g_per_g: Annotated[
        float | None,
        Field(None, ge=0, description="蛋白质密度(g/g)"),
    ] = None
    fat_g_per_g: Annotated[
        float | None,
        Field(None, ge=0, description="脂肪密度(g/g)"),
    ] = None
    carb_g_per_g: Annotated[
        float | None,
        Field(None, ge=0, description="碳水密度(g/g)"),
    ] = None


class NutritionGoal(SQLModel):
    """目标约束"""

    daily_kcals: Annotated[
        float | None,
        Field(None, gt=0, description="每日目标热量(kcal)，为空时自动估算"),
    ] = None
    protein_g: Annotated[float | None, Field(None, ge=0, description="蛋白目标(g)")] = (
        None
    )
    fat_g: Annotated[float | None, Field(None, ge=0, description="脂肪目标(g)")] = None
    carb_g: Annotated[float | None, Field(None, ge=0, description="碳水目标(g)")] = None


class NutritionPlanCreate(SQLModel):
    """营养计划计算请求"""

    profile_id: Annotated[int, Field(..., description="宠物ID")]
    foods: Annotated[
        list[NutritionFoodItem], Field(..., min_length=1, description="候选食品")
    ]
    goal: NutritionGoal
    weight_g_override: Annotated[
        int | None,
        Field(None, gt=0, description="覆盖体重(克)"),
    ] = None
    age_months_override: Annotated[
        int | None, Field(None, ge=0, description="覆盖月龄（优先使用）")
    ] = None
    neutered_override: Annotated[
        bool | None, Field(None, description="覆盖绝育状态（优先使用）")
    ] = None
    activity_level_override: Annotated[
        str | None,
        Field(None, description="覆盖活动水平: low/medium/high（优先使用）"),
    ] = None
    is_obese_override: Annotated[
        bool | None, Field(None, description="覆盖肥胖状态（优先使用）")
    ] = None
    is_pregnant: Annotated[bool, Field(False, description="是否妊娠（临时状态）")] = (
        False
    )
    is_lactating: Annotated[bool, Field(False, description="是否哺乳（临时状态）")] = (
        False
    )
    is_senior_override: Annotated[
        bool | None, Field(None, description="覆盖老年犬状态（优先使用）")
    ] = None
    activity_factor_override: Annotated[
        float | None,
        Field(None, ge=0.8, le=8.0, description="手动覆盖活动系数（最高优先级）"),
    ] = None


class NutritionFoodPlan(SQLModel):
    food_id: int
    food_name: str
    kcals_per_g: float
    grams: float
    kcals: float


class NutritionAchieved(SQLModel):
    protein_g: Annotated[float | None, Field(None, ge=0)] = None
    fat_g: Annotated[float | None, Field(None, ge=0)] = None
    carb_g: Annotated[float | None, Field(None, ge=0)] = None


class NutritionPlanResponse(SQLModel):
    profile_id: int
    weight_g: int
    daily_kcals_target: float
    total_grams: float
    total_kcals: float
    foods: list[NutritionFoodPlan]
    achieved: NutritionAchieved
    notes: list[str]
