from __future__ import annotations
import os
from datetime import timedelta

class BaseConfig:
    def __init__(self, s):
        self.SECRET_KEY = s.SECRET_KEY
        self.SQLALCHEMY_DATABASE_URI = (
            f"postgresql+psycopg://{s.POSTGRES_USER}:{s.POSTGRES_PASSWORD}@{s.POSTGRES_HOST}:{s.POSTGRES_PORT}/{s.POSTGRES_DB}"
        )
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.JWT_SECRET_KEY = s.JWT_SECRET_KEY
        self.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=s.JWT_ACCESS_TOKEN_EXPIRES_MIN)
        self.CACHE_TYPE = "RedisCache"
        self.CACHE_REDIS_URL = s.REDIS_URL
        self.RATELIMIT_STORAGE_URI = s.REDIS_URL
        self.SESSION_COOKIE_SECURE = False
        self.PROPAGATE_EXCEPTIONS = True
        self.API_TITLE = "Task Planner API"
        self.API_VERSION = "v1"
        self.OPENAPI_VERSION = "3.0.3"
        self.OPENAPI_URL_PREFIX = "/api/docs"
        self.OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
        self.OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
        self.SOCKETIO_REDIS = s.REDIS_URL
        self.CORS_ALLOW_ORIGINS = s.CORS_ALLOW_ORIGINS
        self.LLM_PROVIDER = s.LLM_PROVIDER
        self.OPENAI_API_KEY = s.OPENAI_API_KEY
        self.STRIPE_SECRET_KEY = s.STRIPE_SECRET_KEY
        self.STRIPE_PRICE_ID_INR = s.STRIPE_PRICE_ID_INR

class DevConfig(BaseConfig):
    def __init__(self, s):
        super().__init__(s)
        self.DEBUG = True

class ProdConfig(BaseConfig):
    def __init__(self, s):
        super().__init__(s)
        self.SESSION_COOKIE_SECURE = True
