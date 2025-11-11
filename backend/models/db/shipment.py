"""Shipment ORM 모델"""
from sqlalchemy import Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from backend.db.base import Base
from datetime import datetime


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
