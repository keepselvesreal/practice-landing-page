"""
Place Order Service 단위 테스트
Chapter 4 & Chapter 8: Mock을 사용한 Use Case 테스트
"""
import pytest
from unittest.mock import Mock
from decimal import Decimal

from cosmetics_landing.application.service.place_order_service import PlaceOrderService
from cosmetics_landing.application.port.in_.place_order_use_case import PlaceOrderCommand
from cosmetics_landing.application.port.out.payment_gateway import PaymentResult
from cosmetics_landing.application.exceptions import PaymentFailedError, InvalidAddressError
from cosmetics_landing.domain.order import OrderId


class TestPlaceOrderCommand:
    """PlaceOrderCommand 검증 테스트"""

    def test_valid_command(self):
        """유효한 명령 생성"""
        command = PlaceOrderCommand(
            customer_email="test@example.com",
            customer_address="123 Main St, Manila",
            product_price=Decimal("29.99")
        )

        assert command.customer_email == "test@example.com"
        assert command.customer_address == "123 Main St, Manila"
        assert command.product_price == Decimal("29.99")

    def test_rejects_empty_email(self):
        """빈 이메일 거부"""
        with pytest.raises(ValueError, match="customer_email is required"):
            PlaceOrderCommand(
                customer_email="",
                customer_address="123 Main St",
                product_price=Decimal("29.99")
            )

    def test_rejects_invalid_email(self):
        """유효하지 않은 이메일 거부"""
        with pytest.raises(ValueError, match="must be valid email address"):
            PlaceOrderCommand(
                customer_email="invalid-email",
                customer_address="123 Main St",
                product_price=Decimal("29.99")
            )

    def test_rejects_empty_address(self):
        """빈 주소 거부"""
        with pytest.raises(ValueError, match="customer_address is required"):
            PlaceOrderCommand(
                customer_email="test@example.com",
                customer_address="",
                product_price=Decimal("29.99")
            )

    def test_rejects_negative_price(self):
        """음수 가격 거부"""
        with pytest.raises(ValueError, match="product_price must be positive"):
            PlaceOrderCommand(
                customer_email="test@example.com",
                customer_address="123 Main St",
                product_price=Decimal("-10.00")
            )


class TestPlaceOrderService:
    """PlaceOrderService 테스트"""

    def create_service(
        self,
        save_order=None,
        process_payment=None,
        validate_address=None
    ):
        """테스트용 서비스 생성 헬퍼"""
        return PlaceOrderService(
            save_order_port=save_order or Mock(),
            process_payment_port=process_payment or Mock(),
            validate_address_port=validate_address or Mock()
        )

    def test_validates_address(self):
        """주문 생성 시 주소 검증 (Business Rule Validation)"""
        # Given: 잘못된 주소
        validate_address = Mock()
        validate_address.is_valid.return_value = False

        service = self.create_service(validate_address=validate_address)

        command = PlaceOrderCommand(
            customer_email="test@example.com",
            customer_address="Invalid Address",
            product_price=Decimal("29.99")
        )

        # When/Then: 예외 발생
        with pytest.raises(InvalidAddressError):
            service.place_order(command)

        validate_address.is_valid.assert_called_once_with("Invalid Address")

    def test_saves_order_before_payment(self):
        """결제 전에 주문을 저장"""
        # Given
        save_order = Mock()
        save_order.save.return_value = OrderId(value=1)

        validate_address = Mock()
        validate_address.is_valid.return_value = True

        process_payment = Mock()
        process_payment.process_payment.return_value = PaymentResult(
            success=True,
            transaction_id="txn_123",
            error_message=None
        )

        service = self.create_service(
            save_order=save_order,
            validate_address=validate_address,
            process_payment=process_payment
        )

        command = PlaceOrderCommand(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Decimal("29.99")
        )

        # When
        service.place_order(command)

        # Then: save가 2번 호출됨 (결제 전, 결제 후)
        assert save_order.save.call_count == 2

    def test_processes_payment(self):
        """결제 처리"""
        # Given
        save_order = Mock()
        save_order.save.return_value = OrderId(value=1)

        validate_address = Mock()
        validate_address.is_valid.return_value = True

        process_payment = Mock()
        process_payment.process_payment.return_value = PaymentResult(
            success=True,
            transaction_id="txn_123",
            error_message=None
        )

        service = self.create_service(
            save_order=save_order,
            validate_address=validate_address,
            process_payment=process_payment
        )

        command = PlaceOrderCommand(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Decimal("29.99")
        )

        # When
        order_id = service.place_order(command)

        # Then
        assert order_id.value == 1
        process_payment.process_payment.assert_called_once()

    def test_raises_exception_when_payment_fails(self):
        """결제 실패 시 예외 발생"""
        # Given
        save_order = Mock()
        save_order.save.return_value = OrderId(value=1)

        validate_address = Mock()
        validate_address.is_valid.return_value = True

        process_payment = Mock()
        process_payment.process_payment.return_value = PaymentResult(
            success=False,
            transaction_id=None,
            error_message="Insufficient funds"
        )

        service = self.create_service(
            save_order=save_order,
            validate_address=validate_address,
            process_payment=process_payment
        )

        command = PlaceOrderCommand(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Decimal("29.99")
        )

        # When/Then
        with pytest.raises(PaymentFailedError, match="Insufficient funds"):
            service.place_order(command)

        # 주문 상태가 failed로 저장되는지 확인
        assert save_order.save.call_count == 2  # 최초 저장 + 실패 상태 저장

    def test_marks_order_as_paid_on_success(self):
        """결제 성공 시 주문을 paid 상태로 변경"""
        # Given
        save_order = Mock()
        save_order.save.return_value = OrderId(value=1)

        validate_address = Mock()
        validate_address.is_valid.return_value = True

        process_payment = Mock()
        process_payment.process_payment.return_value = PaymentResult(
            success=True,
            transaction_id="txn_123",
            error_message=None
        )

        service = self.create_service(
            save_order=save_order,
            validate_address=validate_address,
            process_payment=process_payment
        )

        command = PlaceOrderCommand(
            customer_email="test@example.com",
            customer_address="123 Main St",
            product_price=Decimal("29.99")
        )

        # When
        service.place_order(command)

        # Then: 두 번째 save 호출의 주문이 paid 상태인지 확인
        second_call_order = save_order.save.call_args_list[1][0][0]
        assert second_call_order.is_paid()
