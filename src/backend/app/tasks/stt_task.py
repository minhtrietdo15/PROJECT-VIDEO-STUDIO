"""
Speech-to-Text Celery Task
Runs Whisper transcription asynchronously with progress reporting and retry logic.
"""

import logging

from app.services.stt_service import STTService
from app.tasks.base import BaseTask
from app.tasks.celery_app import celery_app
from app.models.base import get_session

logger = logging.getLogger(__name__)


@celery_app.task(base=BaseTask, bind=True, max_retries=3)
def stt_task(
    self,
    project_id: str,
    model_size: str = "medium",
    language: str | None = None,
    word_timestamps: bool = True,
) -> dict:
    """
    Celery task to transcribe a project's video audio.

    Args:
        project_id: UUID of the project.
        model_size: Whisper model size (tiny, base, small, medium, large).
        language: Optional ISO 639-1 language code.
        word_timestamps: Whether to include word-level timestamps.

    Returns:
        Dict with project_id, status, and segment count.
    """
    logger.info("Starting STT task for project %s with model %s", project_id, model_size)
    self.update_state(state="PROGRESS", meta={"progress": 10, "current_segment": 0, "eta": None})

    import asyncio

    async def _run() -> dict:
        async for db in get_session():
            service = STTService(db)
            transcript_result = await service.transcribe(
                project_id=project_id,
                model_size=model_size,
                language=language,
                word_timestamps=word_timestamps,
            )
            segment_count = len(transcript_result.segments or [])
            self.update_state(
                state="PROGRESS",
                meta={
                    "progress": 100,
                    "current_segment": segment_count,
                    "eta": 0,
                    "language": transcript_result.language,
                    "model_used": transcript_result.model_used,
                },
            )
            logger.info("STT completed for project %s: %s segments", project_id, segment_count)
            return {
                "project_id": project_id,
                "status": "completed",
                "segment_count": segment_count,
                "language": transcript_result.language,
                "model_used": transcript_result.model_used,
            }

    try:
        return asyncio.run(_run())
    except Exception as exc:
        logger.exception("STT task failed for project %s", project_id)
        try:
            raise self.retry(exc=exc)
        except Exception as retry_exc:  # noqa: BLE001
            logger.error("STT task retries exhausted for project %s", project_id)
            raise retry_exc from exc
