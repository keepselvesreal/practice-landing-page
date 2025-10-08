"""
Address Validator Port - Outgoing Port
주소 검증 외부 서비스 인터페이스
"""
from abc import ABC, abstractmethod


class ValidateAddressPort(ABC):
    """
    주소 검증 포트

    Google Places API 등 구체적인 구현은 Adapter 계층에서
    """

    @abstractmethod
    def is_valid(self, address: str) -> bool:
        """
        주소 유효성 검증

        Args:
            address: 검증할 주소

        Returns:
            유효하면 True, 아니면 False
        """
        pass
