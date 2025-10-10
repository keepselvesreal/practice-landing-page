"""
UI 인수 테스트: 사용자 주문 폼 제출 시나리오
GOOS Chapter 11: First End-to-End Test
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.e2e
class TestOrderFormUI:
    """
    브라우저 레벨 인수 테스트

    GOOS: 사용자 관점에서 전체 시스템 동작 검증
    """

    def test_user_can_submit_order_form(self, selenium_driver, live_server):
        """
        인수 테스트: 사용자가 주문 폼을 작성하고 제출할 수 있다

        GOOS: Outside-in, 사용자 시나리오부터 시작
        """
        # Given: 랜딩 페이지 방문
        selenium_driver.get(f"{live_server}/")

        # When: 주문 폼 작성
        selenium_driver.find_element(By.ID, "customer_email").send_keys("test@example.com")
        selenium_driver.find_element(By.ID, "customer_address").send_keys("123 Main St, Manila, Philippines")
        selenium_driver.find_element(By.ID, "product_price").send_keys("29.99")
        selenium_driver.find_element(By.ID, "submit_order").click()

        # Then: 성공 메시지 표시
        wait = WebDriverWait(selenium_driver, 10)
        success_msg = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "주문이 완료되었습니다" in success_msg.text

    def test_user_can_submit_order_with_affiliate_code(self, selenium_driver, live_server):
        """
        인수 테스트: 사용자가 어필리에이트 코드와 함께 주문할 수 있다

        Epic 2: 어필리에이트 통합 시나리오
        """
        # Given: 랜딩 페이지 방문
        selenium_driver.get(f"{live_server}/")

        # When: 어필리에이트 코드를 포함한 주문 폼 작성
        selenium_driver.find_element(By.ID, "customer_email").send_keys("customer@example.com")
        selenium_driver.find_element(By.ID, "customer_address").send_keys("Seoul, Korea")
        selenium_driver.find_element(By.ID, "product_price").send_keys("150.00")
        selenium_driver.find_element(By.ID, "affiliate_code").send_keys("INFLUENCER123")
        selenium_driver.find_element(By.ID, "submit_order").click()

        # Then: 성공 메시지 표시
        wait = WebDriverWait(selenium_driver, 10)
        success_msg = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "주문이 완료되었습니다" in success_msg.text

    def test_landing_page_displays_order_form(self, selenium_driver, live_server):
        """
        랜딩 페이지에 주문 폼이 표시된다

        기본 UI 요소 검증
        """
        # Given & When: 랜딩 페이지 방문
        selenium_driver.get(f"{live_server}/")

        # Then: 주문 폼 요소들이 표시됨
        assert selenium_driver.find_element(By.ID, "customer_email").is_displayed()
        assert selenium_driver.find_element(By.ID, "customer_address").is_displayed()
        assert selenium_driver.find_element(By.ID, "product_price").is_displayed()
        assert selenium_driver.find_element(By.ID, "affiliate_code").is_displayed()
        assert selenium_driver.find_element(By.ID, "submit_order").is_displayed()
