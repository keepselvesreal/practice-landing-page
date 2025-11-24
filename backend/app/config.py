import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# ENV 환경변수로 .env 파일 동적 선택
# - ENV 있음: .env.{ENV} 파일 로드 (예: ENV=test → .env.test, ENV=docker → .env.docker)
# - ENV 없음: 환경변수만 사용 (Cloud Run 배포 환경)
# - 파일 없음: 환경변수만 사용
env = os.getenv("ENV")
if env:
    env_file = Path(__file__).parent.parent / f".env.{env}"
    env_file_path = str(env_file) if env_file.exists() else None
else:
    # 배포 환경: .env 파일 없이 환경변수만 사용
    env_file_path = None


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields in .env
    )

    # Database
    database_url: str

    # Gmail SMTP
    gmail_address: str
    gmail_app_password: str
    smtp_host: str = "smtp.gmail.com"  # Gmail SMTP 고정값
    smtp_port: int = 587  # TLS 포트 고정값

    # Google Places API
    google_places_api_key: str

    # PayPal
    paypal_client_id: str
    paypal_client_secret: str
    paypal_api_base: str

    # Base URL (for CORS)
    base_url: str


settings = Settings()
