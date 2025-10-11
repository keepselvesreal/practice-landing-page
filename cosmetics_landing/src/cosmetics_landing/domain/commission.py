"""
Commission 값 객체 - 수수료 계산 로직 캡슐화
"""
from dataclasses import dataclass
from decimal import Decimal

from .order import Money


@dataclass(frozen=True)
class Commission:
    """
    수수료 계산 로직을 캡슐화한 값 객체

    비즈니스 규칙: 20% 수수료
    """
    rate: Decimal = Decimal('0.20')  # 20%

    def __post_init__(self):
        if not (Decimal('0') <= self.rate <= Decimal('1')):
            raise ValueError("Commission rate must be between 0 and 1")

    def calculate(self, order_amount: Money) -> Money:
        """
        주문 금액에서 수수료 계산

        Args:
            order_amount: 주문 금액

        Returns:
            계산된 수수료 (소수점 둘째 자리까지 반올림)
        """
        commission_amount = order_amount.amount * self.rate
        # 소수점 둘째 자리까지 반올림 (ROUND_HALF_UP)
        rounded_amount = commission_amount.quantize(Decimal('0.01'))
        return Money.of(rounded_amount)

    def __str__(self):
        return f"{self.rate * 100:.0f}%"
