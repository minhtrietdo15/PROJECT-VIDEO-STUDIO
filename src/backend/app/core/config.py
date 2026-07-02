"""
Application Configuration Management
Uses pydantic-settings for typed, validated settings from env vars / .env
"""

from pathlib import Path
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ─── App Metadata ────────────────────────────────────────
    PROJECT_NAME: str = "Video Localization AI Studio"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "AI-powered video localization pipeline for Vietnamese content creators"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # ─── API Configuration ───────────────────────────────────
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # ─── Database ────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/videostudio"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # ─── Redis ───────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ─── Celery ──────────────────────────────────────────────
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    CELERY_TASK_TRACK_STARTED: bool = True
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: List[str] = ["json"]
    CELERY_WORKER_CONCURRENCY: int = 4
    CELERY_MAX_RETRIES: int = 3

    # ─── Authentication ──────────────────────────────────────
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ─── File Storage ────────────────────────────────────────
    DATA_ROOT: Path = Path("/data")
    UPLOAD_DIR: Path = Path("/data/projects")
    TEMPLATE_DIR: Path = Path("/data/templates")
    VOICE_PROFILE_DIR: Path = Path("/data/voice-profiles")
    EXPORT_DIR: Path = Path("/data/exports")
    CACHE_DIR: Path = Path("/data/cache")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024 * 1024  # 10GB
    ALLOWED_VIDEO_FORMATS: List[str] = [
        "mp4", "mov", "mkv", "avi", "webm"
    ]

    # ─── GPU / AI ────────────────────────────────────────────
    WHISPER_MODEL: str = "medium"
    WHISPER_MODEL_DIR: Optional[Path] = None
    TTS_ENGINE: str = "edge-tts"
    GPU_ENABLED: bool = False
    CUDA_DEVICE: int = 0

    # ─── Logging ─────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    SENTRY_DSN: Optional[str] = None

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"


settings = Settings()