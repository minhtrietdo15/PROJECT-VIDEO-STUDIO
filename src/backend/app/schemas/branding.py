"""
Branding Pydantic Schemas
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import TimestampedModel


class BrandingBase(BaseModel):
    intro_enabled: bool = True
    outro_enabled: bool = True
    watermark_enabled: bool = False
    bg_music_enabled: bool = False
    intro_config: Optional[dict[str, Any]] = None
    outro_config: Optional[dict[str, Any]] = None
    watermark_config: Optional[dict[str, Any]] = None
    bg_music_config: Optional[dict[str, Any]] = None
    bg_music_volume: float = Field(default=50.0, ge=0.0, le=100.0)


class BrandingCreate(BrandingBase):
    project_id: str


class BrandingUpdate(BaseModel):
    intro_enabled: Optional[bool] = None
    outro_enabled: Optional[bool] = None
    watermark_enabled: Optional[bool] = None
    bg_music_enabled: Optional[bool] = None
    intro_config: Optional[dict[str, Any]] = None
    outro_config: Optional[dict[str, Any]] = None
    watermark_config: Optional[dict[str, Any]] = None
    bg_music_config: Optional[dict[str, Any]] = None
    bg_music_volume: Optional[float] = Field(None, ge=0.0, le=100.0)


class BrandingResponse(BrandingBase, TimestampedModel):
    id: str
    project_id: str

    model_config = ConfigDict(from_attributes=True)