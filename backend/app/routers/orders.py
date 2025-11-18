from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import OrderCreate, OrderResponse
from app.services.order_service import create_order

router = APIRouter()


@router.post("/orders/create", response_model=OrderResponse)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order and send confirmation email.

    This endpoint:
    1. Saves order to Cloud SQL database
    2. Sends confirmation email via Gmail SMTP
    3. Logs email delivery status
    4. Returns order ID and status
    """
    try:
        db_order, email_sent = create_order(db, order)

        return OrderResponse(
            order_id=db_order.order_number,
            status="created",
            email_sent=email_sent
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")
