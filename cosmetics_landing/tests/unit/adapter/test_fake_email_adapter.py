"""
Fake Email Adapter Contract Test
"""
import pytest

from cosmetics_landing.adapter.out.email.fake_email_adapter import FakeEmailAdapter
from cosmetics_landing.application.port.out.email_sender import SendEmailPort
from cosmetics_landing.domain.email import Email


class TestFakeEmailAdapterContract:
    """Fake Email Adapter 계약 검증"""

    def test_implements_send_email_port(self):
        """SendEmailPort 인터페이스 구현 확인"""
        fake_sender = FakeEmailAdapter()
        assert isinstance(fake_sender, SendEmailPort)

    def test_send_returns_boolean(self):
        """send() 메서드가 boolean 반환"""
        fake_sender = FakeEmailAdapter()
        email = Email(
            from_address="test@example.com",
            to_address="support@cosmetics.com",
            subject="Test",
            body="Test message"
        )

        result = fake_sender.send(email)
        assert isinstance(result, bool)


class TestFakeEmailAdapterBehavior:
    """Fake Email Adapter 동작 검증"""

    def test_fake_stores_sent_emails(self):
        """Fake는 전송된 이메일을 저장한다 (테스트 편의성)"""
        # Given
        fake_sender = FakeEmailAdapter(always_succeed=True)

        email = Email(
            from_address="customer@example.com",
            to_address="support@cosmetics.com",
            subject="Inquiry",
            body="When will my order arrive?"
        )

        # When
        result = fake_sender.send(email)

        # Then
        assert result is True
        sent_emails = fake_sender.get_sent_emails()
        assert len(sent_emails) == 1
        assert sent_emails[0].from_address == "customer@example.com"
        assert "When will my order arrive?" in sent_emails[0].body

    def test_fake_allows_failure_mode(self):
        """Fake는 실패 모드 시뮬레이션 가능"""
        # Given
        fake_sender = FakeEmailAdapter(always_succeed=False)

        email = Email(
            from_address="test@example.com",
            to_address="support@cosmetics.com",
            subject="Test",
            body="Test message"
        )

        # When
        result = fake_sender.send(email)

        # Then
        assert result is False
        assert len(fake_sender.get_sent_emails()) == 0

    def test_fake_clear_resets_sent_emails(self):
        """clear() 메서드가 전송 기록을 초기화한다"""
        # Given
        fake_sender = FakeEmailAdapter()
        email = Email(
            from_address="test@example.com",
            to_address="support@cosmetics.com",
            subject="Test",
            body="Test"
        )
        fake_sender.send(email)

        # When
        fake_sender.clear()

        # Then
        assert len(fake_sender.get_sent_emails()) == 0
