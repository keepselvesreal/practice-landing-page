"""
Order 엔티티 단위 테스트
"""
import pytest
from decimal import Decimal
from datetime import datetime

from cosmetics_landing.domain.order import Order, Money, OrderId


class TestMoney:
    """Money 값 객체 테스트"""

    def test_creates_money_with_valid_amount(self):
        """유효한 금액으로 Money 생성"""
        money = Money.of(Decimal("29.99"))
        assert money.amount == Decimal("29.99")

    def test_rejects_negative_amount(self):
        """음수 금액은 거부"""
        with pytest.raises(ValueError, match="Amount must be positive"):
            Money(amount=Decimal("-10.00"))

    def test_money_is_immutable(self):
        """Money는 불변 객체"""
        money = Money.of(Decimal("10.00"))
        with pytest.raises(Exception):  # dataclass frozen
            money.amount = Decimal("20.00")


class TestOrder:
    """Order 엔티티 테스트"""

    def test_creates_new_order_with_pending_status(self):
        """새 주문은 pending 상태로 생성"""
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St, Manila",
            product_price=Money.of(Decimal("29.99"))
        )

        assert order.customer_email == "test@example.com"
        assert order.customer_address == "123 Main St, Manila"
        assert order.product_price.amount == Decimal("29.99")
        assert order.payment_status == "pending"
        assert order.id is None
        assert order.affiliate_code is None
        assert isinstance(order.created_at, datetime)

    def test_creates_order_with_affiliate_code(self):
        """어필리에이트 코드와 함께 주문 생성"""
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Money.of(Decimal("29.99")),
            affiliate_code="INFLUENCER123"
        )

        assert order.affiliate_code == "INFLUENCER123"
        assert order.has_affiliate()

    def test_marks_order_as_paid(self):
        """주문을 결제 완료 상태로 변경"""
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Money.of(Decimal("29.99"))
        )

        paid_order = order.mark_as_paid()

        assert paid_order.payment_status == "completed"
        assert paid_order.is_paid()
        # 원본은 변경되지 않음 (불변성)
        assert order.payment_status == "pending"

    def test_marks_order_as_failed(self):
        """주문을 결제 실패 상태로 변경"""
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Money.of(Decimal("29.99"))
        )

        failed_order = order.mark_as_failed()

        assert failed_order.payment_status == "failed"
        assert not failed_order.is_paid()

    def test_has_affiliate_returns_false_when_no_code(self):
        """어필리에이트 코드가 없으면 False 반환"""
        order = Order.create_new(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Money.of(Decimal("29.99"))
        )

        assert not order.has_affiliate()
