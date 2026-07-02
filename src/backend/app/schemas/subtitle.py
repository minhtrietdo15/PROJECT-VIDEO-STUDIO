"""
Subtitle Pydantic Schemas
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.models.subtitle import SubtitleFormat
from app.schemas.common import TimestampedModel


class SubtitleResponse(TimestampedModel):
    id: str
    project_id: str
    format: SubtitleFormat
    content: Optional[list[dict[str, Any]]] = None
    style_config: Optional[dict[str, Any]] = None
    file_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)