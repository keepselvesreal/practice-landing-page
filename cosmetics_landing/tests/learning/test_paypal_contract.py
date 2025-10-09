"""
PayPal API Contract Learning Test
Chapter 22: "Maintaining the TDD Cycle"

목적:
1. 실제 PayPal Sandbox API 동작 확인
2. API 계약(request/response) 구조 학습
3. 에러 처리 방식 이해
4. Mock 및 실제 어댑터 구현 근거 마련

실행:
    pytest tests/learning/test_paypal_contract.py -v -m learning
"""
import pytest
import os
from decimal import Decimal
from datetime import datetime

# PayPal SDK import
try:
    import paypalrestsdk
except ImportError:
    pytest.skip("paypalrestsdk not installed", allow_module_level=True)


@pytest.fixture(scope="module")
def paypal_config():
    """PayPal Sandbox 설정"""
    client_id = os.getenv("PAYPAL_SANDBOX_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_SANDBOX_CLIENT_SECRET")

    if not client_id or not client_secret:
        pytest.skip("PayPal credentials not configured in .env")

    paypalrestsdk.configure({
        "mode": "sandbox",
        "client_id": client_id,
        "client_secret": client_secret
    })

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "mode": "sandbox"
    }


@pytest.mark.learning
class TestPayPalPaymentCreation:
    """PayPal 결제 생성 API 계약 학습"""

    def test_payment_creation_returns_payment_id(self, paypal_config):
        """
        학습 목표: 결제 생성 시 payment_id를 반환한다

        API 계약 검증:
        - 성공 시 payment.create() == True
        - payment.id가 "PAY-"로 시작
        - payment.state == "created"
        """
        # Given: 최소 결제 정보
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": "10.00",
                    "currency": "USD"
                },
                "description": "Learning test payment"
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/success",
                "cancel_url": "http://localhost:8000/payment/cancel"
            }
        })

        # When: 결제 생성
        result = payment.create()

        # Then: 성공 응답 검증
        assert result is True, f"Payment creation failed: {payment.error}"

        # Payment ID 검증
        assert payment.id is not None
        assert isinstance(payment.id, str)
        assert payment.id.startswith("PAYID-"), f"Unexpected payment ID format: {payment.id}"

        # State 검증
        assert payment.state == "created"

        # Timestamps 검증
        assert hasattr(payment, 'create_time')
        assert payment.create_time is not None

        print(f"\n✅ Payment created: {payment.id}")
        print(f"   State: {payment.state}")
        print(f"   Created: {payment.create_time}")

    def test_payment_creation_provides_approval_url(self, paypal_config):
        """
        학습 목표: 결제 생성 시 approval_url을 제공한다

        API 계약 검증:
        - payment.links 배열 존재
        - rel="approval_url"인 링크 포함
        - approval_url에 paypal.com 포함
        """
        # Given
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": "10.00", "currency": "USD"}
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/success",
                "cancel_url": "http://localhost:8000/payment/cancel"
            }
        })

        # When
        payment.create()

        # Then: Links 검증
        assert hasattr(payment, 'links')
        assert len(payment.links) > 0

        # approval_url 추출
        approval_url = None
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = link.href
                break

        assert approval_url is not None, "approval_url not found in payment.links"
        assert "paypal.com" in approval_url

        print(f"\n✅ Approval URL: {approval_url[:50]}...")

    def test_payment_with_different_amounts(self, paypal_config):
        """
        학습 목표: 다양한 금액으로 결제 생성 가능

        API 계약 검증:
        - 소수점 이하 2자리 금액 처리
        - 다양한 금액 범위 지원
        """
        test_amounts = ["1.00", "29.99", "100.00", "999.99"]

        for amount in test_amounts:
            # Given
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "transactions": [{
                    "amount": {"total": amount, "currency": "USD"}
                }],
                "redirect_urls": {
                    "return_url": "http://localhost:8000/success",
                    "cancel_url": "http://localhost:8000/cancel"
                }
            })

            # When
            result = payment.create()

            # Then
            assert result is True, f"Failed for amount {amount}: {payment.error}"
            assert payment.transactions[0].amount.total == amount

            print(f"✅ Amount {amount}: {payment.id}")


