"""
TTS Celery Task
"""

from app.tasks.base import BaseTask
from app.tasks.celery_app import celery_app


@celery_app.task(base=BaseTask, bind=True)
def tts_task(self, project_id: str, voice_id: str):
    """Generate dubbed audio for a project."""
    raise NotImplementedError("TTS task not yet implemented")