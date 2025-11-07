"""E2E 테스트용 Playwright fixture"""
import pytest
from playwright.sync_api import Page, Browser, BrowserContext
from typing import Generator


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, base_url: str) -> dict:
    """Playwright 브라우저 컨텍스트 설정"""
    return {
        **browser_context_args,
        "base_url": base_url,
    }


@pytest.fixture(scope="function")
def context(
    browser: Browser,
    browser_context_args: dict,
) -> Generator[BrowserContext, None, None]:
    """각 테스트마다 새로운 브라우저 컨텍스트 생성"""
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """각 테스트마다 새로운 페이지 생성"""
    page = context.new_page()
    yield page
    page.close()
