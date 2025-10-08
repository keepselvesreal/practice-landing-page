"""
Affiliate 엔티티 - 어필리에이트 도메인 모델
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

from .order import Money


@dataclass(frozen=True)
class AffiliateId:
    """어필리에이트 ID 값 객체"""
    value: int


@dataclass
class Affiliate:
    """
    어필리에이트 엔티티

    인플루언서의 추천 활동을 추적하고 수수료를 관리
    """
    id: Optional[AffiliateId]
    code: str  # 고유 추천 코드
    total_clicks: int
    total_sales: int
    total_commission: Money
    pending_commission: Money
    created_at: datetime

    @classmethod
    def create_new(cls, code: str) -> 'Affiliate':
        """
        새 어필리에이트 생성

        Args:
            code: 고유 추천 코드

        Returns:
            초기화된 Affiliate 인스턴스
        """
        return cls(
            id=None,
            code=code,
            total_clicks=0,
            total_sales=0,
            total_commission=Money.of(Decimal('0')),
            pending_commission=Money.of(Decimal('0')),
            created_at=datetime.now()
        )

    def record_click(self) -> 'Affiliate':
        """
        클릭 기록

        링크 클릭 시 카운터 증가
        """
        return Affiliate(
            id=self.id,
            code=self.code,
            total_clicks=self.total_clicks + 1,
            total_sales=self.total_sales,
            total_commission=self.total_commission,
            pending_commission=self.pending_commission,
            created_at=self.created_at
        )

    def record_sale(self, commission: Money) -> 'Affiliate':
        """
        판매 및 수수료 기록

        Args:
            commission: 이번 판매의 수수료

        Returns:
            업데이트된 Affiliate 인스턴스
        """
        return Affiliate(
            id=self.id,
            code=self.code,
            total_clicks=self.total_clicks,
            total_sales=self.total_sales + 1,
            total_commission=Money.of(
                self.total_commission.amount + commission.amount
            ),
            pending_commission=Money.of(
                self.pending_commission.amount + commission.amount
            ),
            created_at=self.created_at
        )

    def clear_pending_commission(self) -> 'Affiliate':
        """
        대기 중인 수수료 정산 완료

        수수료 지급 후 pending_commission을 0으로 초기화
        """
        return Affiliate(
            id=self.id,
            code=self.code,
            total_clicks=self.total_clicks,
            total_sales=self.total_sales,
            total_commission=self.total_commission,
            pending_commission=Money.of(Decimal('0')),
            created_at=self.created_at
        )
