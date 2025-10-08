"""
Commission 값 객체 단위 테스트
"""
import pytest
from decimal import Decimal

from cosmetics_landing.domain.commission import Commission
from cosmetics_landing.domain.order import Money


class TestCommission:
    """Commission 값 객체 테스트"""

    def test_calculates_20_percent_commission(self):
        """수수료는 주문 금액의 20%"""
        commission = Commission()
        order_amount = Money.of(Decimal("100.00"))

        result = commission.calculate(order_amount)

        assert result.amount == Decimal("20.00")

    def test_calculates_commission_for_product_price(self):
        """실제 제품 가격($29.99)의 수수료 계산"""
        commission = Commission()
        product_price = Money.of(Decimal("29.99"))

        result = commission.calculate(product_price)

        # 29.99 * 0.20 = 5.998
        assert result.amount == Decimal("5.998")

    def test_rejects_invalid_commission_rate(self):
        """잘못된 수수료율 거부 (0~1 범위 밖)"""
        with pytest.raises(ValueError, match="Commission rate must be between 0 and 1"):
            Commission(rate=Decimal("1.5"))

        with pytest.raises(ValueError, match="Commission rate must be between 0 and 1"):
            Commission(rate=Decimal("-0.1"))

    def test_accepts_custom_commission_rate(self):
        """커스텀 수수료율 허용"""
        commission = Commission(rate=Decimal("0.15"))  # 15%
        order_amount = Money.of(Decimal("100.00"))

        result = commission.calculate(order_amount)

        assert result.amount == Decimal("15.00")

    def test_commission_is_immutable(self):
        """Commission은 불변 객체"""
        commission = Commission()
        with pytest.raises(Exception):  # dataclass frozen
            commission.rate = Decimal("0.30")
