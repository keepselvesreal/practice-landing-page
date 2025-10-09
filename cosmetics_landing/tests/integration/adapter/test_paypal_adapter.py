"""
PayPal Adapter Integration Test
Chapter 8: "Mapping Between Boundaries" - Third-Party Integration

목적:
- 실제 PayPal Sandbox로 어댑터 동작 검증
- Learning Test에서 학습한 계약 준수 확인
- 에러 처리 검증

실행:
    pytest tests/integration/adapter/test_paypal_adapter.py -v -m integration
"""
import pytest
import os
from decimal import Decimal
from datetime import datetime

from cosmetics_landing.adapter.out.payment.paypal_adapter import PayPalAdapter
from cosmetics_landing.domain.order import Order, OrderId, Money


@pytest.fixture(scope="module")
def paypal_adapter():
    """PayPal 어댑터 픽스처"""
    client_id = os.getenv("PAYPAL_SANDBOX_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_SANDBOX_CLIENT_SECRET")

    if not client_id or not client_secret:
        pytest.skip("PayPal credentials not configured")

    return PayPalAdapter(
        client_id=client_id,
        client_secret=client_secret,
        mode="sandbox"
    )


@pytest.fixture
def sample_order():
    """테스트용 주문"""
    return Order(
        id=OrderId(value=1),
        customer_email="test@example.com",
        customer_address="123 Main St, Manila, Philippines",
        product_price=Money.of(Decimal("29.99")),
        affiliate_code=None,
        created_at=datetime.now(),
        payment_status="pending"
    )


@pytest.mark.integration
class TestPayPalAdapterIntegration:
    """PayPal 어댑터 통합 테스트"""

    def test_processes_payment_successfully(self, paypal_adapter, sample_order):
        """
        실제 PayPal Sandbox로 결제 처리 성공

        검증:
        - result.success == True
        - transaction_id 존재 (PAYID- 접두사)
        - error_message == None
        """
        # When: 결제 처리
        result = paypal_adapter.process_payment(sample_order)

        # Then: 성공
        assert result.success is True, f"Payment failed: {result.error_message}"
        assert result.transaction_id is not None
        assert result.transaction_id.startswith("PAYID-")
        assert result.error_message is None

        print(f"\n✅ Payment processed: {result.transaction_id}")

    def test_processes_different_amounts(self, paypal_adapter):
        """다양한 금액으로 결제 처리"""
        test_amounts = [Decimal("1.00"), Decimal("10.99"), Decimal("100.00")]

        for amount in test_amounts:
            # Given
            order = Order(
                id=OrderId(value=1),
                customer_email="test@example.com",
                customer_address="123 Main St",
                product_price=Money.of(amount),
                affiliate_code=None,
                created_at=datetime.now(),
                payment_status="pending"
            )

            # When
            result = paypal_adapter.process_payment(order)

            # Then
            assert result.success is True
            print(f"✅ Amount ${amount}: {result.transaction_id}")

    def test_handles_network_issues_gracefully(self, sample_order):
        """네트워크 문제 시 적절히 처리"""
        # Given: 잘못된 credentials
        bad_adapter = PayPalAdapter(
            client_id="INVALID",
            client_secret="INVALID",
            mode="sandbox"
        )

        # When/Then: PayPal SDK가 예외를 발생시킴
        # 어댑터는 이를 PaymentResult로 변환해야 함
        try:
            result = bad_adapter.process_payment(sample_order)
            # PaymentResult로 변환되면 성공
            assert result.success is False
            assert result.transaction_id is None
            assert result.error_message is not None
            print(f"\n✅ Error handled: {result.error_message}")
        except Exception as e:
            # 예외가 발생하면 테스트 실패
            pytest.fail(f"Adapter should handle errors gracefully, but raised: {e}")

    def test_returns_approval_url(self, sample_order):
        """결제 생성 후 approval_url 조회 가능"""
        # Given: 새로운 어댑터 인스턴스 생성 (테스트 격리)
        client_id = os.getenv("PAYPAL_SANDBOX_CLIENT_ID")
        client_secret = os.getenv("PAYPAL_SANDBOX_CLIENT_SECRET")

        if not client_id or not client_secret:
            pytest.skip("PayPal credentials not configured")

        adapter = PayPalAdapter(
            client_id=client_id,
            client_secret=client_secret,
            mode="sandbox"
        )

        # Given: 결제 생성
        result = adapter.process_payment(sample_order)
        assert result.success is True

        # When: approval_url 조회
        approval_url = adapter.get_approval_url(result.transaction_id)

        # Then: URL 존재
        assert approval_url is not None
        assert "paypal.com" in approval_url

        print(f"\n✅ Approval URL: {approval_url[:60]}...")


@pytest.mark.integration
class TestPayPalAdapterPortCompliance:
    """PayPal 어댑터의 포트 인터페이스 준수 검증"""

    def test_implements_process_payment_port(self, paypal_adapter):
        """ProcessPaymentPort 인터페이스 구현 확인"""
        from cosmetics_landing.application.port.out.payment_gateway import ProcessPaymentPort

        assert isinstance(paypal_adapter, ProcessPaymentPort)

    def test_returns_payment_result_type(self, paypal_adapter, sample_order):
        """PaymentResult 타입 반환 확인"""
        from cosmetics_landing.application.port.out.payment_gateway import PaymentResult

        result = paypal_adapter.process_payment(sample_order)

        assert isinstance(result, PaymentResult)
        assert hasattr(result, 'success')
        assert hasattr(result, 'transaction_id')
        assert hasattr(result, 'error_message')
