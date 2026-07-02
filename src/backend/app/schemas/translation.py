"""
Translation Pydantic Schemas
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.models.translation import TranslationStatus
from app.schemas.common import TimestampedModel


class TranslationResponse(TimestampedModel):
    id: str
    project_id: str
    transcript_id: str
    status: TranslationStatus
    translated_text: Optional[str] = None
    segments: Optional[list[dict[str, Any]]] = None
    style: Optional[str] = None
    engine_used: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)