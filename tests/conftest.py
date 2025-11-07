"""전역 pytest fixture 설정"""
import pytest
from typing import Generator
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def base_url() -> str:
    """테스트용 기본 URL"""
    return "http://localhost:8000"


@pytest.fixture(scope="function")
def test_client() -> Generator[TestClient, None, None]:
    """FastAPI TestClient fixture"""
    # 나중에 backend.main:app이 생성되면 import
    # from backend.main import app
    # yield TestClient(app)

    # 현재는 더미 반환
    pass
