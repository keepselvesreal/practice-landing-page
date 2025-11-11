"""주문 관련 Pydantic 모델"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class OrderCreate(BaseModel):
    """주문 생성 요청 모델"""

    customer_name: str = Field(..., min_length=1)
    customer_email: EmailStr
    customer_phone: str = Field(..., min_length=1)
    shipping_address: str = Field(..., min_length=1)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    affiliate_code: str | None = None


class OrderCreateResponse(BaseModel):
    """주문 생성 응답 모델"""

    order_number: str
    paypal_order_id: str
    approval_url: str
    total_amount: int  # 센타보 단위


class ShipmentResponse(BaseModel):
    """배송 정보 응답 모델"""

    shipping_status: str
    tracking_number: str | None = None
    courier: str | None = None
    shipped_at: datetime | None = None
    delivered_at: datetime | None = None


class OrderResponse(BaseModel):
    """주문 조회 응답 모델"""

    order_number: str
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    product_id: int
    quantity: int
    unit_price: int  # 센타보 단위
    shipping_fee: int  # 센타보 단위
    total_amount: int  # 센타보 단위
    order_status: str
    affiliate_code: str | None = None
    shipment: ShipmentResponse | None = None  # 배송 정보 (없을 수 있음)
