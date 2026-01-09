from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import Base, DateTimeMixin


class Profile(Base, DateTimeMixin):
    __tablename__ = "profiles"
    __table_args__ = {"comment": "档案表"}

    id: Mapped[int | None] = mapped_column(Integer, primary_key=True, comment="编号")
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, comment="姓名"
    )
    gender: Mapped[str] = mapped_column(String(20), nullable=False, comment="性别")
    variety: Mapped[str] = mapped_column(String(100), nullable=False, comment="品种")
    birthday: Mapped[date | None] = mapped_column(Date, nullable=True, comment="生日")
