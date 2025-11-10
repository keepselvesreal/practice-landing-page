"""Acceptance Test: PayPal 결제 완료 후 이메일 발송

사용자 스토리:
- 고객이 PayPal로 결제를 완료하면
- 시스템이 Webhook을 수신하고
- 주문 상태를 PAID로 변경하며
- 고객에게 주문 확인 이메일을 발송한다
"""
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def reset_mock_data():
    """각 테스트마다 Mock 데이터 초기화"""
    from backend.api.orders import MOCK_ORDERS, MOCK_PRODUCTS
    from backend.api.webhooks import PROCESSED_WEBHOOK_EVENTS

    # 재고 초기화
    MOCK_PRODUCTS[1].stock = 10

    # 주문 데이터 초기화
    MOCK_ORDERS.clear()

    # Webhook 이벤트 기록 초기화
    PROCESSED_WEBHOOK_EVENTS.clear()

    yield

    # 테스트 후 정리
    MOCK_PRODUCTS[1].stock = 10
    MOCK_ORDERS.clear()
    PROCESSED_WEBHOOK_EVENTS.clear()


@pytest.fixture
def sample_paypal_webhook_completed():
    """PayPal Webhook - PAYMENT.CAPTURE.COMPLETED 이벤트"""
    return {
        "event_type": "PAYMENT.CAPTURE.COMPLETED",
        "resource": {
            "id": "8XY12345ABCD67890",  # PayPal Capture ID
            "status": "COMPLETED",
            "amount": {
                "currency_code": "PHP",
                "value": "1250.00"
            },
            "custom_id": "ORD-TEST123456",  # 주문 번호
        }
    }


@pytest.fixture
def sample_paypal_webhook_denied():
    """PayPal Webhook - PAYMENT.CAPTURE.DENIED 이벤트"""
    return {
        "event_type": "PAYMENT.CAPTURE.DENIED",
        "resource": {
            "id": "8XY12345ABCD67890",
            "status": "DECLINED",
            "amount": {
                "currency_code": "PHP",
                "value": "1250.00"
            },
            "custom_id": "ORD-TEST123456",
        }
    }


@pytest.mark.e2e
def test_customer_receives_email_after_successful_payment(
    test_client: TestClient,
    reset_mock_data,
    sample_paypal_webhook_completed
):
    """결제 완료 후 고객이 주문 확인 이메일을 받는다

    Given: 주문이 생성되고 PayPal 결제 대기 중
    When: PayPal Webhook으로 PAYMENT.CAPTURE.COMPLETED 이벤트 수신
    Then:
      - 주문 상태가 PAID로 변경
      - 고객에게 이메일 발송
      - 이메일에 주문 정보 포함
    """
    # Given: 주문 생성
    order_data = {
        "customer_name": "Maria Santos",
        "customer_email": "maria.santos@example.com",
        "customer_phone": "+63-917-123-4567",
        "shipping_address": "123 Rizal Avenue, Makati City, Metro Manila 1200",
        "product_id": 1,
        "quantity": 2,
        "affiliate_code": None,
    }

    # 주문 생성 (재고 차감됨)
    response = test_client.post("/api/orders", json=order_data)
    assert response.status_code == 201

    order_result = response.json()
    order_number = order_result["order_number"]

    # Webhook 이벤트에 주문 번호 설정
    sample_paypal_webhook_completed["resource"]["custom_id"] = order_number

    # When: 이메일 발송 Mock (webhooks.py에서 import한 위치를 패치)
    with patch("backend.api.webhooks.send_order_confirmation_email") as mock_send_email:
        mock_send_email.return_value = True

        # PayPal Webhook 호출
        webhook_response = test_client.post(
            "/webhooks/paypal",
            json=sample_paypal_webhook_completed,
            headers={"Content-Type": "application/json"}
        )

        # Then: Webhook 성공
        assert webhook_response.status_code == 200

        # 주문 상태 확인
        order_check = test_client.get(f"/api/orders/{order_number}")
        assert order_check.status_code == 200

        order_info = order_check.json()
        assert order_info["order_status"] == "PAID"

        # 이메일 발송 확인
        mock_send_email.assert_called_once()

        # 발송된 이메일 인자 확인
        call_args = mock_send_email.call_args
        email_order = call_args[0][0]  # 첫 번째 인자 (OrderResponse)

        assert email_order.order_number == order_number
        assert email_order.customer_email == "maria.santos@example.com"
        assert email_order.order_status == "PAID"


