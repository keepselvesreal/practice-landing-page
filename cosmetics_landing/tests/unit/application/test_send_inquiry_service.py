"""
Send Inquiry Service 단위 테스트
"""
import pytest
from unittest.mock import Mock

from cosmetics_landing.application.service.send_inquiry_service import SendInquiryService
from cosmetics_landing.application.port.in_.send_inquiry_use_case import SendInquiryCommand
from cosmetics_landing.domain.email import Email


# 테스트 상수 (GOOS 23장: 자기 설명적 값)
CUSTOMER_EMAIL = "customer@example.com"
SUPPORT_EMAIL = "support@cosmetics.com"
SAMPLE_INQUIRY_MESSAGE = "When will my order arrive?"


# 테스트 헬퍼
def assert_inquiry_sent_successfully(result: bool):
    """
    문의 전송 성공 검증

    실패 시 명확한 메시지 제공 (GOOS 23장)
    """
    assert result is True, "Inquiry email should be sent successfully"


def assert_email_sent_with(
    mock_sender,
    from_email: str,
    to_email: str,
    containing: str
):
    """
    이메일 전송 내용 검증

    GOOS 24장: 유연한 단언 - 중요한 부분만 검증
    """
    mock_sender.send.assert_called_once()
    sent_email = mock_sender.send.call_args[0][0]

    assert sent_email.from_address == from_email, \
        f"Expected from={from_email}, got {sent_email.from_address}"
    assert sent_email.to_address == to_email, \
        f"Expected to={to_email}, got {sent_email.to_address}"
    assert containing in sent_email.body, \
        f"Email body should contain '{containing}'"


class TestSendInquiryService:
    """SendInquiryService 테스트"""

    def test_sends_inquiry_email_to_support(self):
        """
        문의 내용을 고객 이메일에서 지원팀으로 전송한다

        Given: 고객이 문의 메시지 작성
        When: 문의 전송 서비스 호출
        Then: 지원팀에게 이메일 전송됨
        """
        # Given
        email_sender = Mock()
        email_sender.send.return_value = True

        service = SendInquiryService(email_sender_port=email_sender)

        command = SendInquiryCommand(
            customer_email=CUSTOMER_EMAIL,
            message=SAMPLE_INQUIRY_MESSAGE
        )

        # When
        result = service.send_inquiry(command)

        # Then: 자기 설명적 검증
        assert_inquiry_sent_successfully(result)
        assert_email_sent_with(
            email_sender,
            from_email=CUSTOMER_EMAIL,
            to_email=SUPPORT_EMAIL,
            containing=SAMPLE_INQUIRY_MESSAGE
        )

    def test_handles_email_send_failure(self):
        """이메일 전송 실패 시 False 반환"""
        # Given
        email_sender = Mock()
        email_sender.send.return_value = False  # 전송 실패

        service = SendInquiryService(email_sender_port=email_sender)

        command = SendInquiryCommand(
            customer_email=CUSTOMER_EMAIL,
            message="Test message"
        )

        # When
        result = service.send_inquiry(command)

        # Then
        assert result is False, "Should return False on send failure"

    def test_rejects_invalid_email(self):
        """잘못된 이메일은 거부된다"""
        # Given
        email_sender = Mock()
        service = SendInquiryService(email_sender_port=email_sender)

        # When/Then
        with pytest.raises(ValueError, match="Invalid email"):
            SendInquiryCommand(
                customer_email="invalid-email",
                message="Test message"
            )

    def test_rejects_empty_message(self):
        """빈 메시지는 거부된다"""
        # Given
        email_sender = Mock()
        service = SendInquiryService(email_sender_port=email_sender)

        # When/Then
        with pytest.raises(ValueError, match="Message cannot be empty"):
            SendInquiryCommand(
                customer_email=CUSTOMER_EMAIL,
                message=""
            )
