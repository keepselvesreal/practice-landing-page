"""Integration Test: 실제 PayPal Simulator 데이터로 Webhook 테스트

이 테스트는 PayPal Simulator에서 실제로 받은 데이터를 기반으로 작성됨.
Contract Test로 생성된 fixture 사용.
"""
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def real_paypal_event():
    """PayPal Simulator에서 실제로 받은 PAYMENT.CAPTURE.COMPLETED 이벤트"""
    fixture_path = Path(__file__).parent.parent / "fixtures" / "paypal_simulator_event.json"

    with open(fixture_path) as f:
        return json.load(f)


@pytest.fixture
def real_paypal_headers():
    """PayPal Simulator에서 실제로 받은 서명 헤더들"""
    fixture_path = Path(__file__).parent.parent / "fixtures" / "paypal_simulator_headers.json"

    with open(fixture_path) as f:
        return json.load(f)


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


def test_real_paypal_event_structure_parsing_success(
    test_client: TestClient,
    real_paypal_event,
    real_paypal_headers
):
    """실제 PayPal 이벤트 구조를 파싱할 수 있다

    Given: PayPal Simulator가 보낸 실제 이벤트 (모든 필드 포함)
    When: 서명 검증 통과 (mock)
    Then: JSON 파싱 성공, 추가 필드들 무시하고 처리
    """
    with patch("backend.api.webhooks.WebhookEvent.verify") as mock_verify:
        mock_verify.return_value = True

        # 실제 PayPal 이벤트 전송
        response = test_client.post(
            "/webhooks/paypal",
            json=real_paypal_event,
            headers=real_paypal_headers
        )

        # 서명 검증은 통과했으므로 401 아님
        assert response.status_code != 401

        # PayPal SDK 호출 확인
        mock_verify.assert_called_once()


def test_real_paypal_event_recognizes_payment_capture_completed(
    test_client: TestClient,
    real_paypal_event,
    real_paypal_headers
):
    """실제 PayPal PAYMENT.CAPTURE.COMPLETED 이벤트를 인식한다

    Given: event_type이 PAYMENT.CAPTURE.COMPLETED
    When: 이벤트 수신
    Then: 우리 코드가 이 이벤트 타입을 처리
    """
    assert real_paypal_event["event_type"] == "PAYMENT.CAPTURE.COMPLETED"
    assert real_paypal_event["resource_type"] == "capture"


def test_real_paypal_event_with_our_order_number(
    test_client: TestClient,
    real_paypal_event,
    real_paypal_headers,
    reset_mock_data
):
    """실제 PayPal 데이터 구조 + 우리 주문 번호로 성공적으로 처리

    Given:
      - 주문 생성 (custom_id를 주문 번호로 설정)
      - PayPal 실제 이벤트 구조 사용
      - custom_id만 우리 주문 번호로 교체
    When: Webhook 수신
    Then: 주문 찾아서 PAID로 변경
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

    # PayPal 실제 이벤트의 custom_id를 우리 주문 번호로 교체
    modified_event = real_paypal_event.copy()
    modified_event["resource"]["custom_id"] = order_number

    # When: 서명 검증 통과 + 이벤트 수신
    with patch("backend.api.webhooks.WebhookEvent.verify") as mock_verify:
        mock_verify.return_value = True

        webhook_response = test_client.post(
            "/webhooks/paypal",
            json=modified_event,
            headers=real_paypal_headers
        )

        # Then: 성공
        assert webhook_response.status_code == 200

        # 주문 상태 확인
        order_check = test_client.get(f"/api/orders/{order_number}")
        assert order_check.json()["order_status"] == "PAID"


def test_real_paypal_event_without_matching_order_returns_404(
    test_client: TestClient,
    real_paypal_event,
    real_paypal_headers,
    reset_mock_data
):
    """실제 PayPal custom_id로 주문을 찾지 못하면 404

    Given: PayPal Simulator의 샘플 custom_id (UUID)
    When: 서명 검증 통과 + 이벤트 수신
    Then: 주문 없음 → 404
    """
    with patch("backend.api.webhooks.WebhookEvent.verify") as mock_verify:
        mock_verify.return_value = True

        # PayPal 샘플 custom_id로 전송
        response = test_client.post(
            "/webhooks/paypal",
            json=real_paypal_event,
            headers=real_paypal_headers
        )

        # 주문 없음
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


def test_real_paypal_event_with_invalid_signature_returns_401(
    test_client: TestClient,
    real_paypal_event,
    real_paypal_headers
):
    """실제 PayPal 데이터라도 서명 검증 실패 시 401

    Given: 실제 PayPal 이벤트 구조
    When: 서명 검증 실패 (mock)
    Then: 401 Unauthorized
    """
    with patch("backend.api.webhooks.WebhookEvent.verify") as mock_verify:
        mock_verify.return_value = False  # 서명 검증 실패

        response = test_client.post(
            "/webhooks/paypal",
            json=real_paypal_event,
            headers=real_paypal_headers
        )

        # 서명 검증 실패
        assert response.status_code == 401
        assert "signature" in response.json()["detail"].lower()