@pytest.mark.e2e
def test_stock_restored_when_payment_fails(
    test_client: TestClient,
    reset_mock_data,
    sample_paypal_webhook_denied
):
    """결제 실패 시 재고가 복원된다

    Given: 주문 생성으로 재고 2개 차감 (8개 남음)
    When: PayPal Webhook으로 PAYMENT.CAPTURE.DENIED 이벤트 수신
    Then:
      - 주문 상태가 FAILED로 변경
      - 재고가 10개로 복원
    """
    from backend.api.orders import MOCK_PRODUCTS

    # Given: 초기 재고 확인
    initial_stock = MOCK_PRODUCTS[1].stock
    assert initial_stock == 10

    # 주문 생성 (재고 2개 차감)
    order_data = {
        "customer_name": "Maria Santos",
        "customer_email": "maria.santos@example.com",
        "customer_phone": "+63-917-123-4567",
        "shipping_address": "123 Rizal Avenue, Makati City, Metro Manila 1200",
        "product_id": 1,
        "quantity": 2,
        "affiliate_code": None,
    }

    response = test_client.post("/api/orders", json=order_data)
    assert response.status_code == 201

    order_result = response.json()
    order_number = order_result["order_number"]

    # 재고 차감 확인
    assert MOCK_PRODUCTS[1].stock == 8

    # Webhook 이벤트에 주문 번호 설정
    sample_paypal_webhook_denied["resource"]["custom_id"] = order_number

    # When: PayPal Webhook 호출 (결제 실패)
    webhook_response = test_client.post(
        "/webhooks/paypal",
        json=sample_paypal_webhook_denied,
        headers={"Content-Type": "application/json"}
    )

    # Then: Webhook 성공
    assert webhook_response.status_code == 200

    # 주문 상태 확인
    order_check = test_client.get(f"/api/orders/{order_number}")
    assert order_check.status_code == 200

    order_info = order_check.json()
    assert order_info["order_status"] == "FAILED"

    # 재고 복원 확인
    assert MOCK_PRODUCTS[1].stock == 10


@pytest.mark.e2e
def test_webhook_ignores_duplicate_events(
    test_client: TestClient,
    reset_mock_data
):
    """중복된 Webhook 이벤트는 무시된다

    Given: 결제 완료로 주문 상태가 PAID
    When: 동일한 PAYMENT.CAPTURE.COMPLETED 이벤트 재전송
    Then:
      - 중복 처리 방지
      - 이메일 중복 발송 안 됨
    """
    # Given: 주문 생성
    order_data = {
        "customer_name": "Maria Santos",
        "customer_email": "maria.santos@example.com",
        "customer_phone": "+63-917-123-4567",
        "shipping_address": "123 Rizal Avenue, Makati City, Metro Manila 1200",
        "product_id": 1,
        "quantity": 2,
    }

    response = test_client.post("/api/orders", json=order_data)
    order_number = response.json()["order_number"]

    webhook_event = {
        "event_type": "PAYMENT.CAPTURE.COMPLETED",
        "resource": {
            "id": "8XY12345ABCD67890",
            "status": "COMPLETED",
            "custom_id": order_number,
        }
    }

    with patch("backend.api.webhooks.send_order_confirmation_email") as mock_send_email:
        mock_send_email.return_value = True

        # 첫 번째 Webhook 호출
        response1 = test_client.post("/webhooks/paypal", json=webhook_event)
        assert response1.status_code == 200

        # 두 번째 Webhook 호출 (중복)
        response2 = test_client.post("/webhooks/paypal", json=webhook_event)
        assert response2.status_code == 200

        # 이메일은 1번만 발송되어야 함
        assert mock_send_email.call_count == 1
