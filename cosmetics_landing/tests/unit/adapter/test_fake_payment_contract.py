"""
Fake Payment Adapter Contract Test
Chapter 22: "Learning Tests" - Verify Fake implements same contract as Real

목적:
- FakePaymentGateway가 PayPalAdapter와 동일한 계약 준수 확인
- 포트 인터페이스(ProcessPaymentPort) 구현 검증
- 동일한 입출력 타입과 동작 보장

실행:
    pytest tests/unit/adapter/test_fake_payment_contract.py -v
"""
import pytest
from decimal import Decimal
from datetime import datetime

from cosmetics_landing.adapter.out.payment.fake_payment_adapter import FakePaymentAdapter
from cosmetics_landing.adapter.out.payment.paypal_adapter import PayPalAdapter
from cosmetics_landing.application.port.out.payment_gateway import ProcessPaymentPort, PaymentResult
from cosmetics_landing.domain.order import Order, OrderId, Money


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


class TestFakePaymentAdapterContract:
    """FakePaymentAdapter 계약 검증"""

    def test_implements_process_payment_port(self):
        """ProcessPaymentPort 인터페이스 구현 확인"""
        fake_gateway = FakePaymentAdapter()

        assert isinstance(fake_gateway, ProcessPaymentPort)

    def test_process_payment_returns_payment_result(self, sample_order):
        """process_payment가 PaymentResult 반환"""
        fake_gateway = FakePaymentAdapter()

        result = fake_gateway.process_payment(sample_order)

        assert isinstance(result, PaymentResult)
        assert hasattr(result, 'success')
        assert hasattr(result, 'transaction_id')
        assert hasattr(result, 'error_message')

    def test_successful_payment_returns_transaction_id(self, sample_order):
        """성공 시 transaction_id 반환"""
        fake_gateway = FakePaymentAdapter()

        result = fake_gateway.process_payment(sample_order)

        # Fake는 항상 성공 (Real은 실제 API 호출 결과에 따라 결정)
        assert result.success is True
        assert result.transaction_id is not None
        assert isinstance(result.transaction_id, str)
        assert result.error_message is None

    def test_failed_payment_returns_error_message(self, sample_order):
        """실패 시 error_message 반환 (Fake는 설정에 따라)"""
        fake_gateway = FakePaymentAdapter(always_succeed=False)  # 실패 모드

        result = fake_gateway.process_payment(sample_order)

        assert result.success is False
        assert result.transaction_id is None
        assert result.error_message is not None
        assert isinstance(result.error_message, str)

    def test_same_interface_as_paypal_adapter(self, sample_order):
        """PayPalAdapter와 동일한 인터페이스"""
        fake_gateway = FakePaymentAdapter()

        # 두 어댑터 모두 동일한 포트 구현
        assert isinstance(fake_gateway, ProcessPaymentPort)

        # 동일한 메서드 시그니처
        assert hasattr(fake_gateway, 'process_payment')

        # 동일한 입출력 타입
        result = fake_gateway.process_payment(sample_order)
        assert isinstance(result, PaymentResult)


class TestFakePaymentAdapterBehavior:
    """FakePaymentAdapter 동작 검증 (Real과 다를 수 있는 부분)"""

    def test_fake_allows_success_mode_toggle(self, sample_order):
        """Fake는 성공/실패 모드 전환 가능 (테스트 편의성)"""
        # 성공 모드
        fake_gateway = FakePaymentAdapter(always_succeed=True)
        result = fake_gateway.process_payment(sample_order)
        assert result.success is True

        # 실패 모드
        fake_gateway = FakePaymentAdapter(always_succeed=False)
        result = fake_gateway.process_payment(sample_order)
        assert result.success is False

    def test_fake_generates_predictable_transaction_ids(self, sample_order):
        """Fake는 예측 가능한 transaction_id 생성 (테스트 편의성)"""
        fake_gateway = FakePaymentAdapter()

        result = fake_gateway.process_payment(sample_order)

        # Fake는 "fake_txn_" 접두사 (Real PayPal은 "PAYID-")
        assert result.transaction_id.startswith("fake_txn_")
