"""
Base Celery Task Class
Common task functionality and error handling
"""

import logging
from typing import Any, Dict, Optional

from celery import Task
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


class BaseTask(Task):
    """Base task with common error handling and retry logic."""

    autoretry_for = (Exception,)
    max_retries = settings.CELERY_MAX_RETRIES
    default_retry_delay = 60

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log task failure."""
        logger.error("Task %s failed: %s", task_id, exc)

    def on_success(self, retval, task_id, args, kwargs):
        """Log task success."""
        logger.info("Task %s completed successfully", task_id)


# Alias for convenience
TaskBase = BaseTask