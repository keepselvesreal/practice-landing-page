"""주문 관련 Pydantic 모델"""
from pydantic import BaseModel


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
