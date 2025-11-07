"""Integration 테스트: 주문 생성 API

Outside-In TDD - UI에서 필요성을 발견한 POST /api/orders API 테스트
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
def test_create_order_returns_order_info_and_paypal_url(test_client: TestClient):
    """유효한 주문 데이터로 주문 생성 시 주문 정보와 PayPal URL을 반환한다

    가장 단순한 성공 케이스
    """
    # Given: 유효한 주문 데이터
    order_data = {
        "customer_name": "Maria Santos",
        "customer_email": "maria.santos@example.com",
        "customer_phone": "+63-917-123-4567",
        "shipping_address": "123 Rizal Avenue, Makati City, Metro Manila 1200",
        "product_id": 1,
        "quantity": 2,
    }

    # When: 주문 생성 API 호출
    response = test_client.post("/api/orders", json=order_data)

    # Then: 201 Created 응답
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"

    result = response.json()

    # 주문 번호 생성됨 (ORD-XXXXXXXX 형식)
    assert "order_number" in result
    assert result["order_number"].startswith("ORD-")
    assert len(result["order_number"]) == 12  # ORD- + 8자리

    # PayPal 정보 포함
    assert "paypal_order_id" in result
    assert "approval_url" in result
    assert result["approval_url"].startswith("https://")

    # 총액 정보 (575 * 2 + 100 = 1,250 페소 = 125,000 센타보)
    assert "total_amount" in result
    assert result["total_amount"] == 125000


@pytest.mark.integration
def test_create_order_with_invalid_data_returns_422(test_client: TestClient):
    """필수 필드 누락 시 422 Unprocessable Entity를 반환한다"""
    # Given: customer_name 누락된 데이터
    invalid_data = {
        "customer_email": "maria.santos@example.com",
        "customer_phone": "+63-917-123-4567",
        "shipping_address": "123 Rizal Avenue, Makati City",
        "product_id": 1,
        "quantity": 2,
    }

    # When: 주문 생성 API 호출
    response = test_client.post("/api/orders", json=invalid_data)

    # Then: 422 Unprocessable Entity
    assert response.status_code == 422


@pytest.mark.integration
def test_create_order_with_invalid_quantity_returns_422(test_client: TestClient):
    """수량이 0 이하일 때 422를 반환한다"""
    # Given: 수량이 0인 데이터
    invalid_data = {
        "customer_name": "Maria Santos",
        "customer_email": "maria.santos@example.com",
        "customer_phone": "+63-917-123-4567",
        "shipping_address": "123 Rizal Avenue, Makati City",
        "product_id": 1,
        "quantity": 0,  # 유효하지 않은 수량
    }

    # When: 주문 생성 API 호출
    response = test_client.post("/api/orders", json=invalid_data)

    # Then: 422 Unprocessable Entity
    assert response.status_code == 422


@pytest.mark.integration
def test_create_order_with_insufficient_stock_returns_409(test_client: TestClient):
    """재고가 부족할 때 409 Conflict를 반환한다

    TODO: 이 테스트는 DB 연결 후 실제 재고 확인이 가능해지면 통과할 것
    지금은 Skip 또는 Mock으로 처리
    """
    pytest.skip("재고 관리 기능은 DB 연결 후 구현 예정")
