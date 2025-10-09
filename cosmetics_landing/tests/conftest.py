"""
Pytest Configuration
"""
import pytest
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from cosmetics_landing.config.main import create_app

# .env 파일 로드 (프로젝트 루트의 상위 디렉토리)
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


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


# pytest marker 설정
def pytest_configure(config):
    """pytest 설정"""
    config.addinivalue_line(
        "markers", "learning: mark test as learning test (external API contract verification)"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (real external services)"
    )
