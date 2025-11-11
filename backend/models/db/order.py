"""Order ORM 모델"""
from sqlalchemy import Integer, String, ForeignKey, Text, TIMESTAMP, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from backend.db.base import Base
from datetime import datetime


class OrderDB(Base):
    """주문 테이블"""
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # 구매자 정보 (암호화 저장)
    customer_name: Mapped[str] = mapped_column(Text, nullable=False)
    customer_email: Mapped[str] = mapped_column(Text, nullable=False)
    customer_phone: Mapped[str] = mapped_column(Text, nullable=False)
    shipping_address: Mapped[str] = mapped_column(Text, nullable=False)

    # 주문 정보
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[int] = mapped_column(Integer, nullable=False)
    shipping_fee: Mapped[int] = mapped_column(Integer, nullable=False, default=10000)
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)

    # 어필리에이트
    affiliate_code: Mapped[str | None] = mapped_column(String, nullable=True)

    # PayPal 정보
    paypal_order_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    paypal_transaction_id: Mapped[str | None] = mapped_column(String, nullable=True)

    # 주문 상태
    order_status: Mapped[str] = mapped_column(String, nullable=False, default="PAYMENT_PENDING")

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    shipment: Mapped["ShipmentDB"] = relationship("ShipmentDB", back_populates="order", uselist=False)

    __table_args__ = (
        CheckConstraint("total_amount = (unit_price * quantity) + shipping_fee", name="check_total_amount"),
    )
