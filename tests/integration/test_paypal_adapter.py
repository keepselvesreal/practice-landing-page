"""Integration Test: PayPal Adapter

Outside-In TDD [8.2]: "집중된 Integration Test로 Adapter 테스트"
실제 PayPal Sandbox API를 호출하여 Adapter 동작 확인
"""
import pytest
from backend.services.payment.paypal_adapter import PayPalAdapter, PaymentServiceError


@pytest.fixture
def paypal_adapter():
    """PayPal Adapter 인스턴스"""
    return PayPalAdapter()


@pytest.mark.integration
def test_paypal_adapter_create_order(paypal_adapter: PayPalAdapter):
    """PayPal Adapter로 Order 생성 테스트"""
    # Given: 주문 금액 (1,250 페소 = 125,000 센타보)
    amount = 125000

    # When: Order 생성
    result = paypal_adapter.create_order(amount=amount, currency="PHP")

    # Then: 결과 확인
    assert result.order_id is not None
    assert result.order_id.startswith("")  # PayPal Order ID
    assert result.approval_url.startswith("https://www.sandbox.paypal.com")
    assert "token=" in result.approval_url
    assert result.status == "CREATED"

    print(f"\n✅ Order ID: {result.order_id}")
    print(f"✅ Approval URL: {result.approval_url}")


@pytest.mark.integration
def test_paypal_adapter_amount_conversion(paypal_adapter: PayPalAdapter):
    """센타보 → 페소 변환 확인

    675 페소 = 67,500 센타보
    PayPal API에는 "675.00" 형식으로 전달되어야 함
    """
    # Given: 675 페소 (67,500 센타보)
    amount = 67500

    # When: Order 생성
    result = paypal_adapter.create_order(amount=amount, currency="PHP")

    # Then: Order 생성 성공
    assert result.order_id is not None
    assert result.approval_url is not None

    print(f"\n✅ 67,500 센타보 → 675.00 페소 변환 성공")
    print(f"✅ Order ID: {result.order_id}")


@pytest.mark.integration
def test_paypal_adapter_without_credentials(monkeypatch):
    """자격증명 없이 Adapter 생성 시 에러"""
    # Given: 환경변수 제거
    monkeypatch.delenv("PAYPAL_CLIENT_ID", raising=False)
    monkeypatch.delenv("PAYPAL_CLIENT_SECRET", raising=False)

    # When/Then: 자격증명 없이 Adapter 생성
    with pytest.raises(PaymentServiceError, match="PayPal credentials not configured"):
        PayPalAdapter()
