"""
Render Pydantic Schemas
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.models.render_task import RenderStatus
from app.schemas.common import TimestampedModel


class RenderTaskResponse(TimestampedModel):
    id: str
    project_id: str
    status: RenderStatus
    progress: float
    output_path: Optional[str] = None
    settings: Optional[dict[str, Any]] = None
    error_log: Optional[str] = None
    duration_seconds: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class RenderRequest(BaseModel):
    project_id: str
    format: str = "mp4"
    resolution: str = "1080p"
    quality_preset: str = "balanced"
    burn_subtitles: bool = False
    include_branding: bool = True