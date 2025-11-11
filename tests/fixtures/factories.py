"""테스트 데이터 Factory 함수들"""
from typing import Dict, Any
from sqlalchemy.orm import Session
from backend.models.db import ProductDB, OrderDB, ShipmentDB
from backend.utils.encryption import encrypt


def create_purchase_data(
    name: str = "Juan Dela Cruz",
    phone: str = "+63-917-123-4567",
    email: str = "juan@example.com",
    address: str = "123 Rizal Avenue, Makati City, Metro Manila",
    **kwargs: Any,
) -> Dict[str, str]:
    """구매 정보 테스트 데이터 생성 (필리핀 고객 기준)"""
    data = {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
    }
    data.update(kwargs)
    return data


def create_product(db: Session, **overrides) -> ProductDB:
    """Product 생성 Factory

    Args:
        db: DB 세션
        **overrides: 기본값 오버라이드

    Returns:
        ProductDB: 생성된 Product (DB에 추가되고 flush됨)
    """
    defaults = {
        "name": "조선미녀 맑은쌀 선크림",
        "price": 57500,
        "stock": 10
    }
    product = ProductDB(**{**defaults, **overrides})
    db.add(product)
    db.flush()  # ID 생성
    return product


def create_order(db: Session, product_id: int, **overrides) -> OrderDB:
    """Order 생성 Factory

    Args:
        db: DB 세션
        product_id: 상품 ID (필수)
        **overrides: 기본값 오버라이드

    Returns:
        OrderDB: 생성된 Order (DB에 추가되고 flush됨)
    """
    defaults = {
        "order_number": "ORD-TEST001",
        "customer_name": encrypt("Maria Santos"),
        "customer_email": encrypt("maria@test.com"),
        "customer_phone": encrypt("+63-917-123-4567"),
        "shipping_address": encrypt("123 Test St, Manila"),
        "quantity": 2,
        "unit_price": 57500,
        "shipping_fee": 10000,
        "total_amount": 125000,
        "order_status": "PAID"
    }
    order = OrderDB(product_id=product_id, **{**defaults, **overrides})
    db.add(order)
    db.flush()  # ID 생성
    return order


def create_shipment(db: Session, order_id: int, **overrides) -> ShipmentDB:
    """Shipment 생성 Factory

    Args:
        db: DB 세션
        order_id: 주문 ID (필수)
        **overrides: 기본값 오버라이드

    Returns:
        ShipmentDB: 생성된 Shipment (DB에 추가되고 flush됨)
    """
    defaults = {
        "shipping_status": "PREPARING",
        "tracking_number": None,
        "courier": None
    }
    shipment = ShipmentDB(order_id=order_id, **{**defaults, **overrides})
    db.add(shipment)
    db.flush()
    return shipment
