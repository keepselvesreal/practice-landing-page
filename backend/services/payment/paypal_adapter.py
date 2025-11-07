"""PayPal Adapter

PayPal SDK를 우리 애플리케이션 인터페이스로 감싸는 얇은 Adapter
Outside-In TDD [8.2]: "가능한 얇게 유지 (테스트하기 어려운 코드 최소화)"
"""
import os
from paypalserversdk.paypal_serversdk_client import PaypalServersdkClient
from paypalserversdk.http.auth.o_auth_2 import ClientCredentialsAuthCredentials
from paypalserversdk.configuration import Environment

from backend.services.payment.payment_service import (
    PaymentService,
    CreateOrderResult,
    PaymentServiceError,
)


class PayPalAdapter(PaymentService):
    """PayPal SDK를 감싸는 Adapter

    Learning Test에서 확인한 PayPal API 동작 방식:
    - create_order로 Order 생성
    - 응답의 links에서 rel="approve" 찾아서 approval_url 추출
    """

    def __init__(self, client_id: str | None = None, client_secret: str | None = None):
        """PayPal Client 초기화

        Args:
            client_id: PayPal Client ID (None이면 환경변수에서 로드)
            client_secret: PayPal Client Secret (None이면 환경변수에서 로드)
        """
        self.client_id = client_id or os.getenv("PAYPAL_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("PAYPAL_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            raise PaymentServiceError("PayPal credentials not configured")

        self.client = PaypalServersdkClient(
            client_credentials_auth_credentials=ClientCredentialsAuthCredentials(
                o_auth_client_id=self.client_id,
                o_auth_client_secret=self.client_secret
            ),
            environment=Environment.SANDBOX
        )

    def create_order(self, amount: int, currency: str = "PHP") -> CreateOrderResult:
        """PayPal Order 생성

        Args:
            amount: 결제 금액 (센타보 단위)
            currency: 통화 코드

        Returns:
            CreateOrderResult: Order ID, approval URL

        Raises:
            PaymentServiceError: PayPal API 호출 실패
        """
        try:
            # 센타보 → 페소 변환 (PayPal API는 소수점 금액 사용)
            amount_in_currency = f"{amount / 100:.2f}"

            order_body = {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": currency,
                            "value": amount_in_currency
                        }
                    }
                ]
            }

            result = self.client.orders.create_order(
                {
                    "body": order_body,
                    "prefer": "return=representation"
                }
            )

            if result.status_code != 201:
                raise PaymentServiceError(
                    f"PayPal order creation failed: {result.status_code}"
                )

            order = result.body

            # approval_url 찾기 (Learning Test에서 확인한 방식)
            approval_url = None
            for link in order.links:
                if link.rel == "approve":
                    approval_url = link.href
                    break

            if not approval_url:
                raise PaymentServiceError("Approval URL not found in PayPal response")

            return CreateOrderResult(
                order_id=order.id,
                approval_url=approval_url,
                status=order.status
            )

        except PaymentServiceError:
            raise
        except Exception as e:
            raise PaymentServiceError(f"PayPal API error: {str(e)}") from e

    def capture_order(self, order_id: str) -> dict:
        """PayPal Order Capture (결제 확정)

        Args:
            order_id: PayPal Order ID

        Returns:
            dict: Capture 결과

        Raises:
            PaymentServiceError: Capture 실패
        """
        try:
            result = self.client.orders.capture_order(
                {
                    "id": order_id,
                    "prefer": "return=representation"
                }
            )

            if result.status_code != 201:
                raise PaymentServiceError(
                    f"PayPal capture failed: {result.status_code}"
                )

            return {
                "order_id": result.body.id,
                "status": result.body.status
            }

        except PaymentServiceError:
            raise
        except Exception as e:
            raise PaymentServiceError(f"PayPal capture error: {str(e)}") from e
