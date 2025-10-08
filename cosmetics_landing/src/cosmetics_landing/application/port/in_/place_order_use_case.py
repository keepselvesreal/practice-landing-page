"""
Place Order Use Case - Incoming Port
Chapter 4: Use Case 인터페이스와 Self-Validating Command
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

from ....domain.order import OrderId


@dataclass(frozen=True)
class PlaceOrderCommand:
    """
    주문 생성 명령 - Self-Validating Command

    Chapter 4, Lines 274-363: 입력 검증을 생성자에서 수행
    """
    customer_email: str
    customer_address: str
    product_price: Decimal
    affiliate_code: Optional[str] = None

    def __post_init__(self):
        """입력 검증 (Self-Validating)"""
        if not self.customer_email or not self.customer_email.strip():
            raise ValueError("customer_email is required")

        if '@' not in self.customer_email:
            raise ValueError("customer_email must be valid email address")

        if not self.customer_address or not self.customer_address.strip():
            raise ValueError("customer_address is required")

        if self.product_price <= 0:
            raise ValueError("product_price must be positive")


class PlaceOrderUseCase(ABC):
    """
    주문 생성 Use Case 인터페이스 (Incoming Port)

    애플리케이션의 진입점을 명확히 정의
    """

    @abstractmethod
    def place_order(self, command: PlaceOrderCommand) -> OrderId:
        """
        주문 생성 및 결제 처리

        Args:
            command: 주문 생성 명령

        Returns:
            생성된 주문 ID

        Raises:
            ValueError: 입력 검증 실패 또는 비즈니스 규칙 위반
            PaymentFailedError: 결제 실패
        """
        pass
