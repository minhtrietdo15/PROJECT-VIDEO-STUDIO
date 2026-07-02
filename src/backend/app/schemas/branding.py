"""
Branding Pydantic Schemas
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.common import TimestampedModel


class BrandingResponse(TimestampedModel):
    id: str
    project_id: str
    intro_enabled: bool
    outro_enabled: bool
    watermark_enabled: bool
    bg_music_enabled: bool
    watermark_config: Optional[dict[str, Any]] = None
    bg_music_volume: float

    model_config = ConfigDict(from_attributes=True)