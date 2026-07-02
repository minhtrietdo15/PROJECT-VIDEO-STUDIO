"""
Render Celery Task
"""

from app.tasks.base import BaseTask
from app.tasks.celery_app import celery_app


@celery_app.task(base=BaseTask, bind=True)
def render_task(self, project_id: str, settings: dict):
    """Render final video."""
    raise NotImplementedError("Render task not yet implemented")