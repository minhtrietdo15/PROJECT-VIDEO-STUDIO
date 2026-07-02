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