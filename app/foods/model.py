from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import Base, DateTimeMixin


class Food(Base, DateTimeMixin):
    __tablename__ = "food"
    __table_args__ = {"comment": "食物表"}

    id: Mapped[int | None] = mapped_column(
        Integer, default=None, primary_key=True, comment="编号"
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True, comment="名称"
    )
    brand: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True, comment="品牌"
    )
    kcals_per_g: Mapped[float | None] = mapped_column(
        Float, nullable=True, comment="卡路里/克"
    )
    price: Mapped[float | None] = mapped_column(Float, nullable=True, comment="价格")
    weight: Mapped[float | None] = mapped_column(Float, nullable=True, comment="重量")
    description: Mapped[str | None] = mapped_column(
        String(255), nullable=True, comment="描述"
    )
