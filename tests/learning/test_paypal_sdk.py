"""Learning Test: PayPal SDK 동작 확인

외부 서비스(PayPal Sandbox)의 동작 방식과 응답 구조를 파악하기 위한 테스트
실제 PayPal API를 호출하므로 느릴 수 있음
"""
import os
import pytest
from paypalserversdk.paypal_serversdk_client import PaypalServersdkClient
from paypalserversdk.http.auth.o_auth_2 import ClientCredentialsAuthCredentials
from paypalserversdk.configuration import Environment


@pytest.fixture(scope="module")
def paypal_client():
    """PayPal SDK Client 초기화"""
    client_id = os.getenv("PAYPAL_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET")

    if not client_id or not client_secret:
        pytest.skip("PayPal credentials not configured")

    client = PaypalServersdkClient(
        client_credentials_auth_credentials=ClientCredentialsAuthCredentials(
            o_auth_client_id=client_id,
            o_auth_client_secret=client_secret
        ),
        environment=Environment.SANDBOX
    )

    return client


@pytest.mark.learning
@pytest.mark.integration
def test_paypal_create_order_basic(paypal_client: PaypalServersdkClient):
    """PayPal Order 생성 기본 테스트

    목적:
    - PayPal SDK가 제대로 동작하는지 확인
    - Order 생성 요청/응답 구조 파악
    - approval_url 형식 확인
    """
    orders_controller = paypal_client.orders

    # Order 생성 요청 (최소한의 필드)
    order_body = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "PHP",
                    "value": "1250.00"
                }
            }
        ]
    }

    # API 호출
    result = orders_controller.create_order(
        {
            "body": order_body,
            "prefer": "return=representation"
        }
    )

    # 응답 확인
    assert result.status_code == 201
    assert result.body is not None

    order = result.body
    print(f"\n📦 Created Order ID: {order.id}")
    print(f"📦 Status: {order.status}")
    print(f"📦 Intent: {order.intent}")

    # Links 확인
    assert order.links is not None
    assert len(order.links) > 0

    # approval_url 찾기
    approval_url = None
    for link in order.links:
        print(f"🔗 Link: {link.rel} -> {link.href}")
        if link.rel == "approve":
            approval_url = link.href

    assert approval_url is not None
    assert "sandbox.paypal.com" in approval_url

    print(f"\n✅ Approval URL: {approval_url}")
    print(f"✅ Order created successfully!")


@pytest.mark.learning
@pytest.mark.integration
def test_paypal_order_response_structure(paypal_client: PaypalServersdkClient):
    """PayPal Order 응답 구조 확인

    목적: Adapter 작성을 위한 응답 필드 파악
    """
    orders_controller = paypal_client.orders

    order_body = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "PHP",
                    "value": "675.00"
                }
            }
        ]
    }

    result = orders_controller.create_order(
        {
            "body": order_body,
            "prefer": "return=representation"
        }
    )

    order = result.body

    # 응답 구조 출력
    print("\n📋 Order Response Structure:")
    print(f"  - id: {order.id}")
    print(f"  - status: {order.status}")
    print(f"  - intent: {order.intent}")

    if hasattr(order, 'create_time'):
        print(f"  - create_time: {order.create_time}")

    if hasattr(order, 'purchase_units') and order.purchase_units:
        print(f"  - purchase_units[0].amount: {order.purchase_units[0].amount}")

    if hasattr(order, 'links') and order.links:
        print(f"  - links: {len(order.links)} links")
        for link in order.links:
            print(f"    - {link.rel}: {link.href}")

    # Adapter 작성 시 필요한 필드 확인
    assert hasattr(order, 'id')
    assert hasattr(order, 'status')
    assert hasattr(order, 'links')
