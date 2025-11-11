"""Shipment ORM 모델"""
from sqlalchemy import Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from backend.db.base import Base
from datetime import datetime
from enum import Enum


class ShipmentStatus(str, Enum):
    """배송 상태 Enum"""
    PREPARING = "PREPARING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"


class InvalidTransitionError(Exception):
    """잘못된 상태 전환 예외"""
    pass


class ShipmentDB(Base):
    """배송 테이블"""
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)

    # 배송 정보
    shipping_status: Mapped[str] = mapped_column(String, nullable=False, default="PREPARING")
    tracking_number: Mapped[str | None] = mapped_column(String, nullable=True)
    courier: Mapped[str | None] = mapped_column(String, nullable=True)

    # 타임스탬프
    shipped_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    delivered_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    returned_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    order: Mapped["OrderDB"] = relationship("OrderDB", back_populates="shipment")

    # 상태 전환 규칙
    VALID_TRANSITIONS = {
        ShipmentStatus.PREPARING: [ShipmentStatus.SHIPPED],
        ShipmentStatus.SHIPPED: [ShipmentStatus.DELIVERED],
        ShipmentStatus.DELIVERED: []
    }

    def update_status(
        self,
        new_status: str,
        tracking_number: str | None = None,
        courier: str | None = None
    ) -> list:
        """
        배송 상태 업데이트 (도메인 로직)

        Args:
            new_status: 새 배송 상태
            tracking_number: 운송장 번호
            courier: 택배사

        Returns:
            list: 발생한 이벤트 목록

        Raises:
            InvalidTransitionError: 잘못된 상태 전환 시
            ValueError: 필수 필드 누락 시
        """
        new_status_enum = ShipmentStatus(new_status)
        current_status_enum = ShipmentStatus(self.shipping_status)

        # 1. 상태 전환 규칙 검증
        if new_status_enum not in self.VALID_TRANSITIONS[current_status_enum]:
            allowed = [s.value for s in self.VALID_TRANSITIONS[current_status_enum]]
            raise InvalidTransitionError(
                f"{self.shipping_status} → {new_status} 전환은 불가능합니다. "
                f"허용: {allowed}"
            )

        # 2. SHIPPED 필수 필드 검증
        if new_status_enum == ShipmentStatus.SHIPPED:
            if not tracking_number:
                raise ValueError("운송장 번호를 입력하세요")
            if not courier:
                raise ValueError("택배사를 선택하세요")

        # 3. 상태 업데이트
        self.shipping_status = new_status

        if tracking_number:
            self.tracking_number = tracking_number
        if courier:
            self.courier = courier

        # 3. 타임스탬프 기록
        events = []
        if new_status_enum == ShipmentStatus.SHIPPED:
            self.shipped_at = datetime.now()
            # 이벤트는 나중에 구현
        elif new_status_enum == ShipmentStatus.DELIVERED:
            self.delivered_at = datetime.now()
            # 이벤트는 나중에 구현

        return events
