"""
Dubbing Pydantic Schemas
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.models.dubbing import DubbingStatus
from app.schemas.common import TimestampedModel


class DubbingResponse(TimestampedModel):
    id: str
    project_id: str
    status: DubbingStatus
    voice_id: Optional[str] = None
    voice_name: Optional[str] = None
    engine_used: Optional[str] = None
    audio_path: Optional[str] = None
    speed: float
    pitch: float
    volume: float
    segments: Optional[list[dict[str, Any]]] = None

    model_config = ConfigDict(from_attributes=True)