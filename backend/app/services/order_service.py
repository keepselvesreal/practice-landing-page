from datetime import datetime
from sqlalchemy.orm import Session

from app.models import Order, EmailLog
from app.schemas import OrderCreate
from app.services.email_service import send_order_confirmation_email


def generate_order_number() -> str:
    """Generate unique order number based on timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"ORD-{timestamp}"


def create_order(db: Session, order_data: OrderCreate) -> tuple[Order, bool]:
    """
    Create a new order and send confirmation email.

    Args:
        db: Database session
        order_data: Order creation data

    Returns:
        Tuple of (Order object, email_sent boolean)
    """
    # Generate order number
    order_number = generate_order_number()

    # Create order
    db_order = Order(
        order_number=order_number,
        customer_name=order_data.customer_name,
        email=order_data.email,
        phone=order_data.phone,
        address=order_data.address,
        place_id=order_data.place_id,
    )

    # Save to database
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Send confirmation email
    email_sent = send_order_confirmation_email(
        recipient_email=order_data.email,
        order_number=order_number
    )

    # Log email delivery status
    email_log = EmailLog(
        order_id=db_order.id,
        recipient=order_data.email,
        subject=f"주문 확인 - {order_number}",
        status="sent" if email_sent else "failed"
    )
    db.add(email_log)
    db.commit()

    return db_order, email_sent
