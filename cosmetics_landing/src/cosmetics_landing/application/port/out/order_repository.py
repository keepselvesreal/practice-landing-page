"""
Order Repository Ports - Outgoing Ports
Chapter 6: 포트 인터페이스 슬라이싱 (Interface Segregation)
"""
from abc import ABC, abstractmethod
from typing import Optional

from ....domain.order import Order, OrderId


class SaveOrderPort(ABC):
    """
    주문 저장 포트 - 단일 책임

    Chapter 6, Lines 67-104: 포트를 작은 단위로 분리
    """

    @abstractmethod
    def save(self, order: Order) -> OrderId:
        """
        주문 저장

        Args:
            order: 저장할 주문 엔티티

        Returns:
            저장된 주문의 ID
        """
        pass


class LoadOrderPort(ABC):
    """
    주문 조회 포트 - 단일 책임
    """

    @abstractmethod
    def load_by_id(self, order_id: OrderId) -> Optional[Order]:
        """
        ID로 주문 조회

        Args:
            order_id: 주문 ID

        Returns:
            주문 엔티티 또는 None
        """
        pass

    @abstractmethod
    def load_by_affiliate_code(self, affiliate_code: str) -> list[Order]:
        """
        어필리에이트 코드로 주문 목록 조회

        Args:
            affiliate_code: 어필리에이트 코드

        Returns:
            주문 엔티티 리스트
        """
        pass
