"""
Send Inquiry Use Case (입력 포트)
"""
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class SendInquiryCommand:
    """문의 전송 커맨드"""
    customer_email: str
    message: str

    def __post_init__(self):
        """유효성 검증"""
        if not self.customer_email or "@" not in self.customer_email:
            raise ValueError("Invalid email address")
        if not self.message or len(self.message.strip()) == 0:
            raise ValueError("Message cannot be empty")


class SendInquiryUseCase(ABC):
    """문의 전송 유스케이스 인터페이스"""

    @abstractmethod
    def send_inquiry(self, command: SendInquiryCommand) -> bool:
        """
        고객 문의 전송

        Args:
            command: 문의 전송 커맨드

        Returns:
            bool: 전송 성공 여부
        """
        pass
