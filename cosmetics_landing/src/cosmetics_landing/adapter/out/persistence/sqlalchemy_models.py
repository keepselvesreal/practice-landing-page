"""
SQLAlchemy ORM Models
Chapter 6: "Implementing a Persistence Adapter" - Database Schema

목적:
- Order 도메인 엔티티를 데이터베이스 테이블로 매핑
- SQLAlchemy ORM 모델 정의
"""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OrderModel(Base):
    """
    주문 테이블 ORM 모델

    Chapter 6: 영속성 어댑터는 도메인 모델과 독립적인 DB 모델 사용
    - 도메인: Order (Value Object 포함)
    - DB: OrderModel (Flat Structure)
    """
    __tablename__ = "orders"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Customer Information
    customer_email = Column(String(255), nullable=False)
    customer_address = Column(String(500), nullable=False)

    # Product Information
    product_price_amount = Column(Numeric(10, 2), nullable=False)
    product_price_currency = Column(String(3), default="USD", nullable=False)

    # Affiliate Information
    affiliate_code = Column(String(50), nullable=True)

    # Order Status
    payment_status = Column(String(20), default="pending", nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<OrderModel(id={self.id}, customer_email='{self.customer_email}', payment_status='{self.payment_status}')>"
