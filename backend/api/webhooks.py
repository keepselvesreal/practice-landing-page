"""PayPal Webhook 처리"""
import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request, status

from backend.api.orders import MOCK_ORDERS, MOCK_PRODUCTS
from backend.services.email import send_order_confirmation_email

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = logging.getLogger(__name__)

# 처리된 Webhook 이벤트 추적 (중복 방지)
PROCESSED_WEBHOOK_EVENTS: set[str] = set()


@router.post("/paypal")
async def handle_paypal_webhook(request: Request) -> Dict[str, Any]:
    """PayPal Webhook 이벤트 처리

    Args:
        request: FastAPI Request 객체

    Returns:
        처리 결과

    Raises:
        HTTPException: 주문 없음(404), 처리 실패(500)
    """
    # Webhook 이벤트 수신
    webhook_body = await request.json()

    event_type = webhook_body.get("event_type")
    resource = webhook_body.get("resource", {})

    # 이벤트 ID (중복 방지용)
    event_id = resource.get("id", "")
    order_number = resource.get("custom_id", "")

    logger.info(f"Webhook 수신: event_type={event_type}, order_number={order_number}")

    # 중복 이벤트 체크
    if event_id in PROCESSED_WEBHOOK_EVENTS:
        logger.info(f"중복 이벤트 무시: event_id={event_id}")
        return {"status": "success", "message": "Duplicate event ignored"}

    # 주문 조회
    order = MOCK_ORDERS.get(order_number)
    if not order:
        logger.error(f"주문 없음: order_number={order_number}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_number} not found"
        )

    # 이벤트 타입별 처리
    if event_type == "PAYMENT.CAPTURE.COMPLETED":
        # 결제 완료 처리
        return _handle_payment_completed(order, event_id)

    elif event_type == "PAYMENT.CAPTURE.DENIED":
        # 결제 실패 처리
        return _handle_payment_denied(order, event_id)

    else:
        # 처리하지 않는 이벤트 타입
        logger.warning(f"처리하지 않는 이벤트 타입: {event_type}")
        return {"status": "ignored", "message": f"Event type {event_type} not handled"}


def _handle_payment_completed(order, event_id: str) -> Dict[str, Any]:
    """결제 완료 처리

    Args:
        order: OrderResponse
        event_id: Webhook 이벤트 ID

    Returns:
        처리 결과
    """
    # 이미 PAID 상태면 중복 처리 방지
    if order.order_status == "PAID":
        logger.info(f"이미 PAID 상태: order_number={order.order_number}")
        PROCESSED_WEBHOOK_EVENTS.add(event_id)
        return {"status": "success", "message": "Already paid"}

    # 주문 상태 업데이트
    order.order_status = "PAID"
    logger.info(f"주문 상태 PAID로 변경: order_number={order.order_number}")

    # 이메일 발송
    try:
        email_sent = send_order_confirmation_email(order)
        if email_sent:
            logger.info(f"이메일 발송 성공: {order.customer_email}")
        else:
            logger.warning(f"이메일 발송 실패: {order.customer_email}")
    except Exception as e:
        logger.error(f"이메일 발송 오류: {e}")
        # 이메일 실패해도 주문 처리는 성공으로 간주

    # 처리 완료 기록
    PROCESSED_WEBHOOK_EVENTS.add(event_id)

    return {
        "status": "success",
        "message": "Payment completed",
        "order_number": order.order_number,
        "order_status": order.order_status,
    }


def _handle_payment_denied(order, event_id: str) -> Dict[str, Any]:
    """결제 실패 처리 - 재고 복원

    Args:
        order: OrderResponse
        event_id: Webhook 이벤트 ID

    Returns:
        처리 결과
    """
    # 이미 FAILED 상태면 중복 처리 방지
    if order.order_status == "FAILED":
        logger.info(f"이미 FAILED 상태: order_number={order.order_number}")
        PROCESSED_WEBHOOK_EVENTS.add(event_id)
        return {"status": "success", "message": "Already failed"}

    # 주문 상태 업데이트
    order.order_status = "FAILED"
    logger.info(f"주문 상태 FAILED로 변경: order_number={order.order_number}")

    # 재고 복원
    product = MOCK_PRODUCTS.get(order.product_id)
    if product:
        product.stock += order.quantity
        logger.info(
            f"재고 복원: product_id={order.product_id}, "
            f"quantity={order.quantity}, new_stock={product.stock}"
        )
    else:
        logger.error(f"상품 없음: product_id={order.product_id}")

    # 처리 완료 기록
    PROCESSED_WEBHOOK_EVENTS.add(event_id)

    return {
        "status": "success",
        "message": "Payment denied, stock restored",
        "order_number": order.order_number,
        "order_status": order.order_status,
    }
