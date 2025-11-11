"""이메일 발송 서비스 통합 테스트 (Outside-in TDD)

주문 확인 이메일 발송 기능을 E2E로 테스트
"""

import os

import pytest
from dotenv import load_dotenv

from backend.models.order import OrderResponse
from backend.services.email import send_order_confirmation_email

load_dotenv()


@pytest.fixture
def sample_order():
    """테스트용 주문 데이터"""
    return OrderResponse(
        order_number="ORD-20251110-ABC123",
        customer_name="홍길동",
        customer_email=os.getenv("GMAIL_ADDRESS", "test@example.com"),  # 환경변수 없으면 기본값
        customer_phone="010-1234-5678",
        shipping_address="서울특별시 강남구 테헤란로 123",
        product_id=1,
        quantity=2,
        unit_price=2500000,  # 25,000.00 USD (센타보)
        shipping_fee=1000000,  # 10,000.00 USD (센타보)
        total_amount=6000000,  # 60,000.00 USD (센타보)
        order_status="PENDING",
        affiliate_code="AFFILIATE123",
    )


def test_send_order_confirmation_email(sample_order, smtp_mock):
    """주문 확인 이메일 발송 테스트

    Given: 주문 정보가 있을 때
    When: send_order_confirmation_email() 함수를 호출하면
    Then: 이메일이 성공적으로 발송되어야 한다
    """
    # Gmail 환경 변수 확인
    if not os.getenv("GMAIL_ADDRESS") or not os.getenv("GMAIL_APP_PASSWORD"):
        pytest.skip("GMAIL_ADDRESS 또는 GMAIL_APP_PASSWORD 환경 변수가 설정되지 않음")

    # When: 주문 확인 이메일 발송
    result = send_order_confirmation_email(sample_order)

    # Then: 발송 성공
    assert result is True, "이메일 발송이 실패했습니다"

    # Mock SMTP가 이메일을 받았는지 확인
    assert len(smtp_mock.messages) > 0, "Mock SMTP가 이메일을 받지 못했습니다"

    print(f"\n✓ 주문 확인 이메일 발송 성공")
    print(f"  수신자: {sample_order.customer_email}")
    print(f"  주문 번호: {sample_order.order_number}")
    print(f"  총 금액: ${sample_order.total_amount / 10000:.2f}")


def test_send_order_confirmation_email_with_invalid_email(sample_order):
    """잘못된 이메일 주소로 발송 시 에러 처리 테스트

    Given: 잘못된 이메일 주소가 있을 때
    When: send_order_confirmation_email() 함수를 호출하면
    Then: False를 반환하거나 예외를 발생시켜야 한다
    """
    if not os.getenv("GMAIL_ADDRESS") or not os.getenv("GMAIL_APP_PASSWORD"):
        pytest.skip("GMAIL_ADDRESS 또는 GMAIL_APP_PASSWORD 환경 변수가 설정되지 않음")

    # Given: 잘못된 이메일 주소
    sample_order.customer_email = "invalid-email-address"

    # When & Then: 에러 발생 또는 False 반환
    # Pydantic EmailStr 검증으로 이미 걸러지겠지만, 서비스 레벨에서도 체크
    with pytest.raises(ValueError):
        send_order_confirmation_email(sample_order)
