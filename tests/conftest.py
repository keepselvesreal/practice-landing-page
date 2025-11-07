"""전역 pytest fixture 설정"""
import os
from pathlib import Path
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# .env 파일 로드
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


@pytest.fixture(scope="session")
def base_url() -> str:
    """테스트용 기본 URL"""
    return "http://localhost:8000"


@pytest.fixture(scope="function")
def test_client() -> Generator[TestClient, None, None]:
    """FastAPI TestClient fixture"""
    from backend.main import app

    yield TestClient(app)
