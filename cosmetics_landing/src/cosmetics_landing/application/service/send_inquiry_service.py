"""
Send Inquiry Service (애플리케이션 서비스)
"""
from cosmetics_landing.application.port.in_.send_inquiry_use_case import (
    SendInquiryUseCase,
    SendInquiryCommand
)
from cosmetics_landing.application.port.out.email_sender import SendEmailPort
from cosmetics_landing.domain.email import Email


class SendInquiryService(SendInquiryUseCase):
    """
    문의 전송 서비스

    고객 문의를 받아 지원팀에게 이메일로 전달
    """

    SUPPORT_EMAIL = "support@cosmetics.com"

    def __init__(self, email_sender_port: SendEmailPort):
        self._email_sender = email_sender_port

    def send_inquiry(self, command: SendInquiryCommand) -> bool:
        """
        고객 문의를 지원팀에게 전송

        Args:
            command: 문의 전송 커맨드

        Returns:
            bool: 전송 성공 여부
        """
        # 이메일 생성
        email = Email(
            from_address=command.customer_email,
            to_address=self.SUPPORT_EMAIL,
            subject=f"고객 문의: {command.customer_email}",
            body=f"고객 이메일: {command.customer_email}\n\n문의 내용:\n{command.message}"
        )

        # 이메일 전송
        return self._email_sender.send(email)
