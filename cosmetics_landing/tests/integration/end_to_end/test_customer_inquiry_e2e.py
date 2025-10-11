"""
Epic 3 인수 테스트: 고객 문의 전체 흐름
GOOS 4-5장: 사용자 관점 E2E 검증
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fastapi import status


@pytest.mark.e2e
class TestCustomerInquiryE2E:
    """고객 문의 E2E 테스트"""

    def test_customer_can_send_inquiry_from_landing_page(
        self, selenium_driver, live_server
    ):
        """
        인수 테스트: 고객이 랜딩 페이지에서 문의를 보내고 확인 메시지를 받는다

        사용자 여정:
        1. 랜딩 페이지 방문
        2. 문의 폼 작성 및 제출
        3. 성공 메시지 표시
        """
        # Given: 랜딩 페이지 방문
        selenium_driver.get(f"{live_server}/")

        # When: 문의 폼 작성 및 제출
        selenium_driver.find_element(By.ID, "inquiry_email").send_keys("customer@example.com")
        selenium_driver.find_element(By.ID, "inquiry_message").send_keys("When will my order arrive?")
        selenium_driver.find_element(By.ID, "submit_inquiry").click()

        # Then: 성공 메시지 표시
        wait = WebDriverWait(selenium_driver, 10)
        success_msg = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inquiry-success"))
        )
        assert "문의가 접수되었습니다" in success_msg.text

    def test_inquiry_form_validates_email(self, selenium_driver, live_server):
        """잘못된 이메일 형식은 거부된다"""
        # Given: 랜딩 페이지 방문
        selenium_driver.get(f"{live_server}/")

        # When: 잘못된 이메일로 제출
        selenium_driver.find_element(By.ID, "inquiry_email").send_keys("invalid-email")
        selenium_driver.find_element(By.ID, "inquiry_message").send_keys("Test message")
        selenium_driver.find_element(By.ID, "submit_inquiry").click()

        # Then: 에러 메시지 표시
        wait = WebDriverWait(selenium_driver, 5)
        error_msg = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inquiry-error"))
        )
        assert "유효한 이메일" in error_msg.text


@pytest.mark.e2e
class TestCustomerInquiryAPI:
    """고객 문의 API E2E 테스트"""

    def test_api_accepts_valid_inquiry(self, client):
        """API가 유효한 문의를 수락한다"""
        # Given
        inquiry_data = {
            "customer_email": "customer@example.com",
            "message": "When will my order arrive?"
        }

        # When
        response = client.post("/api/inquiries", json=inquiry_data)

        # Then
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "success"
        assert "inquiry_id" in data

    def test_api_rejects_invalid_email(self, client):
        """API가 잘못된 이메일을 거부한다"""
        # Given
        invalid_data = {
            "customer_email": "invalid-email",
            "message": "Test message"
        }

        # When
        response = client.post("/api/inquiries", json=invalid_data)

        # Then
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_api_rejects_empty_message(self, client):
        """API가 빈 메시지를 거부한다"""
        # Given
        invalid_data = {
            "customer_email": "customer@example.com",
            "message": ""
        }

        # When
        response = client.post("/api/inquiries", json=invalid_data)

        # Then
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
