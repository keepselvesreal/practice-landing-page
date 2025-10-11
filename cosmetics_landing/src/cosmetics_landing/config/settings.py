"""
Application Settings
"""
from pydantic_settings import BaseSettings
from decimal import Decimal


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # Application
    app_name: str = "Cosmetics Landing Page"
    debug: bool = True

    # Product
    product_price: Decimal = Decimal("29.99")
    commission_rate: Decimal = Decimal("0.20")

    # Database (추후 실제 DB 사용 시)
    database_url: str = "sqlite:///./cosmetics_landing.db"

    # PayPal (추후 실제 PayPal 사용 시)
    paypal_client_id: str = ""
    paypal_client_secret: str = ""
    paypal_mode: str = "sandbox"

    # Google Places API (추후 실제 API 사용 시)
    google_places_api_key: str = ""

    # Email (추후 실제 이메일 사용 시)
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    support_email: str = "support@cosmetics.com"

    # AI API Keys (선택사항)
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    gemini_api_key: str = ""

    # PayPal Sandbox (선택사항)
    paypal_sandbox_client_id: str = ""
    paypal_sandbox_client_secret: str = ""

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"  # .env의 추가 필드 허용
    }


def get_settings() -> Settings:
    """설정 싱글톤"""
    return Settings()
