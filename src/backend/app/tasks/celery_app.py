"""
Celery Application Configuration
Task queue setup for async processing
"""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "videostudio",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_RESULT_SERIALIZER,
    accept_content=settings.CELERY_ACCEPT_CONTENT,
    task_track_started=settings.CELERY_TASK_TRACK_STARTED,
    worker_concurrency=settings.CELERY_WORKER_CONCURRENCY,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_default_retry_delay=60,
    task_max_retries=settings.CELERY_MAX_RETRIES,
)

# Auto-discover tasks
celery_app.autodiscover_tasks(["app.tasks"])