"""
Application Lifecycle Events
Startup/shutdown hooks for database, Redis, Celery connections
"""

import logging
from typing import Any

from fastapi import FastAPI

from app.core.config import settings

logger = logging.getLogger(__name__)


class LifespanEvents:
    """Manage application startup and shutdown lifecycle."""

    async def startup(self, app: FastAPI) -> None:
        """Initialize connections and resources on startup."""
        logger.info("Starting %s v%s", settings.PROJECT_NAME, settings.VERSION)
        logger.info("Environment: %s", settings.ENVIRONMENT)

        # Ensure data directories exist
        self._ensure_directories()

        # Database connection pool is managed by SQLAlchemy
        # Redis connection is managed by Celery / aioredis
        logger.info("Startup complete")

    async def shutdown(self, app: FastAPI) -> None:
        """Clean up connections and resources on shutdown."""
        logger.info("Shutting down %s", settings.PROJECT_NAME)
        logger.info("Shutdown complete")

    def _ensure_directories(self) -> None:
        """Create required data directories if they don't exist."""
        directories = [
            settings.UPLOAD_DIR,
            settings.TEMPLATE_DIR,
            settings.VOICE_PROFILE_DIR,
            settings.EXPORT_DIR,
            settings.CACHE_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug("Ensured directory: %s", directory)


lifespan_events = LifespanEvents()