"""
Video Pydantic Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.common import TimestampedModel


class VideoResponse(TimestampedModel):
    id: str
    project_id: str
    filename: str
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    file_size: Optional[int] = None
    codec: Optional[str] = None
    thumbnail_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VideoUploadResponse(BaseModel):
    """Response after a successful video upload."""
    id: str
    project_id: str
    filename: str
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    file_size: Optional[int] = None
    codec: Optional[str] = None
    thumbnail_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VideoImportRequest(BaseModel):
    """Request body for URL import."""
    url: str
    filename: Optional[str] = None


class VideoImportResponse(BaseModel):
    """Response for URL import request (async)."""
    id: str
    project_id: str
    filename: str
    task_id: str
    status: str = "downloading"

    model_config = ConfigDict(from_attributes=True)


class VideoMetadataResponse(BaseModel):
    """Enriched video metadata with human-readable formatting."""
    id: str
    project_id: str
    filename: str
    duration_seconds: Optional[float] = None
    duration_formatted: Optional[str] = None
    resolution: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    file_size_bytes: Optional[int] = None
    file_size_formatted: Optional[str] = None
    codec: Optional[str] = None
    audio_codec: Optional[str] = None
    audio_channels: Optional[int] = None
    audio_sample_rate: Optional[int] = None
    thumbnail_url: Optional[str] = None
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)