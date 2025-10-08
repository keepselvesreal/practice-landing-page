"""
Order 엔티티 - 주문 도메인 모델
Chapter 4 기반: 비즈니스 규칙 캡슐화
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal


@dataclass(frozen=True)
class OrderId:
    """주문 ID 값 객체"""
    value: int


@dataclass(frozen=True)
class Money:
    """금액 값 객체 - 비즈니스 규칙 검증"""
    amount: Decimal

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount must be positive")

    @classmethod
    def of(cls, amount: Decimal) -> 'Money':
        """팩토리 메서드"""
        return cls(amount=amount)

    def __str__(self):
        return f"${self.amount:.2f}"


@dataclass
class Order:
    """
    주문 엔티티 - 비즈니스 규칙 캡슐화

    불변성을 유지하기 위해 상태 변경 시 새 인스턴스 반환
    """
    id: Optional[OrderId]
    customer_email: str
    customer_address: str
    product_price: Money
    affiliate_code: Optional[str]
    created_at: datetime
    payment_status: str  # 'pending', 'completed', 'failed'

    @classmethod
    def create_new(
        cls,
        customer_email: str,
        customer_address: str,
        product_price: Money,
        affiliate_code: Optional[str] = None
    ) -> 'Order':
        """
        새 주문 생성 팩토리 메서드

        Args:
            customer_email: 고객 이메일
            customer_address: 배송 주소
            product_price: 제품 가격
            affiliate_code: 어필리에이트 코드 (선택)

        Returns:
            새로운 Order 인스턴스 (ID 없음, pending 상태)
        """
        return cls(
            id=None,
            customer_email=customer_email,
            customer_address=customer_address,
            product_price=product_price,
            affiliate_code=affiliate_code,
            created_at=datetime.now(),
            payment_status='pending'
        )

    def mark_as_paid(self) -> 'Order':
        """
        결제 완료 처리

        불변 객체이므로 새 인스턴스 반환
        """
        return Order(
            id=self.id,
            customer_email=self.customer_email,
            customer_address=self.customer_address,
            product_price=self.product_price,
            affiliate_code=self.affiliate_code,
            created_at=self.created_at,
            payment_status='completed'
        )

    def mark_as_failed(self) -> 'Order':
        """결제 실패 처리"""
        return Order(
            id=self.id,
            customer_email=self.customer_email,
            customer_address=self.customer_address,
            product_price=self.product_price,
            affiliate_code=self.affiliate_code,
            created_at=self.created_at,
            payment_status='failed'
        )

    def is_paid(self) -> bool:
        """결제 완료 여부 확인"""
        return self.payment_status == 'completed'

    def has_affiliate(self) -> bool:
        """어필리에이트 코드 존재 여부"""
        return self.affiliate_code is not None
