"""
Batch Processing Celery Task
"""

from app.tasks.base import BaseTask
from app.tasks.celery_app import celery_app


@celery_app.task(base=BaseTask, bind=True)
def batch_task(self, project_ids: list[str]):
    """Process multiple projects in batch."""
    raise NotImplementedError("Batch task not yet implemented")