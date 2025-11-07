"""주문 관련 API 라우터"""
import secrets
from fastapi import APIRouter, HTTPException, status

from backend.models.order import OrderCreate, OrderCreateResponse, OrderResponse

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


@router.post("", response_model=OrderCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate) -> OrderCreateResponse:
    """주문 생성 및 PayPal 결제 URL 반환

    Args:
        order_data: 주문 정보

    Returns:
        OrderCreateResponse: 주문 번호, PayPal 정보

    TODO:
        - DB에 주문 저장
        - 실제 PayPal Order 생성
        - 재고 확인
    """
    # 주문 번호 생성 (ORD-XXXXXXXX)
    order_number = f"ORD-{secrets.token_hex(4).upper()}"

    # 총액 계산
    # TODO: DB에서 상품 가격 조회
    PRODUCT_PRICE = 57500  # 575 페소 (센타보)
    SHIPPING_FEE = 10000  # 100 페소 (센타보)
    total_amount = (PRODUCT_PRICE * order_data.quantity) + SHIPPING_FEE

    # TODO: PayPal Order 생성 (실제 PayPal SDK 호출)
    # 지금은 Mock 데이터 반환
    paypal_order_id = f"PAYPAL-{secrets.token_hex(8).upper()}"
    approval_url = f"https://www.sandbox.paypal.com/checkoutnow?token={paypal_order_id}"

    return OrderCreateResponse(
        order_number=order_number,
        paypal_order_id=paypal_order_id,
        approval_url=approval_url,
        total_amount=total_amount,
    )


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
