from sqlmodel import Field, SQLModel


class FoodBase(SQLModel):
    name: str
    me_per_1g: float


class Food(FoodBase, table=True):
    __tablename__ = "foods"  # type: ignore[assignment]
    __table_args__ = {
        "comment": "食物表",
    }

    id: int | None = Field(
        default=None, primary_key=True
    )  # pydantic 2.12 暂时不支持 Annotated 类型注解


