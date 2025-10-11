"""
Fake Email Adapter (테스트용)
"""
from cosmetics_landing.application.port.out.email_sender import SendEmailPort
from cosmetics_landing.domain.email import Email


class FakeEmailAdapter(SendEmailPort):
    """
    Fake Email Sender

    테스트용 이메일 전송 어댑터
    전송된 이메일을 메모리에 저장하여 검증 가능
    """

    def __init__(self, always_succeed: bool = True):
        """
        Args:
            always_succeed: True면 항상 성공, False면 항상 실패
        """
        self._always_succeed = always_succeed
        self._sent_emails: list[Email] = []

    def send(self, email: Email) -> bool:
        """
        이메일 전송 시뮬레이션

        Args:
            email: 전송할 이메일

        Returns:
            bool: 전송 성공 여부
        """
        if self._always_succeed:
            self._sent_emails.append(email)
            return True
        return False

    def get_sent_emails(self) -> list[Email]:
        """전송된 이메일 목록 반환 (테스트 검증용)"""
        return self._sent_emails.copy()

    def clear(self):
        """전송 기록 초기화"""
        self._sent_emails.clear()
