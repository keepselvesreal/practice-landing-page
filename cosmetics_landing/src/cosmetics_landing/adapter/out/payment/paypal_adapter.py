"""
PayPal Payment Adapter
실제 PayPal Sandbox/Production API 연동

Learning Test 기반 구현:
- tests/learning/test_paypal_contract.py에서 학습한 API 계약 준수
"""
import paypalrestsdk
from typing import Optional

from ....application.port.out.payment_gateway import ProcessPaymentPort, PaymentResult
from ....domain.order import Order


class PayPalAdapter(ProcessPaymentPort):
    """
    PayPal 결제 어댑터

    Learning Test 기반 계약:
    - Payment ID 형식: PAYID-XXXXX
    - 성공 시: payment.create() == True, payment.state == "created"
    - 실패 시: payment.error 객체 반환
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        mode: str = "sandbox",
        return_url: str = "http://localhost:8000/payment/success",
        cancel_url: str = "http://localhost:8000/payment/cancel"
    ):
        """
        PayPal SDK 설정

        Args:
            client_id: PayPal Client ID
            client_secret: PayPal Client Secret
            mode: "sandbox" 또는 "live"
            return_url: 결제 성공 리다이렉트 URL
            cancel_url: 결제 취소 리다이렉트 URL
        """
        paypalrestsdk.configure({
            "mode": mode,
            "client_id": client_id,
            "client_secret": client_secret
        })

        self.return_url = return_url
        self.cancel_url = cancel_url
        self.mode = mode

    def process_payment(self, order: Order) -> PaymentResult:
        """
        PayPal로 결제 처리

        Learning Test 기반 계약:
        1. payment.create() 호출
        2. 성공 시 payment.id 반환 (PAYID- 접두사)
        3. 실패 시 payment.error 반환
        4. 예외 발생 시 PaymentResult로 변환

        Args:
            order: 결제할 주문

        Returns:
            PaymentResult: 결제 결과 (예외 발생하지 않음)
        """
        try:
            # Learning Test에서 학습한 필수 필드 구조
            payment = paypalrestsdk.Payment({
                "intent": "sale",  # 즉시 판매
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [{
                    "amount": {
                        "total": str(order.product_price.amount),
                        "currency": "USD"
                    },
                    "description": f"Order for {order.customer_email}"
                }],
                "redirect_urls": {
                    "return_url": self.return_url,
                    "cancel_url": self.cancel_url
                }
            })

            # 결제 생성 시도
            if payment.create():
                # 성공: Learning Test에서 확인한 응답 구조
                return PaymentResult(
                    success=True,
                    transaction_id=payment.id,  # PAYID-XXXXX 형식
                    error_message=None
                )
            else:
                # 실패: Learning Test에서 확인한 에러 구조
                error = payment.error if hasattr(payment, 'error') else {}
                error_name = error.get('name', 'UNKNOWN_ERROR')
                error_message = error.get('message', 'Payment processing failed')

                return PaymentResult(
                    success=False,
                    transaction_id=None,
                    error_message=f"{error_name}: {error_message}"
                )

        except Exception as e:
            # PayPal SDK 예외를 PaymentResult로 변환
            return PaymentResult(
                success=False,
                transaction_id=None,
                error_message=f"PayPal API Error: {str(e)}"
            )

    def get_approval_url(self, payment_id: str) -> Optional[str]:
        """
        결제 승인 URL 조회 (선택적 기능)

        Learning Test에서 학습: payment.links에서 approval_url 추출

        Args:
            payment_id: PayPal Payment ID

        Returns:
            approval_url 또는 None
        """
        try:
            payment = paypalrestsdk.Payment.find(payment_id)

            for link in payment.links:
                if link.rel == "approval_url":
                    return link.href

            return None

        except Exception:
            return None
