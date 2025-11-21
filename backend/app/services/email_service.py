import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import settings


def send_order_confirmation_email(recipient_email: str, order_number: str) -> bool:
    """
    Send order confirmation email using Gmail SMTP.

    Args:
        recipient_email: Customer email address
        order_number: Order number to include in email

    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Create message
        message = MIMEMultipart()
        message["From"] = settings.gmail_address
        message["To"] = recipient_email
        message["Subject"] = f"주문 확인 - {order_number}"

        # Email body
        body = f"""
안녕하세요,

주문이 정상적으로 접수되었습니다.

주문번호: {order_number}

감사합니다.
K-Beauty Team
"""
        message.attach(MIMEText(body, "plain", "utf-8"))

        # Connect to Gmail SMTP server
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()  # Enable TLS
            server.login(settings.gmail_address, settings.gmail_app_password)
            server.send_message(message)

        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
