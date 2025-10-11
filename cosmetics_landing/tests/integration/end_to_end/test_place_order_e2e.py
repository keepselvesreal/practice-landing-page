"""
Place Order E2E Test
Chapter 4, 5: Walking Skeleton 전체 흐름 검증

주문 생성 → 주소 검증 → 결제 처리 → 주문 완료
"""
import pytest
from fastapi import status


class TestPlaceOrderE2E:
    """
    주문 생성 E2E 테스트

    Walking Skeleton: 전체 계층을 관통하는 최소 기능 검증
    """

    def test_customer_can_place_order_successfully(self, client, valid_order_data):
        """
        고객이 주문을 생성하고 결제할 수 있다

        Given: 유효한 주문 정보
        When: 주문 생성 API 호출
        Then: 주문이 성공적으로 생성됨
        """
        # When
        response = client.post("/api/orders", json=valid_order_data)

        # Then
        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()
        assert "order_id" in data
        assert data["order_id"] > 0
        assert data["status"] == "success"
        assert "successfully" in data["message"].lower()

    def test_rejects_invalid_email(self, client, valid_order_data):
        """잘못된 이메일은 거부된다"""
        # Given
        invalid_data = {**valid_order_data, "customer_email": "invalid-email"}

        # When
        response = client.post("/api/orders", json=invalid_data)

        # Then
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_rejects_short_address(self, client, valid_order_data):
        """너무 짧은 주소는 거부된다"""
        # Given
        invalid_data = {**valid_order_data, "customer_address": "abc"}

        # When
        response = client.post("/api/orders", json=invalid_data)

        # Then
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_rejects_invalid_address_pattern(self, client, valid_order_data):
        """
        유효하지 않은 주소 패턴은 거부된다

        Business Rule Validation: FakeAddressValidator가 "invalid" 패턴 거부
        """
        # Given
        invalid_data = {
            **valid_order_data,
            "customer_address": "This is an invalid address"
        }

        # When
        response = client.post("/api/orders", json=invalid_data)

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "address" in response.json()["detail"].lower()

    def test_rejects_negative_price(self, client, valid_order_data):
        """음수 가격은 거부된다"""
        # Given
        invalid_data = {**valid_order_data, "product_price": -10.00}

        # When
        response = client.post("/api/orders", json=invalid_data)

        # Then
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_order_with_affiliate_code(self, client, order_with_affiliate):
        """
        어필리에이트 코드와 함께 주문할 수 있다

        Walking Skeleton: 어필리에이트 기능 통합
        """
        # When
        response = client.post("/api/orders", json=order_with_affiliate)

        # Then
        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()
        assert data["status"] == "success"

    def test_multiple_orders_get_unique_ids(self, client, valid_order_data):
        """여러 주문이 고유한 ID를 받는다"""
        # When: 두 개의 주문 생성
        response1 = client.post("/api/orders", json=valid_order_data)
        response2 = client.post("/api/orders", json=valid_order_data)

        # Then
        assert response1.status_code == status.HTTP_201_CREATED
        assert response2.status_code == status.HTTP_201_CREATED

        order_id1 = response1.json()["order_id"]
        order_id2 = response2.json()["order_id"]

        assert order_id1 != order_id2
        assert order_id1 > 0
        assert order_id2 > 0


class TestHealthEndpoints:
    """헬스 체크 엔드포인트 테스트"""

    def test_root_endpoint(self, client):
        """루트 엔드포인트가 응답한다 (랜딩 페이지)"""
        response = client.get("/")

        assert response.status_code == status.HTTP_200_OK
        # HTML 응답 확인
        assert "text/html" in response.headers["content-type"]
        assert len(response.text) > 0

    def test_health_endpoint(self, client):
        """헬스 체크 엔드포인트가 응답한다"""
        response = client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
