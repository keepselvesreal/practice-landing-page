"""
Email Sender Port (출력 포트)
"""
from abc import ABC, abstractmethod
from cosmetics_landing.domain.email import Email


class SendEmailPort(ABC):
    """이메일 전송 포트 인터페이스"""

    @abstractmethod
    def send(self, email: Email) -> bool:
        """
        이메일 전송

        Args:
            email: 전송할 이메일 객체

        Returns:
            bool: 전송 성공 여부
        """
        pass
