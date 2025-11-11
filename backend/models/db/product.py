"""Product ORM 모델"""
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base


class ProductDB(Base):
    """상품 테이블"""
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # 센타보 단위
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
