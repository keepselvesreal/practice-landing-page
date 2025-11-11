"""Admin 배송 관리 E2E 테스트 (Walking Skeleton)"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.e2e
def test_관리자가_배송상태를_SHIPPED로_변경하면_발송이메일이_발송된다(test_client: TestClient, db_session, test_data):
    """
    Phase 1 Walking Skeleton - 최소 구현 테스트

    Given: PAID 상태 주문이 존재
    When: 관리자가 배송 상태를 SHIPPED로 변경
    Then: 성공 메시지가 표시되고, 업데이트된 정보가 화면에 표시됨
    """
    # Given: 테스트 데이터는 test_data fixture에서 생성됨
    order_id = test_data["order"].id

    # When: 관리자 페이지에서 배송 정보 업데이트 (리다이렉트 자동 따라가기)
    response = test_client.post(
        f"/admin/shipments/{order_id}",
        data={
            "status": "SHIPPED",
            "tracking_number": "1234567890",
            "courier": "LBC Express"
        },
        follow_redirects=True  # 리다이렉트 자동 따라가기
    )

    # Then: 최종 페이지 응답 확인
    assert response.status_code == 200
    html = response.text

    # 성공 메시지 확인
    assert "저장되었습니다" in html

    # 업데이트된 정보 확인 (HTML에 표시됨)
    assert "SHIPPED" in html
    assert "1234567890" in html
    assert "LBC Express" in html

    # Note: 이메일 발송은 콘솔 출력으로 확인 (Walking Skeleton)
    # Phase 2에서 Mock SMTP로 검증 예정
