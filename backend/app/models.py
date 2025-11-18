from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):
    """Order model for storing customer order information."""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    place_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    email_logs = relationship("EmailLog", back_populates="order")


class EmailLog(Base):
    """Email log model for tracking email delivery status."""

    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    recipient = Column(String(100), nullable=False)
    subject = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False)  # 'sent', 'failed'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    order = relationship("Order", back_populates="email_logs")
