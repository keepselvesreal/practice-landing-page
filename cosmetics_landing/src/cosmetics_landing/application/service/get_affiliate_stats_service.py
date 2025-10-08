"""
Get Affiliate Stats Service - Query Use Case 구현
Chapter 4, Lines 576-625: Query Service 패턴
"""
from ..port.in_.get_affiliate_stats_query import GetAffiliateStatsQuery, AffiliateStats
from ..port.out.affiliate_repository import LoadAffiliatePort


class GetAffiliateStatsService(GetAffiliateStatsQuery):
    """
    어필리에이트 통계 조회 서비스 (Query)

    CQS 원칙: 상태를 변경하지 않고 데이터만 반환
    """

    def __init__(self, load_affiliate_port: LoadAffiliatePort):
        self.load_affiliate = load_affiliate_port

    def get_stats(self, affiliate_code: str) -> AffiliateStats:
        """통계 조회"""
        affiliate = self.load_affiliate.load_by_code(affiliate_code)

        if not affiliate:
            raise ValueError(f"Affiliate not found: {affiliate_code}")

        return AffiliateStats(
            code=affiliate.code,
            total_clicks=affiliate.total_clicks,
            total_sales=affiliate.total_sales,
            total_commission=affiliate.total_commission.amount,
            pending_commission=affiliate.pending_commission.amount
        )
