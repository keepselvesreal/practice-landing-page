"""E2E 테스트: 주문 생성 전체 플로우 (UI → Backend → PayPal)

Outside-In TDD - 가장 단순한 성공 케이스
사용자가 랜딩 페이지에서 주문하고 PayPal로 결제하는 전체 시나리오
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_customer_can_create_order_and_pay_with_paypal(page: Page):
    """고객이 랜딩 페이지에서 주문을 생성하고 PayPal로 결제할 수 있다

    Given: 재고가 10개 있는 상품 "조선미녀 맑은쌀 선크림"
    When: 고객이 주문 정보를 입력하고 PayPal로 결제 완료
    Then: 주문이 생성되고, 주문 번호가 표시되며, 재고가 차감됨
    """
    # Given: 랜딩 페이지 방문
    page.goto("http://localhost:8000")

    # 상품 정보가 표시됨
    expect(page.locator("#product-name")).to_contain_text("조선미녀 맑은쌀 선크림")
    expect(page.locator("#product-price")).to_contain_text("575")

    # When: 고객 정보 입력
    page.fill("#customer_name", "Maria Santos")
    page.fill("#customer_email", "maria.santos@example.com")
    page.fill("#customer_phone", "+63-917-123-4567")
    page.fill("#shipping_address", "123 Rizal Avenue, Makati City, Metro Manila 1200")

    # 주문 수량 선택 (기본값 1)
    page.select_option("#quantity", "2")

    # 총액 표시 확인 (575 * 2 + 100 = 1,250 페소)
    expect(page.locator("#total_amount")).to_contain_text("1,250")

    # "Order Now" 버튼 클릭
    page.click("#order_button")

    # PayPal 결제 창으로 리다이렉트됨
    # NOTE: 실제 PayPal Sandbox는 외부 서비스이므로,
    # 일단은 PayPal Approval URL이 생성되는지만 확인
    # (PayPal 결제 완료는 나중에 Mock/Stub으로 처리 가능)
    page.wait_for_url("**/checkoutnow**", timeout=5000)

    # TODO: PayPal Sandbox에서 테스트 계정으로 로그인 및 결제 승인
    # 지금은 자동화가 복잡하므로, 일단 approval_url 생성까지만 테스트
    # PayPal 결제 부분은 Integration Test로 분리 예정

    # 임시로 return_url로 돌아오는 것 시뮬레이션
    # (실제로는 PayPal에서 승인 후 자동 리다이렉트)
    # page.goto("http://localhost:8000/order-complete?order_number=ORD-12345678")

    # Then: 주문 완료 페이지 표시
    # expect(page.locator("#order_complete_message")).to_be_visible()
    # expect(page.locator("#order_number")).to_contain_text("ORD-")

    # 임시로 여기까지만 - PayPal로 리다이렉트되는지 확인


@pytest.mark.e2e
def test_customer_sees_product_information_on_landing_page(page: Page):
    """고객이 랜딩 페이지에서 상품 정보를 볼 수 있다

    가장 단순한 케이스 - UI가 제대로 렌더링되는지 확인
    """
    # Given/When: 랜딩 페이지 방문
    page.goto("http://localhost:8000")

    # Then: 상품 정보 표시
    expect(page.locator("#product-name")).to_be_visible()
    expect(page.locator("#product-name")).to_contain_text("조선미녀 맑은쌀 선크림")
    expect(page.locator("#product-price")).to_contain_text("575")
    expect(page.locator("#shipping-fee")).to_contain_text("100")

    # 주문 폼 요소들이 존재
    expect(page.locator("#customer_name")).to_be_visible()
    expect(page.locator("#customer_email")).to_be_visible()
    expect(page.locator("#customer_phone")).to_be_visible()
    expect(page.locator("#shipping_address")).to_be_visible()
    expect(page.locator("#quantity")).to_be_visible()
    expect(page.locator("#order_button")).to_be_visible()
