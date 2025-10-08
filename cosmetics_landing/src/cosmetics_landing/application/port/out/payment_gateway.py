"""
Payment Gateway Ports - Outgoing Ports
외부 결제 시스템과의 통신 인터페이스
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from ....domain.order import Order


@dataclass(frozen=True)
class PaymentResult:
    """결제 처리 결과"""
    success: bool
    transaction_id: Optional[str]
    error_message: Optional[str]


class ProcessPaymentPort(ABC):
    """
    결제 처리 포트

    PayPal, Stripe 등 구체적인 구현은 Adapter 계층에서
    """

    @abstractmethod
    def process_payment(self, order: Order) -> PaymentResult:
        """
        주문에 대한 결제 처리

        Args:
            order: 결제할 주문

        Returns:
            결제 결과
        """
        pass
