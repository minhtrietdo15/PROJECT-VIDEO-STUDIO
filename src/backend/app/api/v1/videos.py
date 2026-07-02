"""
Videos API Router
Video upload, metadata, and management
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.schemas.video import VideoResponse, VideoUploadResponse, VideoImportResponse, VideoMetadataResponse
from app.services.video_service import VideoService

router = APIRouter()


@router.post("/{project_id}/upload", response_model=VideoUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_video(
    project_id: str,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VideoUploadResponse:
    """
    Upload a video file to a project.

    Supports MP4, MOV, MKV, AVI, WebM formats.
    Maximum file size: 10GB.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided",
        )

    content = await file.read()

    service = VideoService(db)
    try:
        video = await service.upload_video(
            project_id=project_id,
            filename=file.filename,
            content=content,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return VideoUploadResponse(
        id=str(video.id),
        project_id=str(video.project_id),
        filename=video.filename,
        duration=video.duration,
        width=video.width,
        height=video.height,
        fps=video.fps,
        file_size=video.file_size,
        codec=video.codec,
        thumbnail_url=f"/api/v1/files/{project_id}/thumbnail.jpg" if video.thumbnail_path else None,
    )


@router.post("/{project_id}/import-url", response_model=VideoImportResponse, status_code=status.HTTP_202_ACCEPTED)
async def import_video_from_url(
    project_id: str,
    url: str = Form(...),
    filename: str = Form(None),
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VideoImportResponse:
    """
    Import a video from a URL.

    The actual download happens asynchronously via Celery.
    Returns a task_id for tracking download progress.
    """
    service = VideoService(db)
    video, task_id = await service.create_from_url(
        project_id=project_id,
        url=url,
        filename=filename,
    )

    return VideoImportResponse(
        id=str(video.id),
        project_id=str(video.project_id),
        filename=video.filename,
        task_id=task_id,
        status="downloading",
    )


@router.get("/{project_id}", response_model=VideoResponse)
async def get_video(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VideoResponse:
    """Get video metadata for a project."""
    service = VideoService(db)
    video = await service.get_video(project_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found for this project",
        )
    return VideoResponse(
        id=str(video.id),
        project_id=str(video.project_id),
        filename=video.filename,
        duration=video.duration,
        width=video.width,
        height=video.height,
        fps=video.fps,
        file_size=video.file_size,
        codec=video.codec,
        thumbnail_path=video.thumbnail_path,
    )


@router.get("/{project_id}/metadata", response_model=VideoMetadataResponse)
async def get_video_metadata(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VideoMetadataResponse:
    """Get enriched video metadata with human-readable formatting."""
    service = VideoService(db)
    metadata = await service.get_video_metadata(project_id)
    if not metadata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found for this project",
        )
    return VideoMetadataResponse(**metadata)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a video and its associated files."""
    service = VideoService(db)
    deleted = await service.delete_video(project_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found for this project",
        )