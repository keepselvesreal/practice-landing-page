"""
Affiliate 엔티티 단위 테스트
"""
from decimal import Decimal

from cosmetics_landing.domain.affiliate import Affiliate
from cosmetics_landing.domain.order import Money


class TestAffiliate:
    """Affiliate 엔티티 테스트"""

    def test_creates_new_affiliate(self):
        """새 어필리에이트 생성"""
        affiliate = Affiliate.create_new(code="INFLUENCER123")

        assert affiliate.code == "INFLUENCER123"
        assert affiliate.total_clicks == 0
        assert affiliate.total_sales == 0
        assert affiliate.total_commission.amount == Decimal("0")
        assert affiliate.pending_commission.amount == Decimal("0")
        assert affiliate.id is None

    def test_records_click(self):
        """클릭 기록"""
        affiliate = Affiliate.create_new(code="INFLUENCER123")

        updated = affiliate.record_click()

        assert updated.total_clicks == 1
        # 원본은 변경되지 않음
        assert affiliate.total_clicks == 0

    def test_records_multiple_clicks(self):
        """여러 클릭 기록"""
        affiliate = Affiliate.create_new(code="INFLUENCER123")

        affiliate = affiliate.record_click()
        affiliate = affiliate.record_click()
        affiliate = affiliate.record_click()

        assert affiliate.total_clicks == 3

    def test_records_sale_with_commission(self):
        """판매와 수수료 기록"""
        affiliate = Affiliate.create_new(code="INFLUENCER123")
        commission = Money.of(Decimal("5.00"))

        updated = affiliate.record_sale(commission)

        assert updated.total_sales == 1
        assert updated.total_commission.amount == Decimal("5.00")
        assert updated.pending_commission.amount == Decimal("5.00")

    def test_records_multiple_sales(self):
        """여러 판매 기록"""
        affiliate = Affiliate.create_new(code="INFLUENCER123")

        affiliate = affiliate.record_sale(Money.of(Decimal("5.00")))
        affiliate = affiliate.record_sale(Money.of(Decimal("6.00")))

        assert affiliate.total_sales == 2
        assert affiliate.total_commission.amount == Decimal("11.00")
        assert affiliate.pending_commission.amount == Decimal("11.00")

    def test_clears_pending_commission(self):
        """대기 중인 수수료 정산"""
        affiliate = Affiliate.create_new(code="INFLUENCER123")
        affiliate = affiliate.record_sale(Money.of(Decimal("5.00")))

        cleared = affiliate.clear_pending_commission()

        assert cleared.pending_commission.amount == Decimal("0")
        assert cleared.total_commission.amount == Decimal("5.00")  # 총 수수료는 유지