@pytest.mark.learning
class TestPayPalErrorHandling:
    """PayPal 에러 처리 계약 학습"""

    def test_invalid_amount_returns_error(self, paypal_config):
        """
        학습 목표: 잘못된 금액으로 결제 생성 시 에러를 반환한다

        API 계약 검증:
        - payment.create() == False
        - payment.error 객체 존재
        - error.name 필드 포함
        """
        # Given: 음수 금액
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": "-10.00", "currency": "USD"}
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8000/success",
                "cancel_url": "http://localhost:8000/cancel"
            }
        })

        # When
        result = payment.create()

        # Then: 실패 응답 검증
        assert result is False, "Payment creation should fail with negative amount"

        # Error 구조 검증
        assert hasattr(payment, 'error')
        assert payment.error is not None
        assert 'name' in payment.error

        print(f"\n✅ Error caught: {payment.error.get('name')}")
        print(f"   Message: {payment.error.get('message', 'N/A')}")

    def test_missing_redirect_urls_returns_error(self, paypal_config):
        """
        학습 목표: redirect_urls 누락 시 에러를 반환한다

        API 계약 검증:
        - PayPal 결제는 redirect_urls 필수
        - 누락 시 validation error
        """
        # Given: redirect_urls 없음
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": "10.00", "currency": "USD"}
            }]
            # redirect_urls 누락
        })

        # When
        result = payment.create()

        # Then
        assert result is False
        assert payment.error is not None

        print(f"\n✅ Validation error: {payment.error.get('name')}")

    def test_zero_amount_returns_error(self, paypal_config):
        """
        학습 목표: 0원 결제는 거부된다

        API 계약 검증:
        - amount.total이 0인 경우 에러
        """
        # Given
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": "0.00", "currency": "USD"}
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8000/success",
                "cancel_url": "http://localhost:8000/cancel"
            }
        })

        # When
        result = payment.create()

        # Then
        assert result is False
        print(f"\n✅ Zero amount rejected: {payment.error.get('name')}")


@pytest.mark.learning
class TestPayPalResponseStructure:
    """PayPal 응답 구조 상세 학습"""

    def test_payment_response_contains_expected_fields(self, paypal_config):
        """
        학습 목표: 결제 응답의 모든 필드 구조 파악

        API 계약 검증:
        - 응답 객체의 필드 목록
        - 각 필드의 타입
        - HATEOAS links 구조
        """
        # Given & When
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": "10.00", "currency": "USD"},
                "description": "Test payment for response structure"
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8000/success",
                "cancel_url": "http://localhost:8000/cancel"
            }
        })
        payment.create()

        # Then: 응답 구조 분석
        print("\n📋 Payment Response Structure:")
        print(f"   ID: {payment.id}")
        print(f"   Intent: {payment.intent}")
        print(f"   State: {payment.state}")
        print(f"   Create Time: {payment.create_time}")

        # Payer 정보
        assert hasattr(payment, 'payer')
        print(f"   Payer Method: {payment.payer.payment_method}")

        # Transactions 정보
        assert hasattr(payment, 'transactions')
        assert len(payment.transactions) > 0
        tx = payment.transactions[0]
        print(f"   Amount: {tx.amount.total} {tx.amount.currency}")

        # Links 정보
        assert hasattr(payment, 'links')
        print(f"   Links: {len(payment.links)} links")
        for link in payment.links:
            print(f"      - {link.rel}: {link.method} {link.href[:50]}...")

        # 필수 필드 존재 확인
        assert payment.id is not None
        assert payment.intent == "sale"
        assert payment.state == "created"
        assert payment.create_time is not None
