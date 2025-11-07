"""E2E 테스트용 conftest

Playwright를 사용한 UI 레벨 E2E 테스트 설정
"""
import pytest
from playwright.sync_api import Page, Browser


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """브라우저 컨텍스트 설정"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope="function")
def page(page: Page):
    """Playwright page fixture

    pytest-playwright가 자동으로 제공하는 page fixture를 그대로 사용
    """
    yield page
