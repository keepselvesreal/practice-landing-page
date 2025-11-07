"""E2E 테스트: 주문 조회 API

Outside-In TDD - 가장 단순한 성공 케이스부터 시작
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.e2e
def test_query_order_returns_order_details(test_client: TestClient):
    """주문 번호로 주문을 조회하면 주문 정보가 반환된다"""
    # Given: 시스템에 주문 ORD-12345678이 존재함
    order_number = "ORD-12345678"

    # When: 주문 조회 API를 호출
    response = test_client.get(f"/api/orders/{order_number}")

    # Then: 200 OK 응답과 함께 주문 정보가 반환됨
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    order_data = response.json()

    # 주문 기본 정보 확인
    assert order_data["order_number"] == order_number
    assert "customer_name" in order_data
    assert "customer_email" in order_data
    assert "customer_phone" in order_data
    assert "shipping_address" in order_data

    # 주문 상품 정보 확인
    assert "product_id" in order_data
    assert "quantity" in order_data
    assert "unit_price" in order_data
    assert "shipping_fee" in order_data
    assert "total_amount" in order_data

    # 주문 상태 확인
    assert "order_status" in order_data
    assert order_data["order_status"] == "PAYMENT_PENDING"


@pytest.mark.e2e
def test_query_nonexistent_order_returns_404(test_client: TestClient):
    """존재하지 않는 주문 번호로 조회 시 404를 반환한다"""
    # Given: 시스템에 존재하지 않는 주문 번호
    order_number = "ORD-99999999"

    # When: 주문 조회 API를 호출
    response = test_client.get(f"/api/orders/{order_number}")

    # Then: 404 Not Found 응답
    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data
