"""전역 pytest fixture 설정"""
import os
from pathlib import Path
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# .env 파일 로드
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


@pytest.fixture(scope="session")
def base_url() -> str:
    """테스트용 기본 URL"""
    return "http://localhost:8000"


@pytest.fixture(scope="function")
def test_client() -> Generator[TestClient, None, None]:
    """FastAPI TestClient fixture"""
    from backend.main import app

    yield TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    """테스트용 DB 세션 (각 테스트마다 초기화)"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from backend.db.base import Base
    from backend.db.base import get_db

    TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
    if not TEST_DATABASE_URL:
        raise ValueError("TEST_DATABASE_URL not set")

    # 테스트 DB Engine 생성
    engine = create_engine(TEST_DATABASE_URL, echo=False)

    # 테이블 생성
    Base.metadata.create_all(bind=engine)

    # 세션 생성
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # FastAPI app의 DB dependency 오버라이드
    from backend.main import app
    def override_get_db():
        try:
            yield session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db

    yield session

    # Teardown: 세션 종료 및 테이블 삭제
    session.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    app.dependency_overrides.clear()


@pytest.fixture
def test_data(db_session):
    """테스트 데이터 생성"""
    from backend.models.db import ProductDB, OrderDB, ShipmentDB
    from backend.utils.encryption import encrypt

    # Product (id는 자동 생성)
    product = ProductDB(
        name="조선미녀 맑은쌀 선크림",
        price=57500,
        stock=10
    )
    db_session.add(product)
    db_session.flush()  # ID 생성을 위해 flush

    # Order (암호화된 정보)
    order = OrderDB(
        order_number="ORD-12345678",
        customer_name=encrypt("charmaine"),
        customer_email=encrypt("test@example.com"),
        customer_phone=encrypt("+63 912 345 6789"),
        shipping_address=encrypt("123 Test St, Manila, Philippines"),
        product_id=product.id,  # 자동 생성된 product.id 사용
        quantity=1,
        unit_price=57500,
        shipping_fee=10000,
        total_amount=67500,
        affiliate_code=None,
        paypal_order_id="PAYPAL-ORDER-123",
        paypal_transaction_id="PAYPAL-TXN-456",
        order_status="PAID"
    )
    db_session.add(order)
    db_session.flush()  # ID 생성을 위해 flush

    # Shipment
    shipment = ShipmentDB(
        order_id=order.id,  # 자동 생성된 order.id 사용
        shipping_status="PREPARING",
        tracking_number=None,
        courier=None,
        shipped_at=None,
        delivered_at=None
    )
    db_session.add(shipment)

    db_session.commit()

    return {
        "product": product,
        "order": order,
        "shipment": shipment
    }
