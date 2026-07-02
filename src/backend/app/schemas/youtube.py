"""
YouTube Metadata Pydantic Schemas
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.models.youtube_metadata import VisibilityType
from app.schemas.common import TimestampedModel


class YouTubeMetadataResponse(TimestampedModel):
    id: str
    project_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    category_id: Optional[str] = None
    visibility: VisibilityType
    playlist_id: Optional[str] = None
    chapters: Optional[list[dict[str, Any]]] = None
    thumbnail_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)