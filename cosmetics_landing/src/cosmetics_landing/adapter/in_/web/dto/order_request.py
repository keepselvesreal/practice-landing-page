"""
Order Web DTO
Chapter 5: 웹 어댑터 전용 입력 모델
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from decimal import Decimal


class OrderRequest(BaseModel):
    """
    주문 생성 요청 DTO - Pydantic으로 HTTP 검증

    Chapter 5: 웹 계층 전용 모델 (Use Case Command와 분리)
    """
    customer_email: EmailStr
    customer_address: str = Field(..., min_length=5)
    product_price: Decimal = Field(..., gt=0, decimal_places=2)
    affiliate_code: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "customer_email": "customer@example.com",
                    "customer_address": "123 Main St, Manila, Philippines",
                    "product_price": 29.99,
                    "affiliate_code": "INFLUENCER123"
                }
            ]
        }
    }


class OrderResponse(BaseModel):
    """주문 생성 응답 DTO"""
    order_id: int
    status: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": 1,
                    "status": "success",
                    "message": "Order placed successfully"
                }
            ]
        }
    }
