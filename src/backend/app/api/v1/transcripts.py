"""
Transcripts API Router
Speech-to-text endpoints
"""

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.core.exceptions import (
    NotFoundException,
    ProjectNotFoundException,
    TaskInProgressException,
    ValidationException,
)
from app.models.project import Project, ProjectStatus
from app.schemas.transcript import TranscriptResponse
from app.services.stt_service import STTService
from app.tasks.stt_task import stt_task
from pydantic import BaseModel, Field

router = APIRouter()


class TranscribeRequest(BaseModel):
    """Request body for starting transcription."""

    model_size: str = Field(default="medium", pattern="^(tiny|base|small|medium|large)$")
    language: str | None = Field(default=None, max_length=10)
    word_timestamps: bool = Field(default=True)


@router.get("/{project_id}", response_model=TranscriptResponse)
async def get_transcript(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TranscriptResponse:
    """Get transcript for a project."""
    service = STTService(db)
    transcript = await service.get_transcript(project_id)
    if not transcript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transcript for project '{project_id}' not found",
        )
    return TranscriptResponse.model_validate(transcript)


@router.post("/{project_id}/transcribe", status_code=status.HTTP_202_ACCEPTED)
async def start_transcription(
    project_id: str,
    data: TranscribeRequest,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Start an asynchronous transcription task for a project.

    Validates the project state and dispatches a Celery STT task.
    """
    # Validate project exists and has imported video
    project = await db.get(Project, uuid.UUID(project_id))
    if not project:
        raise ProjectNotFoundException(project_id)

    if project.status in (ProjectStatus.TRANSCRIBING, ProjectStatus.TRANSLATING):
        raise TaskInProgressException("transcription")

    if project.status == ProjectStatus.DRAFT:
        raise ValidationException("Video must be imported before transcribing")

    # Dispatch Celery task
    task = stt_task.delay(
        project_id=project_id,
        model_size=data.model_size,
        language=data.language,
        word_timestamps=data.word_timestamps,
    )

    return {
        "success": True,
        "data": {
            "task_id": task.id,
            "status": "queued",
            "project_id": project_id,
            "model_size": data.model_size,
            "language": data.language,
        },
    }


@router.patch("/{project_id}/segments/{segment_index}", response_model=dict[str, Any])
async def update_transcript_segment(
    project_id: str,
    segment_index: int,
    data: dict[str, Any],
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Update a single transcript segment."""
    service = STTService(db)
    try:
        segment = await service.update_segment(
            project_id=project_id,
            segment_index=segment_index,
            text=data.get("text"),
            start_ms=data.get("start_ms"),
            end_ms=data.get("end_ms"),
        )
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    return {"success": True, "data": segment}


@router.post("/{project_id}/segments/{segment_index}/split", response_model=dict[str, Any])
async def split_transcript_segment(
    project_id: str,
    segment_index: int,
    data: dict[str, Any],
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Split a transcript segment at a given timestamp."""
    service = STTService(db)
    try:
        segments = await service.split_segment(
            project_id=project_id,
            segment_index=segment_index,
            split_at_ms=data["split_at_ms"],
        )
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="split_at_ms is required",
        ) from exc
    return {"success": True, "data": {"segments": segments}}


@router.post("/{project_id}/segments/{segment_index}/merge", response_model=dict[str, Any])
async def merge_transcript_segment(
    project_id: str,
    segment_index: int,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Merge a transcript segment with the next one."""
    service = STTService(db)
    try:
        segment = await service.merge_segment_with_next(
            project_id=project_id,
            segment_index=segment_index,
        )
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    return {"success": True, "data": segment}


