"""상품 관련 Pydantic 모델"""
from pydantic import BaseModel, Field


class Product(BaseModel):
    """상품 모델"""

    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1)
    price: int = Field(..., gt=0)  # 센타보 단위
    stock: int = Field(..., ge=0)  # 재고 수량 (0 이상)
    description: str | None = None
