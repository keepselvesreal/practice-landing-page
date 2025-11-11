"""Admin API 라우터 (최소 구현 - Walking Skeleton)"""
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import Session
from backend.db.base import get_db
from backend.models.db import OrderDB, ShipmentDB
from backend.utils.encryption import decrypt
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="backend/templates")


@router.get("/shipments")
def list_shipments(request: Request, db: Session = Depends(get_db)):
    """주문 목록 조회 (최소 구현)"""
    # PAID 상태 주문만 조회
    orders = db.query(OrderDB).filter(OrderDB.order_status == "PAID").all()

    # 복호화 (최소 구현 - 에러 처리 없음)
    for order in orders:
        order.customer_name = decrypt(order.customer_name)
        order.customer_email = decrypt(order.customer_email)

    return templates.TemplateResponse("admin/shipments.html", {
        "request": request,
        "orders": orders
    })


@router.post("/shipments/{order_id}")
def update_shipment(
    order_id: int,
    status: str = Form(...),
    tracking_number: str = Form(...),
    courier: str = Form(...),
    db: Session = Depends(get_db)
):
    """배송 상태 업데이트 (최소 구현 - 검증 없음)"""
    # Shipment 조회 또는 생성
    shipment = db.query(ShipmentDB).filter(ShipmentDB.order_id == order_id).first()
    if not shipment:
        shipment = ShipmentDB(order_id=order_id)
        db.add(shipment)

    # 상태 업데이트 (검증 없음)
    shipment.shipping_status = status
    shipment.tracking_number = tracking_number
    shipment.courier = courier

    # SHIPPED 상태면 shipped_at 기록
    if status == "SHIPPED":
        shipment.shipped_at = datetime.now()

        # 이메일 발송 (하드코딩)
        order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
        customer_email = decrypt(order.customer_email)
        print(f"[EMAIL] To: {customer_email}, Subject: 상품이 발송되었습니다, Tracking: {tracking_number}")

    db.commit()

    return RedirectResponse(url="/admin/shipments?success=저장되었습니다", status_code=303)
