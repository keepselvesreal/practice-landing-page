"""주문 관련 API 라우터"""
from fastapi import APIRouter, HTTPException

from backend.models.order import OrderResponse

router = APIRouter(prefix="/api/orders", tags=["orders"])

# Mock 데이터 저장소 (필리핀 고객 가정)
MOCK_ORDERS = {
    "ORD-12345678": OrderResponse(
        order_number="ORD-12345678",
        customer_name="Maria Santos",
        customer_email="maria.santos@gmail.com",
        customer_phone="+63-917-123-4567",
        shipping_address="123 Rizal Avenue, Makati City, Metro Manila 1200",
        product_id=1,
        quantity=2,
        unit_price=15000,  # 150페소 (15000센타보)
        shipping_fee=10000,  # 100페소 (10000센타보)
        total_amount=40000,  # (150*2 + 100) = 400페소
        order_status="PAYMENT_PENDING",
        affiliate_code=None,
    )
}


@router.get("/{order_number}", response_model=OrderResponse)
async def get_order(order_number: str) -> OrderResponse:
    """주문 번호로 주문 조회

    Args:
        order_number: 주문 번호 (예: ORD-12345678)

    Returns:
        OrderResponse: 주문 정보

    Raises:
        HTTPException: 주문을 찾을 수 없는 경우 404
    """
    if order_number not in MOCK_ORDERS:
        raise HTTPException(
            status_code=404, detail=f"Order {order_number} not found"
        )

    return MOCK_ORDERS[order_number]
