"""
Transcript Pydantic Schemas
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.models.transcript import TranscriptStatus
from app.schemas.common import TimestampedModel


class TranscriptResponse(TimestampedModel):
    id: str
    project_id: str
    status: TranscriptStatus
    language: Optional[str] = None
    model_used: Optional[str] = None
    segments: Optional[list[dict[str, Any]]] = None
    raw_text: Optional[str] = None
    duration_seconds: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)