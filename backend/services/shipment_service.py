"""배송 상태 업데이트 서비스"""
from sqlalchemy.orm import Session
from backend.models.db import ShipmentDB
from backend.models.db.shipment import InvalidTransitionError


def get_shipment_by_order_id(db_session: Session, order_id: int) -> ShipmentDB | None:
    """
    주문 ID로 Shipment 조회

    Args:
        db_session: DB 세션
        order_id: 주문 ID

    Returns:
        Shipment 객체 또는 None
    """
    return db_session.query(ShipmentDB).filter_by(order_id=order_id).first()


def update_shipment_status(
    db_session: Session,
    order_id: int,
    new_status: str,
    tracking_number: str | None = None,
    courier: str | None = None
) -> None:
    """
    배송 상태 업데이트 (도메인 로직 사용)

    Args:
        db_session: DB 세션
        order_id: 주문 ID
        new_status: 새 배송 상태
        tracking_number: 운송장 번호
        courier: 택배사

    Raises:
        InvalidTransitionError: 잘못된 상태 전환 시
        ValueError: 필수 필드 누락 시
    """
    # 1. Shipment 조회
    shipment = db_session.query(ShipmentDB).filter_by(order_id=order_id).first()

    if not shipment:
        # Shipment가 없으면 생성
        shipment = ShipmentDB(order_id=order_id)
        db_session.add(shipment)

    # 2. 도메인 로직을 통한 상태 업데이트 (검증 포함)
    shipment.update_status(
        new_status=new_status,
        tracking_number=tracking_number,
        courier=courier
    )

    # 3. DB 커밋
    db_session.commit()
    db_session.refresh(shipment)
