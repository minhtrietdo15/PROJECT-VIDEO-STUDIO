"""
Voice Profile Pydantic Schemas
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.common import TimestampedModel


class VoiceProfileResponse(TimestampedModel):
    id: str
    user_id: str
    name: str
    engine: str
    voice_id: str
    language: str
    gender: Optional[str] = None
    description: Optional[str] = None
    preview_path: Optional[str] = None
    is_cloned: bool
    config: Optional[dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class VoiceProfileCreate(BaseModel):
    name: str
    engine: str
    voice_id: str
    language: str = "vi"
    gender: Optional[str] = None
    description: Optional[str] = None
    config: Optional[dict[str, Any]] = None


class VoiceProfileUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[dict[str, Any]] = None