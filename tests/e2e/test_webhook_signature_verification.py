"""Acceptance Test: PayPal Webhook 서명 검증

보안 요구사항:
- PayPal에서 보낸 Webhook만 처리
- 위조된 Webhook 요청 거부
- 서명 검증 실패 시 401 Unauthorized 응답
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
def valid_paypal_headers():
    """유효한 PayPal Webhook 서명 헤더"""
    return {
        "paypal-transmission-id": "12345-67890-abcde",
        "paypal-transmission-time": "2024-01-15T10:30:00Z",
        "paypal-transmission-sig": "valid-signature-hash",
        "paypal-auth-algo": "SHA256withRSA",
        "paypal-cert-url": "https://api.sandbox.paypal.com/v1/notifications/certs/CERT-123",
    }


@pytest.fixture
def sample_webhook_event():
    """PayPal Webhook 이벤트 데이터"""
    return {
        "event_type": "PAYMENT.CAPTURE.COMPLETED",
        "resource": {
            "id": "CAPTURE-12345",
            "status": "COMPLETED",
            "custom_id": "ORD-TEST123",
        }
    }


@pytest.mark.e2e
def test_webhook_with_valid_signature_succeeds(
    test_client: TestClient,
    reset_mock_data,
    valid_paypal_headers,
    sample_webhook_event
):
    """유효한 서명이 있으면 Webhook 처리 성공

    Given: 주문이 생성되고 PayPal에서 결제 완료
    When: 유효한 서명과 함께 Webhook 전송
    Then:
      - 서명 검증 통과
      - 200 OK 응답
      - 이벤트 처리 완료
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
    assert response.status_code == 201

    order_number = response.json()["order_number"]
    sample_webhook_event["resource"]["custom_id"] = order_number

    # When: PayPal SDK의 서명 검증을 Mock (유효한 서명)
    with patch("backend.api.webhooks.WebhookEvent.verify") as mock_verify:
        mock_verify.return_value = True

        # Webhook 전송 (유효한 서명 헤더 포함)
        webhook_response = test_client.post(
            "/webhooks/paypal",
            json=sample_webhook_event,
            headers=valid_paypal_headers
        )

        # Then: 서명 검증 성공
        assert webhook_response.status_code == 200

        # PayPal SDK verify() 호출 확인
        mock_verify.assert_called_once()

        # 주문 상태 확인 (이벤트 처리 완료)
        order_check = test_client.get(f"/api/orders/{order_number}")
        assert order_check.json()["order_status"] == "PAID"


@pytest.mark.e2e
def test_webhook_with_invalid_signature_fails(
    test_client: TestClient,
    reset_mock_data,
    valid_paypal_headers,
    sample_webhook_event
):
    """잘못된 서명이면 401 Unauthorized 응답

    Given: 공격자가 위조된 Webhook 전송 시도
    When: 서명 검증 실패
    Then:
      - 401 Unauthorized 응답
      - 이벤트 처리 안 됨
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
    sample_webhook_event["resource"]["custom_id"] = order_number

    # When: PayPal SDK의 서명 검증 실패
    with patch("backend.api.webhooks.WebhookEvent.verify") as mock_verify:
        mock_verify.return_value = False  # 서명 검증 실패

        # 위조된 Webhook 전송
        webhook_response = test_client.post(
            "/webhooks/paypal",
            json=sample_webhook_event,
            headers=valid_paypal_headers
        )

        # Then: 401 Unauthorized
        assert webhook_response.status_code == 401
        assert "signature" in webhook_response.json()["detail"].lower()

        # 주문 상태는 변경되지 않아야 함
        order_check = test_client.get(f"/api/orders/{order_number}")
        assert order_check.json()["order_status"] == "PAYMENT_PENDING"


@pytest.mark.e2e
def test_webhook_without_signature_headers_fails(
    test_client: TestClient,
    reset_mock_data,
    sample_webhook_event
):
    """서명 헤더 없으면 401 Unauthorized 응답

    Given: 서명 헤더 없이 Webhook 전송
    When: 서명 검증 시도
    Then:
      - 401 Unauthorized 응답
      - 이벤트 처리 안 됨
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
    sample_webhook_event["resource"]["custom_id"] = order_number

    # When: 서명 헤더 없이 Webhook 전송
    webhook_response = test_client.post(
        "/webhooks/paypal",
        json=sample_webhook_event,
        # headers 없음
    )

    # Then: 401 Unauthorized
    assert webhook_response.status_code == 401


@pytest.mark.e2e
def test_webhook_signature_verification_exception_fails(
    test_client: TestClient,
    reset_mock_data,
    valid_paypal_headers,
    sample_webhook_event
):
    """서명 검증 중 예외 발생 시 401 응답

    Given: 서명 검증 중 네트워크 오류 등 예외 발생
    When: 예외 발생
    Then:
      - 401 Unauthorized 응답
      - 이벤트 처리 안 됨
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
    sample_webhook_event["resource"]["custom_id"] = order_number

    # When: PayPal SDK 호출 시 예외 발생
    with patch("backend.api.webhooks.WebhookEvent.verify") as mock_verify:
        mock_verify.side_effect = Exception("Network error")

        # Webhook 전송
        webhook_response = test_client.post(
            "/webhooks/paypal",
            json=sample_webhook_event,
            headers=valid_paypal_headers
        )

        # Then: 401 Unauthorized
        assert webhook_response.status_code == 401

        # 주문 상태는 변경되지 않아야 함
        order_check = test_client.get(f"/api/orders/{order_number}")
        assert order_check.json()["order_status"] == "PAYMENT_PENDING"
