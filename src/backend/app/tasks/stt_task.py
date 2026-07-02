"""
Speech-to-Text Celery Task
"""

from app.tasks.base import BaseTask
from app.tasks.celery_app import celery_app


@celery_app.task(base=BaseTask, bind=True)
def stt_task(self, project_id: str, model_size: str = "medium"):
    """Transcribe video audio to text."""
    raise NotImplementedError("STT task not yet implemented")