"""주문 관련 API 라우터"""
import secrets

from fastapi import APIRouter, HTTPException, status

from backend.models.order import OrderCreate, OrderCreateResponse, OrderResponse
from backend.models.product import Product
from backend.services.payment import PayPalAdapter
from backend.services.payment.payment_service import PaymentServiceError

router = APIRouter(prefix="/api/orders", tags=["orders"])

# PayPal Adapter 인스턴스
paypal_adapter = PayPalAdapter()

# Mock 상품 데이터 (재고 관리)
MOCK_PRODUCTS = {
    1: Product(
        id=1,
        name="조선미녀 맑은쌀 선크림 50ml",
        price=57500,  # 575 페소 (센타보)
        stock=10,  # ⭐ 초기 재고 10개
        description="Korean rice sunscreen"
    )
}

# 배송비 (센타보)
SHIPPING_FEE = 10000  # 100 페소

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


@router.post(
    "", response_model=OrderCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_order(order_data: OrderCreate) -> OrderCreateResponse:
    """주문 생성 및 PayPal 결제 URL 반환

    Args:
        order_data: 주문 정보

    Returns:
        OrderCreateResponse: 주문 번호, PayPal 정보

    Raises:
        HTTPException: 상품 없음(404), 재고 부족(409), PayPal 오류(503)
    """
    # 주문 번호 생성 (ORD-XXXXXXXX)
    order_number = f"ORD-{secrets.token_hex(4).upper()}"

    # ⭐ 상품 조회
    product = MOCK_PRODUCTS.get(order_data.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {order_data.product_id} not found"
        )

    # ⭐ 재고 확인
    if product.stock < order_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Insufficient stock. Available: {product.stock}, "
                f"Requested: {order_data.quantity}"
            ),
        )

    # 총액 계산
    total_amount = (product.price * order_data.quantity) + SHIPPING_FEE

    # PayPal Order 생성 (실제 PayPal SDK)
    try:
        paypal_result = paypal_adapter.create_order(amount=total_amount, currency="PHP")
    except PaymentServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Payment service error: {str(e)}"
        )

    # 🟢 재고 차감 (주문 생성 시 즉시 차감)
    product.stock -= order_data.quantity

    return OrderCreateResponse(
        order_number=order_number,
        paypal_order_id=paypal_result.order_id,
        approval_url=paypal_result.approval_url,
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
