"""
Translation Celery Task
"""

from app.tasks.base import BaseTask
from app.tasks.celery_app import celery_app


@celery_app.task(base=BaseTask, bind=True)
def translation_task(self, project_id: str, style: str = "neutral"):
    """Translate transcript to Vietnamese."""
    raise NotImplementedError("Translation task not yet implemented")