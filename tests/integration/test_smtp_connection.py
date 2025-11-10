"""SMTP 연결 및 이메일 발송 통합 테스트 (스모크 테스트)

Gmail SMTP 서버 연결, 인증, 이메일 발송이 정상 동작하는지 확인
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pytest
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


@pytest.fixture
def smtp_config():
    """SMTP 설정 fixture"""
    gmail_address = os.getenv("GMAIL_ADDRESS")
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_address or not gmail_app_password:
        pytest.skip("GMAIL_ADDRESS 또는 GMAIL_APP_PASSWORD 환경 변수가 설정되지 않음")

    return {
        "host": "smtp.gmail.com",
        "port": 587,
        "username": gmail_address,
        "password": gmail_app_password,
        "from_email": gmail_address,
    }


def test_smtp_connection(smtp_config):
    """SMTP 서버 연결 테스트

    Gmail SMTP 서버에 연결하고 인증이 성공하는지 확인
    """
    print(f"\n[SMTP 연결 테스트]")
    print(f"호스트: {smtp_config['host']}")
    print(f"포트: {smtp_config['port']}")
    print(f"사용자: {smtp_config['username']}")

    # SMTP 서버 연결
    server = smtplib.SMTP(smtp_config["host"], smtp_config["port"])

    # 디버그 출력 활성화 (상세 로그 확인)
    server.set_debuglevel(1)

    try:
        # EHLO 명령 (서버 확인)
        code, message = server.ehlo()
        print(f"\nEHLO 응답 코드: {code}")
        print(f"EHLO 응답 메시지: {message.decode()}")
        assert code == 250, f"EHLO 실패: {code}"

        # TLS 시작
        server.starttls()
        code, message = server.ehlo()
        print(f"\nSTARTTLS 후 EHLO 응답 코드: {code}")
        assert code == 250, f"STARTTLS 후 EHLO 실패: {code}"

        # 로그인
        server.login(smtp_config["username"], smtp_config["password"])
        print(f"\n✓ 로그인 성공: {smtp_config['username']}")

    finally:
        server.quit()


def test_send_simple_email(smtp_config):
    """간단한 텍스트 이메일 발송 테스트

    실제로 이메일을 발송하고 응답 코드를 확인
    """
    print(f"\n[이메일 발송 테스트]")

    # 이메일 내용 구성
    to_email = smtp_config["from_email"]  # 자기 자신에게 발송
    subject = "[테스트] SMTP 연결 테스트"
    body = """
    이 이메일은 SMTP 연결 테스트를 위해 자동으로 발송되었습니다.

    테스트 시간: {test_time}
    발신자: {from_email}
    수신자: {to_email}
    """.format(
        test_time=__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        from_email=smtp_config["from_email"],
        to_email=to_email,
    )

    # MIMEText로 메시지 생성
    message = MIMEText(body, "plain", "utf-8")
    message["From"] = smtp_config["from_email"]
    message["To"] = to_email
    message["Subject"] = subject

    print(f"발신자: {smtp_config['from_email']}")
    print(f"수신자: {to_email}")
    print(f"제목: {subject}")

    # SMTP 서버 연결 및 발송
    server = smtplib.SMTP(smtp_config["host"], smtp_config["port"])
    server.set_debuglevel(1)  # 디버그 출력

    try:
        server.starttls()
        server.login(smtp_config["username"], smtp_config["password"])

        # 이메일 발송
        result = server.send_message(message)

        print(f"\n✓ 이메일 발송 완료")
        print(f"발송 결과: {result if result else '성공 (거부된 수신자 없음)'}")

        # 발송 실패한 수신자가 없어야 함
        assert not result, f"일부 수신자에게 발송 실패: {result}"

    finally:
        server.quit()


def test_send_html_email(smtp_config):
    """HTML 이메일 발송 테스트

    HTML 형식 이메일을 발송하고 제대로 렌더링되는지 확인
    """
    print(f"\n[HTML 이메일 발송 테스트]")

    to_email = smtp_config["from_email"]
    subject = "[테스트] HTML 이메일 테스트"

    # HTML 본문
    html_body = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h1 style="color: #333;">HTML 이메일 테스트</h1>
        <p>이 이메일은 <strong>HTML 형식</strong>으로 발송되었습니다.</p>
        <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
            <p><strong>테스트 정보:</strong></p>
            <ul>
                <li>발신자: {from_email}</li>
                <li>수신자: {to_email}</li>
                <li>시간: {test_time}</li>
            </ul>
        </div>
        <p style="color: #666; font-size: 12px; margin-top: 20px;">
            이 이메일은 자동으로 생성되었습니다.
        </p>
    </body>
    </html>
    """.format(
        from_email=smtp_config["from_email"],
        to_email=to_email,
        test_time=__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    # MIMEMultipart로 메시지 생성 (HTML + 대체 텍스트)
    message = MIMEMultipart("alternative")
    message["From"] = smtp_config["from_email"]
    message["To"] = to_email
    message["Subject"] = subject

    # 텍스트 버전 (HTML 미지원 클라이언트용)
    text_part = MIMEText("이 이메일은 HTML을 지원하는 클라이언트에서 확인해주세요.", "plain", "utf-8")
    html_part = MIMEText(html_body, "html", "utf-8")

    message.attach(text_part)
    message.attach(html_part)

    print(f"발신자: {smtp_config['from_email']}")
    print(f"수신자: {to_email}")
    print(f"제목: {subject}")

    # SMTP 서버 연결 및 발송
    server = smtplib.SMTP(smtp_config["host"], smtp_config["port"])
    server.set_debuglevel(1)

    try:
        server.starttls()
        server.login(smtp_config["username"], smtp_config["password"])

        result = server.send_message(message)

        print(f"\n✓ HTML 이메일 발송 완료")
        print(f"발송 결과: {result if result else '성공'}")

        assert not result, f"일부 수신자에게 발송 실패: {result}"

    finally:
        server.quit()
