"""PayPal Webhook 처리"""
import json
import logging
import os
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request, status, Depends
from paypalrestsdk import WebhookEvent
from sqlalchemy.orm import Session

from backend.models.db import OrderDB, ProductDB
from backend.services.email import send_order_confirmation_email
from backend.db.base import get_db
from backend.utils.encryption import decrypt

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = logging.getLogger(__name__)

# 처리된 Webhook 이벤트 추적 (중복 방지)
PROCESSED_WEBHOOK_EVENTS: set[str] = set()


@router.post("/paypal")
async def handle_paypal_webhook(request: Request, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """PayPal Webhook 이벤트 처리

    Args:
        request: FastAPI Request 객체
        db: DB 세션

    Returns:
        처리 결과

    Raises:
        HTTPException: 주문 없음(404), 서명 검증 실패(401)
    """
    # 1. 헤더 추출
    headers = dict(request.headers)

    # 2. Request body 읽기 (서명 검증에 필요)
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")

    # 3. 서명 검증
    try:
        webhook_id = os.getenv("PAYPAL_WEBHOOK_ID")

        is_valid = WebhookEvent.verify(
            transmission_id=headers.get("paypal-transmission-id"),
            timestamp=headers.get("paypal-transmission-time"),
            webhook_id=webhook_id,
            event_body=body_str,
            cert_url=headers.get("paypal-cert-url"),
            actual_sig=headers.get("paypal-transmission-sig"),
            auth_algo=headers.get("paypal-auth-algo"),
        )

        if not is_valid:
            logger.warning("Webhook 서명 검증 실패")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid webhook signature"
            )

    except HTTPException:
        # 위에서 발생시킨 401 예외는 그대로 전달
        raise
    except Exception as e:
        # 서명 검증 중 예외 발생 (네트워크 오류, 인증서 문제 등)
        logger.error(f"Webhook 서명 검증 오류: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature verification failed"
        )

    # 4. 검증 통과 후 JSON 파싱
    webhook_body = json.loads(body_str)

    event_type = webhook_body.get("event_type")
    resource = webhook_body.get("resource", {})

    # 이벤트 ID (중복 방지용)
    event_id = resource.get("id", "")
    # PayPal Order ID로 주문 찾기 (custom_id가 설정되지 않았으므로)
    # CHECKOUT.ORDER.APPROVED 이벤트의 경우 resource.id가 order_id
    # PAYMENT.CAPTURE.COMPLETED의 경우 resource.supplementary_data.related_ids.order_id 사용
    paypal_order_id = resource.get("id", "")
    if "supplementary_data" in resource:
        related_ids = resource.get("supplementary_data", {}).get("related_ids", {})
        paypal_order_id = related_ids.get("order_id", paypal_order_id)

    logger.info(f"Webhook 수신: event_type={event_type}, paypal_order_id={paypal_order_id}")

    # 중복 이벤트 체크
    if event_id in PROCESSED_WEBHOOK_EVENTS:
        logger.info(f"중복 이벤트 무시: event_id={event_id}")
        return {"status": "success", "message": "Duplicate event ignored"}

    # DB에서 주문 조회
    order = db.query(OrderDB).filter(OrderDB.paypal_order_id == paypal_order_id).first()
    if not order:
        logger.error(f"주문 없음: paypal_order_id={paypal_order_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with PayPal ID {paypal_order_id} not found"
        )

    # 이벤트 타입별 처리
    if event_type == "PAYMENT.CAPTURE.COMPLETED":
        # 결제 완료 처리
        return _handle_payment_completed(db, order, event_id)

    elif event_type == "PAYMENT.CAPTURE.DENIED":
        # 결제 실패 처리
        return _handle_payment_denied(db, order, event_id)

    else:
        # 처리하지 않는 이벤트 타입
        logger.warning(f"처리하지 않는 이벤트 타입: {event_type}")
        return {"status": "ignored", "message": f"Event type {event_type} not handled"}


def _handle_payment_completed(db: Session, order: OrderDB, event_id: str) -> Dict[str, Any]:
    """결제 완료 처리

    Args:
        db: DB 세션
        order: OrderDB
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
    db.commit()
    logger.info(f"주문 상태 PAID로 변경: order_number={order.order_number}")

    # 이메일 발송을 위해 고객 정보 복호화
    decrypted_email = decrypt(order.customer_email)
    decrypted_name = decrypt(order.customer_name)
    decrypted_phone = decrypt(order.customer_phone)
    decrypted_address = decrypt(order.shipping_address)

    # 이메일 발송 (OrderResponse 형태로 변환)
    from backend.models.order import OrderResponse
    order_response = OrderResponse(
        order_number=order.order_number,
        customer_name=decrypted_name,
        customer_email=decrypted_email,
        customer_phone=decrypted_phone,
        shipping_address=decrypted_address,
        product_id=order.product_id,
        quantity=order.quantity,
        unit_price=order.unit_price,
        shipping_fee=order.shipping_fee,
        total_amount=order.total_amount,
        order_status=order.order_status,
        affiliate_code=order.affiliate_code,
    )

    try:
        email_sent = send_order_confirmation_email(order_response)
        if email_sent:
            logger.info(f"이메일 발송 성공: {decrypted_email}")
        else:
            logger.warning(f"이메일 발송 실패: {decrypted_email}")
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


def _handle_payment_denied(db: Session, order: OrderDB, event_id: str) -> Dict[str, Any]:
    """결제 실패 처리 - 재고 복원

    Args:
        db: DB 세션
        order: OrderDB
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
    product = db.query(ProductDB).filter(ProductDB.id == order.product_id).first()
    if product:
        product.stock += order.quantity
        logger.info(
            f"재고 복원: product_id={order.product_id}, "
            f"quantity={order.quantity}, new_stock={product.stock}"
        )
    else:
        logger.error(f"상품 없음: product_id={order.product_id}")

    db.commit()

    # 처리 완료 기록
    PROCESSED_WEBHOOK_EVENTS.add(event_id)

    return {
        "status": "success",
        "message": "Payment denied, stock restored",
        "order_number": order.order_number,
        "order_status": order.order_status,
    }
