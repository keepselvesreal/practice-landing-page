"""
Email 도메인 엔티티
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """
    이메일 값 객체

    불변 객체로 이메일 전송 정보 캡슐화
    """
    from_address: str
    to_address: str
    subject: str
    body: str

    def __post_init__(self):
        """유효성 검증"""
        if not self.from_address or "@" not in self.from_address:
            raise ValueError("Invalid from_address")
        if not self.to_address or "@" not in self.to_address:
            raise ValueError("Invalid to_address")
        if not self.subject:
            raise ValueError("Subject cannot be empty")
        if not self.body:
            raise ValueError("Body cannot be empty")
