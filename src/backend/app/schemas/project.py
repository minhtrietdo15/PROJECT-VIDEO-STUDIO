"""
Project Pydantic Schemas
Request/response models for project endpoints
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.project import ProjectStatus
from app.schemas.common import TimestampedModel


class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    source_lang: str = Field(default="auto", max_length=10)
    target_lang: str = Field(default="vi", max_length=10)
    description: Optional[str] = None
    settings: Optional[dict[str, Any]] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    source_lang: Optional[str] = Field(None, max_length=10)
    target_lang: Optional[str] = Field(None, max_length=10)
    description: Optional[str] = None
    settings: Optional[dict[str, Any]] = None
    status: Optional[ProjectStatus] = None


class ProjectResponse(ProjectBase, TimestampedModel):
    id: str
    user_id: str
    status: ProjectStatus

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    @field_validator('id', mode='before')
    @classmethod
    def id_to_str(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]
    total: int
    page: int
    page_size: int
    pages: int
