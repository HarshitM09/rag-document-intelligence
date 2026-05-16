import os
from pathlib import Path
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")
    API_KEY: str = Field("enterprise-demo-key", env="API_KEY")
    VECTOR_DB_PATH: str = Field("./data/vector_store", env="VECTOR_DB_PATH")
    EMBEDDING_MODEL: str = Field("sentence-transformers/all-MiniLM-L6-v2", env="EMBEDDING_MODEL")
    MAX_CHUNK_SIZE: int = Field(800, env="MAX_CHUNK_SIZE")
    MIN_CHUNK_OVERLAP: int = Field(150, env="MIN_CHUNK_OVERLAP")
    MAX_CONTEXT_TOKENS: int = Field(2048, env="MAX_CONTEXT_TOKENS")
    ANALYTICS_ENABLED: bool = Field(True, env="ANALYTICS_ENABLED")
    GROQ_API_KEY: str = Field("", env="GROQ_API_KEY")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    SENTRY_DSN: str = Field("", env="SENTRY_DSN")
    ALLOWED_DOMAINS: str = Field("example.com,internal.example.com", env="ALLOWED_DOMAINS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


def get_allowed_domains():
    return [domain.strip() for domain in settings.ALLOWED_DOMAINS.split(",") if domain.strip()]
