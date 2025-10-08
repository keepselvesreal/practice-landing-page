"""
Affiliate Repository Ports - Outgoing Ports
Chapter 6: 포트 인터페이스 슬라이싱 (Interface Segregation)
"""
from abc import ABC, abstractmethod
from typing import Optional

from ....domain.affiliate import Affiliate, AffiliateId


class SaveAffiliatePort(ABC):
    """어필리에이트 저장 포트 - 단일 책임"""

    @abstractmethod
    def save(self, affiliate: Affiliate) -> AffiliateId:
        """
        어필리에이트 저장

        Args:
            affiliate: 저장할 어필리에이트 엔티티

        Returns:
            저장된 어필리에이트의 ID
        """
        pass


class LoadAffiliatePort(ABC):
    """어필리에이트 조회 포트 - 단일 책임"""

    @abstractmethod
    def load_by_id(self, affiliate_id: AffiliateId) -> Optional[Affiliate]:
        """
        ID로 어필리에이트 조회

        Args:
            affiliate_id: 어필리에이트 ID

        Returns:
            어필리에이트 엔티티 또는 None
        """
        pass

    @abstractmethod
    def load_by_code(self, code: str) -> Optional[Affiliate]:
        """
        코드로 어필리에이트 조회

        Args:
            code: 어필리에이트 코드

        Returns:
            어필리에이트 엔티티 또는 None
        """
        pass
