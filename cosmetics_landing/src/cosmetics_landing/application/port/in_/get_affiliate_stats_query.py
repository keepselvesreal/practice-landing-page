"""
Get Affiliate Stats Query - Incoming Port (Query)
CQS 원칙: 조회만 담당, 상태 변경 없음

Chapter 4, Lines 576-625: Query Service 패턴
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class AffiliateStats:
    """
    어필리에이트 통계 - Query 전용 Output Model

    Chapter 4, Lines 548-575: Use Case 전용 Output Model
    """
    code: str
    total_clicks: int
    total_sales: int
    total_commission: Decimal
    pending_commission: Decimal


class GetAffiliateStatsQuery(ABC):
    """
    어필리에이트 통계 조회 Query (Query)

    CQS 원칙: 상태를 변경하지 않고 데이터만 반환
    """

    @abstractmethod
    def get_stats(self, affiliate_code: str) -> AffiliateStats:
        """
        어필리에이트 통계 조회

        Args:
            affiliate_code: 어필리에이트 코드

        Returns:
            통계 데이터

        Raises:
            ValueError: 존재하지 않는 코드
        """
        pass
