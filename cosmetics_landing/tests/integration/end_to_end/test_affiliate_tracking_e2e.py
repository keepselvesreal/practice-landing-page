"""
Epic 2 인수 테스트: 어필리에이트 추적 전체 흐름
GOOS 4-5장: Outside-in, 사용자 관점 시나리오
"""
import pytest
from fastapi import status


@pytest.mark.e2e
class TestAffiliateTrackingE2E:
    """어필리에이트 추적 E2E 테스트"""

    def test_affiliate_earns_commission_on_sale(self, client):
        """
        인수 테스트: 어필리에이트 링크로 유입된 고객이 주문하면 커미션이 기록된다

        사용자 여정:
        1. 인플루언서가 어필리에이트 링크 공유 (예: ?ref=INFLUENCER123)
        2. 고객이 해당 링크로 랜딩 페이지 방문 → 클릭 카운트 증가
        3. 고객이 주문 완료 → 어필리에이트 판매 및 커미션 기록
        4. 어필리에이트 대시보드에서 실적 확인
        """
        # Given: 어필리에이트 링크로 방문 (클릭 추적)
        response = client.get("/?ref=INFLUENCER123")
        assert response.status_code == status.HTTP_200_OK

        # When: 고객이 주문
        order_request = {
            "customer_email": "customer@example.com",
            "customer_address": "123 Main St, Seoul",
            "product_price": 100.00,
            "affiliate_code": "INFLUENCER123"
        }
        order_response = client.post("/api/orders", json=order_request)
        assert order_response.status_code == status.HTTP_201_CREATED

        # Then: 어필리에이트 실적 확인
        stats_response = client.get("/api/affiliates/INFLUENCER123/stats")
        assert stats_response.status_code == status.HTTP_200_OK

        stats = stats_response.json()
        assert stats["total_clicks"] == 1
        assert stats["total_sales"] == 1
        assert stats["total_commission"] == 20.00  # 100 * 20%
        assert stats["pending_commission"] == 20.00

    def test_multiple_sales_accumulate_commission(self, client):
        """여러 판매 시 커미션이 누적된다"""
        # Given: 어필리에이트 링크로 방문
        client.get("/?ref=PARTNER999")

        # When: 두 번의 주문
        order1 = {
            "customer_email": "customer1@example.com",
            "customer_address": "Address 1",
            "product_price": 50.00,
            "affiliate_code": "PARTNER999"
        }
        order2 = {
            "customer_email": "customer2@example.com",
            "customer_address": "Address 2",
            "product_price": 150.00,
            "affiliate_code": "PARTNER999"
        }

        client.post("/api/orders", json=order1)
        client.post("/api/orders", json=order2)

        # Then: 커미션 누적 확인
        stats_response = client.get("/api/affiliates/PARTNER999/stats")
        stats = stats_response.json()

        assert stats["total_sales"] == 2
        assert stats["total_commission"] == 40.00  # (50 + 150) * 20%

    def test_order_without_affiliate_code_is_processed(self, client):
        """어필리에이트 코드 없는 주문도 정상 처리된다"""
        # When: 어필리에이트 코드 없이 주문
        order_request = {
            "customer_email": "customer@example.com",
            "customer_address": "123 Main St",
            "product_price": 50.00
            # affiliate_code 없음
        }
        order_response = client.post("/api/orders", json=order_request)

        # Then: 주문은 성공
        assert order_response.status_code == status.HTTP_201_CREATED
