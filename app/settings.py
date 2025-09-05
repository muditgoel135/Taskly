from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    FLASK_ENV: str = "development"
    SECRET_KEY: str = "dev-secret-change"

    # DB/Redis
    POSTGRES_USER: str = "planner"
    POSTGRES_PASSWORD: str = "planner"
    POSTGRES_DB: str = "planner"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    REDIS_URL: str = "redis://redis:6379/0"

    # JWT
    JWT_SECRET_KEY: str = "jwt-dev-change"
    JWT_ACCESS_TOKEN_EXPIRES_MIN: int = 30

    # LLM
    LLM_PROVIDER: str = "LOCAL"  # OPENAI|LOCAL
    OPENAI_API_KEY: str | None = None

    # Stripe (test)
    STRIPE_SECRET_KEY: str | None = None
    STRIPE_PRICE_ID_INR: str | None = None

    # CORS origins
    CORS_ALLOW_ORIGINS: str = "*"

    # Email (optional)
    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None

