"""
Fake Payment Adapter
Walking Skeleton용 결제 시뮬레이터
"""
from ....application.port.out.payment_gateway import ProcessPaymentPort, PaymentResult
from ....domain.order import Order


class FakePaymentAdapter(ProcessPaymentPort):
    """
    Fake 결제 어댑터

    Walking Skeleton: 실제 PayPal 대신 항상 성공 반환
    추후 실제 PayPal 어댑터로 교체
    """

    def __init__(self, always_succeed: bool = True):
        """
        Args:
            always_succeed: True면 항상 성공, False면 항상 실패
        """
        self.always_succeed = always_succeed
        self.processed_orders = []  # 테스트용 추적

    def process_payment(self, order: Order) -> PaymentResult:
        """결제 처리 시뮬레이션"""
        self.processed_orders.append(order)

        if self.always_succeed:
            return PaymentResult(
                success=True,
                transaction_id=f"fake_txn_{order.id.value if order.id else 'unknown'}",
                error_message=None
            )
        else:
            return PaymentResult(
                success=False,
                transaction_id=None,
                error_message="Fake payment failure"
            )
