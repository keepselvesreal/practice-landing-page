"""
Place Order Service - Use Case 구현
Chapter 4: Use Case 4단계 구조 적용
"""
from decimal import Decimal
from typing import Optional

from ..port.in_.place_order_use_case import PlaceOrderUseCase, PlaceOrderCommand
from ..port.out.order_repository import SaveOrderPort
from ..port.out.payment_gateway import ProcessPaymentPort
from ..port.out.address_validator import ValidateAddressPort
from ..port.out.affiliate_repository import LoadAffiliatePort, SaveAffiliatePort
from ..exceptions import PaymentFailedError, InvalidAddressError

from ...domain.order import Order, OrderId, Money
from ...domain.commission import Commission


class PlaceOrderService(PlaceOrderUseCase):
    """
    주문 생성 Use Case 구현

    Chapter 4, Lines 237-243: Use Case 4단계
    1. Input 받기 (Command 객체)
    2. 비즈니스 규칙 검증
    3. 모델 상태 조작
    4. Output 반환
    """

    def __init__(
        self,
        save_order_port: SaveOrderPort,
        process_payment_port: ProcessPaymentPort,
        validate_address_port: ValidateAddressPort,
        load_affiliate_port: Optional[LoadAffiliatePort] = None,
        save_affiliate_port: Optional[SaveAffiliatePort] = None
    ):
        """
        의존성 주입

        Args:
            save_order_port: 주문 저장 포트
            process_payment_port: 결제 처리 포트
            validate_address_port: 주소 검증 포트
            load_affiliate_port: 어필리에이트 조회 포트 (옵션)
            save_affiliate_port: 어필리에이트 저장 포트 (옵션)
        """
        self.save_order = save_order_port
        self.process_payment = process_payment_port
        self.validate_address = validate_address_port
        self.load_affiliate = load_affiliate_port
        self.save_affiliate = save_affiliate_port
        self.commission_calculator = Commission()

    def place_order(self, command: PlaceOrderCommand) -> OrderId:
        """
        주문 생성 및 결제 처리

        Walking Skeleton: 주문 생성 → 저장 → 결제 → 상태 업데이트
        """
        # 1. Input 받기 (Command 객체) - 이미 검증됨 (Self-Validating)

        # 2. Business Rule Validation (Chapter 4, Lines 428-521)
        if not self.validate_address.is_valid(command.customer_address):
            raise InvalidAddressError(command.customer_address)

        # 3. 도메인 엔티티 생성
        order = Order.create_new(
            customer_email=command.customer_email,
            customer_address=command.customer_address,
            product_price=Money.of(command.product_price),
            affiliate_code=command.affiliate_code
        )

        # 4. 주문 저장 (결제 전)
        order_id = self.save_order.save(order)

        # ID를 가진 주문 객체 생성
        order_with_id = Order(
            id=order_id,
            customer_email=order.customer_email,
            customer_address=order.customer_address,
            product_price=order.product_price,
            affiliate_code=order.affiliate_code,
            created_at=order.created_at,
            payment_status=order.payment_status
        )

        # 5. 결제 처리
        payment_result = self.process_payment.process_payment(order_with_id)
        if not payment_result.success:
            # 결제 실패 시 주문 상태 업데이트
            failed_order = order_with_id.mark_as_failed()
            self.save_order.save(failed_order)
            raise PaymentFailedError(
                payment_result.error_message or "Unknown payment error"
            )

        # 6. 주문 상태 업데이트 (결제 완료)
        paid_order = order_with_id.mark_as_paid()
        self.save_order.save(paid_order)

        # 7. 어필리에이트 커미션 기록 (결제 성공 후)
        if command.affiliate_code and self.load_affiliate and self.save_affiliate:
            self._track_affiliate_sale(command.affiliate_code, order.product_price)

        # 8. Output 반환
        return order_id

    def _track_affiliate_sale(self, affiliate_code: str, order_amount: Money) -> None:
        """
        어필리에이트 판매 추적 (내부 헬퍼)

        Args:
            affiliate_code: 어필리에이트 코드
            order_amount: 주문 금액
        """
        try:
            # 어필리에이트 조회
            affiliate = self.load_affiliate.load_by_code(affiliate_code)
            if not affiliate:
                # 어필리에이트가 없으면 기록하지 않음 (주문은 정상 처리)
                return

            # 커미션 계산
            commission = self.commission_calculator.calculate(order_amount)

            # 판매 기록
            updated_affiliate = affiliate.record_sale(commission)
            self.save_affiliate.save(updated_affiliate)
        except Exception:
            # 어필리에이트 추적 실패해도 주문은 정상 처리
            pass
