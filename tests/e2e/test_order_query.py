"""E2E 테스트: 주문 조회 API

Outside-In TDD - 가장 단순한 성공 케이스부터 시작
"""
import pytest
from fastapi.testclient import TestClient
from tests.fixtures.factories import create_product, create_order, create_shipment


@pytest.mark.e2e
def test_query_order_returns_order_details(test_client: TestClient, db_session):
    """주문 번호로 주문을 조회하면 주문 정보가 반환된다"""
    # Given: DB에 주문 생성
    order_number = "ORD-12345678"

    product = create_product(db_session)
    order = create_order(
        db_session,
        product_id=product.id,
        order_number=order_number,
        order_status="PAYMENT_PENDING"
    )
    db_session.commit()

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
def test_query_nonexistent_order_returns_404(test_client: TestClient, db_session):
    """존재하지 않는 주문 번호로 조회 시 404를 반환한다"""
    # Given: 존재하지 않는 주문 번호 (DB에 데이터 생성 안 함)
    order_number = "ORD-99999999"

    # When: 주문 조회 API를 호출
    response = test_client.get(f"/api/orders/{order_number}")

    # Then: 404 Not Found 응답
    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data


@pytest.mark.e2e
def test_when_querying_order_with_preparing_shipment_then_returns_shipment_info(test_client, db_session):
    """
    Phase 3: 주문 조회 페이지 - PREPARING 상태 배송 정보 표시

    Given: PAID order with PREPARING shipment (no tracking/courier)
    When: Query order by order_number
    Then: Returns shipment with status PREPARING and null tracking info
    """
    # Given: PAID 상태 주문 + PREPARING shipment
    product = create_product(db_session)
    order = create_order(db_session, product_id=product.id, order_number="ORD-TEST001")
    shipment = create_shipment(db_session, order_id=order.id, shipping_status="PREPARING")
    db_session.commit()

    # When: 주문 조회
    response = test_client.get("/api/orders/ORD-TEST001")

    # Then: shipment 정보 포함
    assert response.status_code == 200
    data = response.json()

    assert data["order_number"] == "ORD-TEST001"
    assert data["order_status"] == "PAID"

    assert "shipment" in data
    shipment_data = data["shipment"]

    assert shipment_data["shipping_status"] == "PREPARING"
    assert shipment_data["tracking_number"] is None
    assert shipment_data["courier"] is None
    assert shipment_data["shipped_at"] is None
    assert shipment_data["delivered_at"] is None


@pytest.mark.e2e
def test_when_querying_order_with_shipped_shipment_then_returns_tracking_info(test_client, db_session):
    """
    Phase 3: 주문 조회 페이지 - SHIPPED 상태 배송 정보 표시

    Given: PAID order with SHIPPED shipment (with tracking/courier)
    When: Query order by order_number
    Then: Returns shipment with complete tracking information
    """
    # Given: PAID 상태 주문 + SHIPPED shipment
    from datetime import datetime

    product = create_product(db_session)
    order = create_order(db_session, product_id=product.id, order_number="ORD-TEST002")

    shipped_at = datetime(2025, 1, 15, 10, 30, 0)
    shipment = create_shipment(
        db_session,
        order_id=order.id,
        shipping_status="SHIPPED",
        tracking_number="1234567890",
        courier="LBC Express",
        shipped_at=shipped_at
    )
    db_session.commit()

    # When: 주문 조회
    response = test_client.get("/api/orders/ORD-TEST002")

    # Then: 전체 배송 정보 포함
    assert response.status_code == 200
    data = response.json()

    assert data["order_number"] == "ORD-TEST002"
    assert data["order_status"] == "PAID"

    assert "shipment" in data
    shipment_data = data["shipment"]

    assert shipment_data["shipping_status"] == "SHIPPED"
    assert shipment_data["tracking_number"] == "1234567890"
    assert shipment_data["courier"] == "LBC Express"
    assert shipment_data["shipped_at"] is not None  # 타임스탬프 존재
    assert shipment_data["delivered_at"] is None  # 아직 배송 완료 안됨


@pytest.mark.e2e
def test_when_querying_order_with_delivered_shipment_then_returns_delivery_completion(test_client, db_session):
    """
    Phase 3: 주문 조회 페이지 - DELIVERED 상태 배송 정보 표시

    Given: PAID order with DELIVERED shipment (with delivery completion time)
    When: Query order by order_number
    Then: Returns shipment with delivered_at timestamp
    """
    # Given: PAID 상태 주문 + DELIVERED shipment
    from datetime import datetime

    product = create_product(db_session)
    order = create_order(db_session, product_id=product.id, order_number="ORD-TEST003")

    shipped_at = datetime(2025, 1, 15, 10, 30, 0)
    delivered_at = datetime(2025, 1, 17, 14, 20, 0)

    shipment = create_shipment(
        db_session,
        order_id=order.id,
        shipping_status="DELIVERED",
        tracking_number="9876543210",
        courier="J&T Express",
        shipped_at=shipped_at,
        delivered_at=delivered_at
    )
    db_session.commit()

    # When: 주문 조회
    response = test_client.get("/api/orders/ORD-TEST003")

    # Then: 배송 완료 정보 포함
    assert response.status_code == 200
    data = response.json()

    assert data["order_number"] == "ORD-TEST003"
    assert data["order_status"] == "PAID"

    assert "shipment" in data
    shipment_data = data["shipment"]

    assert shipment_data["shipping_status"] == "DELIVERED"
    assert shipment_data["tracking_number"] == "9876543210"
    assert shipment_data["courier"] == "J&T Express"
    assert shipment_data["shipped_at"] is not None
    assert shipment_data["delivered_at"] is not None  # 배송 완료 시각 존재
