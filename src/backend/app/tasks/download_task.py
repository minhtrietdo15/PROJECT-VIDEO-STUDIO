"""
Download Celery Task
URL import/download stub
"""

from app.tasks.base import BaseTask
from app.tasks.celery_app import celery_app


@celery_app.task(base=BaseTask, bind=True)
def download_task(self, project_id: str, url: str):
    """Download video from URL."""
    raise NotImplementedError("Download task not yet implemented")