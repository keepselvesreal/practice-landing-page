"""
Gmail SMTP Adapter Integration Test
GOOS 8장: 어댑터 테스트는 얇고 통제 가능하게
"""
import pytest
from unittest import mock

from cosmetics_landing.adapter.out.email.gmail_smtp_adapter import GmailSmtpAdapter
from cosmetics_landing.application.port.out.email_sender import SendEmailPort
from cosmetics_landing.domain.email import Email


class TestGmailAdapterPortCompliance:
    """Gmail 어댑터의 포트 인터페이스 준수 검증"""

    def test_implements_send_email_port(self):
        """SendEmailPort 인터페이스 구현 확인"""
        adapter = GmailSmtpAdapter()
        assert isinstance(adapter, SendEmailPort)


class TestGmailAdapterSMTPContract:
    """Gmail 어댑터가 SMTP 프로토콜 계약을 준수한다"""

    def test_gmail_adapter_follows_smtp_protocol(self):
        """
        SMTP 프로토콜 계약 검증

        Mock SMTP 응답 시뮬레이션
        """
        with mock.patch("smtplib.SMTP") as mock_smtp:
            # SMTP 서버 응답 시뮬레이션
            mock_instance = mock_smtp.return_value.__enter__.return_value
            mock_instance.sendmail.return_value = {}

            adapter = GmailSmtpAdapter(
                smtp_server="smtp.gmail.com",
                port=587,
                username="test@example.com",
                password="test_password"
            )

            email = Email(
                from_address="customer@example.com",
                to_address="support@cosmetics.com",
                subject="Test",
                body="Test message"
            )

            result = adapter.send(email)

            # Then: SMTP 프로토콜 계약 검증
            assert result is True
            mock_instance.starttls.assert_called_once()
            mock_instance.login.assert_called_once_with("test@example.com", "test_password")
            mock_instance.sendmail.assert_called_once()

    def test_handles_smtp_authentication_failure(self):
        """SMTP 인증 실패 시 적절히 처리"""
        with mock.patch("smtplib.SMTP") as mock_smtp:
            mock_instance = mock_smtp.return_value.__enter__.return_value
            mock_instance.login.side_effect = Exception("Authentication failed")

            adapter = GmailSmtpAdapter(
                smtp_server="smtp.gmail.com",
                port=587,
                username="invalid",
                password="invalid"
            )

            email = Email(
                from_address="test@example.com",
                to_address="support@cosmetics.com",
                subject="Test",
                body="Test message"
            )

            # When: 예외를 잡아서 False 반환해야 함
            result = adapter.send(email)

            # Then
            assert result is False

    def test_handles_network_failure(self):
        """네트워크 오류 시 적절히 처리"""
        with mock.patch("smtplib.SMTP") as mock_smtp:
            mock_smtp.side_effect = Exception("Network error")

            adapter = GmailSmtpAdapter(
                smtp_server="smtp.gmail.com",
                port=587,
                username="test@example.com",
                password="test_password"
            )

            email = Email(
                from_address="test@example.com",
                to_address="support@cosmetics.com",
                subject="Test",
                body="Test"
            )

            result = adapter.send(email)

            # Then: 예외를 잡아서 False 반환
            assert result is False
