"""
Gmail SMTP Adapter (실제 구현)
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from cosmetics_landing.application.port.out.email_sender import SendEmailPort
from cosmetics_landing.domain.email import Email


class GmailSmtpAdapter(SendEmailPort):
    """
    Gmail SMTP 어댑터

    실제 Gmail SMTP 서버를 통해 이메일 전송
    """

    def __init__(
        self,
        smtp_server: str = "smtp.gmail.com",
        port: int = 587,
        username: str = "",
        password: str = ""
    ):
        """
        Args:
            smtp_server: SMTP 서버 주소
            port: SMTP 포트 (기본 587 - TLS)
            username: SMTP 인증 사용자명
            password: SMTP 인증 비밀번호
        """
        self._smtp_server = smtp_server
        self._port = port
        self._username = username
        self._password = password

    def send(self, email: Email) -> bool:
        """
        Gmail SMTP로 이메일 전송

        Args:
            email: 전송할 이메일

        Returns:
            bool: 전송 성공 여부
        """
        try:
            # MIME 메시지 생성
            msg = MIMEMultipart()
            msg['From'] = email.from_address
            msg['To'] = email.to_address
            msg['Subject'] = email.subject

            # 본문 추가
            msg.attach(MIMEText(email.body, 'plain', 'utf-8'))

            # SMTP 서버 연결 및 전송
            with smtplib.SMTP(self._smtp_server, self._port) as server:
                server.starttls()  # TLS 암호화
                server.login(self._username, self._password)
                server.sendmail(
                    email.from_address,
                    email.to_address,
                    msg.as_string()
                )

            return True

        except Exception as e:
            # 로그 기록 (실제 프로덕션에서는 로거 사용)
            print(f"Email send failed: {e}")
            return False
