from pydantic import BaseModel, EmailStr


class OrderCreate(BaseModel):
    """Schema for creating a new order."""

    customer_name: str
    email: EmailStr
    phone: str
    address: str
    place_id: str | None = None


class OrderResponse(BaseModel):
    """Schema for order API response."""

    order_id: str
    status: str
    email_sent: bool

    class Config:
        from_attributes = True
