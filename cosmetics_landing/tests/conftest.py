"""
Pytest Configuration
"""
import pytest
import os
import threading
import time
from pathlib import Path
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from selenium import webdriver
import uvicorn

from cosmetics_landing.config.main import create_app

# .env 파일 로드 (프로젝트 루트의 상위 디렉토리)
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


@pytest.fixture
def client():
    """
    FastAPI 테스트 클라이언트

    E2E 테스트용 애플리케이션 인스턴스
    """
    app = create_app()
    return TestClient(app)


@pytest.fixture
def valid_order_data():
    """유효한 주문 데이터"""
    return {
        "customer_email": "test@example.com",
        "customer_address": "123 Main St, Manila, Philippines",
        "product_price": 29.99
    }


@pytest.fixture
def order_with_affiliate():
    """어필리에이트 코드가 포함된 주문 데이터"""
    return {
        "customer_email": "test@example.com",
        "customer_address": "123 Main St, Manila, Philippines",
        "product_price": 29.99,
        "affiliate_code": "INFLUENCER123"
    }


@pytest.fixture(scope="session")
def live_server():
    """
    실제 서버를 백그라운드에서 실행하는 픽스처

    Selenium 테스트용 라이브 서버
    포트 충돌 방지를 위해 사용 가능한 포트 자동 탐색
    """
    import socket

    # 사용 가능한 포트 찾기
    def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port

    port = find_free_port()

    # 서버를 별도 스레드에서 실행
    server_thread = threading.Thread(
        target=uvicorn.run,
        args=(create_app(),),
        kwargs={
            "host": "127.0.0.1",
            "port": port,
            "log_level": "error"
        },
        daemon=True
    )
    server_thread.start()

    # 서버 시작 대기
    time.sleep(3)

    yield f"http://localhost:{port}"

    # 종료는 daemon 스레드이므로 자동으로 처리됨


@pytest.fixture
def selenium_driver():
    """
    Selenium WebDriver 설정

    Headless Chrome 브라우저 사용
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)  # 암묵적 대기 시간

    yield driver

    driver.quit()


# pytest marker 설정
def pytest_configure(config):
    """pytest 설정"""
    config.addinivalue_line(
        "markers", "learning: mark test as learning test (external API contract verification)"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (real external services)"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test (UI + API)"
    )
