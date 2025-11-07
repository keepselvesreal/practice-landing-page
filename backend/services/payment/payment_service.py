"""결제 서비스 인터페이스

애플리케이션 도메인 용어로 정의된 결제 서비스 추상화
Third-party 결제 서비스 (PayPal 등)의 세부사항을 숨김
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CreateOrderResult:
    """주문 생성 결과"""

    order_id: str  # PayPal Order ID
    approval_url: str  # 사용자가 결제를 승인할 URL
    status: str  # 주문 상태


class PaymentService(ABC):
    """결제 서비스 인터페이스

    애플리케이션 관점에서 필요한 결제 기능만 노출
    """

    @abstractmethod
    def create_order(self, amount: int, currency: str = "PHP") -> CreateOrderResult:
        """결제 주문 생성

        Args:
            amount: 결제 금액 (센타보 단위)
            currency: 통화 코드 (기본값: PHP)

        Returns:
            CreateOrderResult: 주문 ID, approval URL 등

        Raises:
            PaymentServiceError: 결제 서비스 오류
        """
        pass

    @abstractmethod
    def capture_order(self, order_id: str) -> dict:
        """결제 확정 (Capture)

        Args:
            order_id: PayPal Order ID

        Returns:
            dict: 결제 결과 정보

        Raises:
            PaymentServiceError: 결제 실패
        """
        pass


class PaymentServiceError(Exception):
    """결제 서비스 오류"""

    pass
