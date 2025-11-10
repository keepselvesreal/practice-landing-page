"""이메일 발송 서비스"""

import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from backend.models.order import OrderResponse

# 로거 설정
logger = logging.getLogger(__name__)

# 템플릿 경로
TEMPLATE_DIR = Path(__file__).parent.parent / "templates" / "email"


def _load_template(template_name: str) -> str:
    """HTML 템플릿 로드

    Args:
        template_name: 템플릿 파일명 (예: "order_confirmation.html")

    Returns:
        템플릿 내용

    Raises:
        FileNotFoundError: 템플릿 파일이 없는 경우
    """
    template_path = TEMPLATE_DIR / template_name
    if not template_path.exists():
        raise FileNotFoundError(f"템플릿 파일을 찾을 수 없습니다: {template_path}")

    return template_path.read_text(encoding="utf-8")


def _render_order_confirmation_template(order: OrderResponse) -> tuple[str, str]:
    """주문 확인 이메일 템플릿 렌더링

    Args:
        order: 주문 정보

    Returns:
        (텍스트 본문, HTML 본문) 튜플
    """
    # 금액 계산 (센타보 → 달러)
    product_amount = order.unit_price * order.quantity / 10000
    shipping_fee = order.shipping_fee / 10000
    total_amount = order.total_amount / 10000

    # 텍스트 버전 (HTML 미지원 클라이언트용)
    text_body = f"""
안녕하세요 {order.customer_name}님,

주문이 정상적으로 접수되었습니다.

■ 주문 정보
- 주문 번호: {order.order_number}
- 주문 상태: {order.order_status}
- 수량: {order.quantity}개
- 상품 금액: ${product_amount:.2f}
- 배송비: ${shipping_fee:.2f}
- 총 금액: ${total_amount:.2f}

■ 배송지 정보
- 받는 분: {order.customer_name}
- 연락처: {order.customer_phone}
- 주소: {order.shipping_address}

감사합니다.
    """.strip()

    # HTML 템플릿 로드 및 변수 치환
    html_template = _load_template("order_confirmation.html")
    html_body = html_template.format(
        order_number=order.order_number,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        shipping_address=order.shipping_address,
        order_status=order.order_status,
        quantity=order.quantity,
        product_amount=f"{product_amount:.2f}",
        shipping_fee=f"{shipping_fee:.2f}",
        total_amount=f"{total_amount:.2f}",
    )

    return text_body, html_body


def send_order_confirmation_email(order: OrderResponse) -> bool:
    """주문 확인 이메일 발송

    Args:
        order: 주문 정보

    Returns:
        발송 성공 여부 (True: 성공, False: 실패)

    Raises:
        ValueError: 잘못된 이메일 주소 또는 환경 변수 미설정
    """
    # 환경 변수 확인
    gmail_address = os.getenv("GMAIL_ADDRESS")
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_address or not gmail_app_password:
        raise ValueError("GMAIL_ADDRESS 또는 GMAIL_APP_PASSWORD 환경 변수가 설정되지 않음")

    # 이메일 주소 검증 (간단한 검증)
    if "@" not in order.customer_email or "." not in order.customer_email:
        raise ValueError(f"잘못된 이메일 주소: {order.customer_email}")

    try:
        # 이메일 내용 구성
        subject = f"[주문 확인] 주문 번호: {order.order_number}"
        text_body, html_body = _render_order_confirmation_template(order)

        # MIMEMultipart 메시지 생성 (텍스트 + HTML)
        message = MIMEMultipart("alternative")
        message["From"] = gmail_address
        message["To"] = order.customer_email
        message["Subject"] = subject

        # 텍스트 버전 추가
        text_part = MIMEText(text_body, "plain", "utf-8")
        message.attach(text_part)

        # HTML 버전 추가
        html_part = MIMEText(html_body, "html", "utf-8")
        message.attach(html_part)

        # SMTP 서버 연결 및 발송
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail_address, gmail_app_password)
        server.send_message(message)
        server.quit()

        logger.info(
            f"주문 확인 이메일 발송 성공: {order.order_number} -> {order.customer_email}"
        )
        return True

    except FileNotFoundError as e:
        logger.error(f"이메일 템플릿 로드 실패: {e}")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP 에러: {e}")
        return False
    except Exception as e:
        logger.error(f"이메일 발송 실패: {e}")
        return False
