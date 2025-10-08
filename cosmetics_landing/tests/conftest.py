"""
Pytest Configuration
"""
import pytest
from fastapi.testclient import TestClient

from cosmetics_landing.config.main import create_app


@pytest.fixture
def client():
    """
    FastAPI 테스트 클라이언트

    E2E 테스트용 애플리케이션 인스턴스
    """
    app = create_app()
    return TestClient(app)


@pytest.fixture
def valid_order_data():
    """유효한 주문 데이터"""
    return {
        "customer_email": "test@example.com",
        "customer_address": "123 Main St, Manila, Philippines",
        "product_price": 29.99
    }


@pytest.fixture
def order_with_affiliate():
    """어필리에이트 코드가 포함된 주문 데이터"""
    return {
        "customer_email": "test@example.com",
        "customer_address": "123 Main St, Manila, Philippines",
        "product_price": 29.99,
        "affiliate_code": "INFLUENCER123"
    }
