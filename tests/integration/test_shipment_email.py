"""배송 이메일 SMTP Integration 테스트"""
import pytest
import base64
from backend.models.db import ShipmentDB
from backend.services.email import send_shipment_email, send_delivery_email


@pytest.mark.integration
def test_when_sending_shipment_email_then_smtp_receives_message(smtp_mock, db_session, test_data):
    """
    SMTP 이메일 발송 검증: SHIPPED 상태

    Given: SHIPPED 상태 Shipment (DB에 저장된)
    When: send_shipment_email() 호출
    Then: Mock SMTP에 이메일 1개 수신, 운송장 번호 포함
    """
    # Given: test_data에서 Shipment 가져와서 SHIPPED 상태로 변경
    shipment = test_data["shipment"]
    shipment.shipping_status = "SHIPPED"
    shipment.tracking_number = "1234567890"
    shipment.courier = "LBC Express"
    db_session.commit()
    db_session.refresh(shipment)

    # When: 배송 이메일 발송
    send_shipment_email(shipment)

    # Then: Mock SMTP에서 이메일 확인
    assert len(smtp_mock.messages) == 1

    email_data = smtp_mock.messages[0]["data"]

    # base64 디코딩 (이메일 본문이 인코딩되어 있음)
    # HTML 파트를 찾아서 디코딩
    if "base64" in email_data:
        # base64 인코딩된 부분을 찾아서 디코딩
        import re
        base64_pattern = r'Content-Transfer-Encoding: base64\r\n\r\n(.*?)\r\n\r\n--'
        matches = re.findall(base64_pattern, email_data, re.DOTALL)

        decoded_found = False
        for match in matches:
            try:
                decoded = base64.b64decode(match.replace('\r\n', '')).decode('utf-8')
                if "1234567890" in decoded:
                    decoded_found = True
                    assert "LBC Express" in decoded
                    break
            except:
                continue

        assert decoded_found, "운송장 번호가 이메일 본문에 없음"


@pytest.mark.integration
def test_when_sending_delivery_email_then_smtp_receives_completion_message(smtp_mock, db_session, test_data):
    """
    SMTP 배송완료 이메일 발송 검증: DELIVERED 상태

    Given: DELIVERED 상태 Shipment (DB에 저장된)
    When: send_delivery_email() 호출
    Then: Mock SMTP에 이메일 1개 수신, "배송 완료" 포함
    """
    # Given: test_data에서 Shipment 가져와서 DELIVERED 상태로 변경
    shipment = test_data["shipment"]
    shipment.shipping_status = "DELIVERED"
    shipment.tracking_number = "1234567890"
    shipment.courier = "LBC Express"
    db_session.commit()
    db_session.refresh(shipment)

    # When: 배송 완료 이메일 발송
    send_delivery_email(shipment)

    # Then: Mock SMTP에서 이메일 확인
    assert len(smtp_mock.messages) == 1

    email_data = smtp_mock.messages[0]["data"]

    # base64 디코딩하여 "배송 완료" 확인
    if "base64" in email_data:
        import re
        base64_pattern = r'Content-Transfer-Encoding: base64\r\n\r\n(.*?)\r\n\r\n--'
        matches = re.findall(base64_pattern, email_data, re.DOTALL)

        decoded_found = False
        for match in matches:
            try:
                decoded = base64.b64decode(match.replace('\r\n', '')).decode('utf-8')
                if "배송 완료" in decoded or "배송이 완료" in decoded:
                    decoded_found = True
                    break
            except:
                continue

        assert decoded_found, "배송 완료 메시지가 이메일 본문에 없음"


@pytest.mark.integration
def test_when_smtp_fails_then_retries_three_times_and_logs_critical(db_session, test_data, caplog, monkeypatch):
    """
    SMTP 실패 시 재시도 및 로그 검증

    Given: SMTP 연결이 항상 실패하는 상황
    When: send_shipment_email() 호출
    Then: 재시도 3회 후 CRITICAL 로그 기록
    """
    # Given: test_data에서 Shipment 준비
    shipment = test_data["shipment"]
    shipment.shipping_status = "SHIPPED"
    shipment.tracking_number = "1234567890"
    shipment.courier = "LBC Express"
    db_session.commit()
    db_session.refresh(shipment)

    # SMTP 연결을 항상 실패하도록 monkeypatch
    import smtplib

    original_smtp = smtplib.SMTP
    call_count = {"count": 0}

    def failing_smtp(*args, **kwargs):
        call_count["count"] += 1
        raise smtplib.SMTPConnectError(421, "Connection refused")

    monkeypatch.setattr(smtplib, "SMTP", failing_smtp)

    # When: 이메일 발송 시도 (실패할 것)
    import logging
    # caplog 레벨 설정
    caplog.set_level(logging.DEBUG)
    caplog.set_level(logging.DEBUG, logger="backend.services.email")

    result = send_shipment_email(shipment)

    # Then: 실패 결과
    assert result is False

    # 재시도 3회 확인 (초기 시도 1회 + 재시도 2회 = 총 3회)
    assert call_count["count"] == 3, f"Expected 3 attempts, got {call_count['count']}"

    # CRITICAL 로그 확인
    # 모든 로그 출력 (디버깅용)
    print(f"\n===== Captured logs ({len(caplog.records)} records) =====")
    for record in caplog.records:
        print(f"{record.levelname}: {record.message}")

    critical_logs = [r for r in caplog.records if r.levelname == "CRITICAL"]
    assert len(critical_logs) > 0, f"CRITICAL 로그가 없음. 전체 로그: {[(r.levelname, r.message) for r in caplog.records]}"

    critical_messages = [r.message for r in critical_logs]
    assert any("SMTP" in msg or "실패" in msg for msg in critical_messages), \
        f"SMTP 실패 관련 CRITICAL 로그가 없음. CRITICAL 로그: {critical_messages}"
