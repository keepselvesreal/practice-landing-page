from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields in .env
    )

    # Database
    database_url: str

    # Gmail SMTP
    gmail_address: str
    gmail_app_password: str
    smtp_host: str
    smtp_port: int

    # Google Places API
    google_places_api_key: str

    # PayPal
    paypal_client_id: str
    paypal_client_secret: str
    paypal_api_base: str

    # Base URL (for CORS)
    base_url: str


settings = Settings()
