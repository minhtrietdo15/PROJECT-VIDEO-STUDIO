"""
Project Model
Core entity representing a video localization project
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

import enum


class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    VIDEO_IMPORTED = "video_imported"
    TRANSCRIBING = "transcribing"
    TRANSCRIPT_READY = "transcript_ready"
    TRANSLATING = "translating"
    TRANSLATION_READY = "translation_ready"
    DUBBING = "dubbing"
    DUBBING_READY = "dubbing_ready"
    RENDERING = "rendering"
    COMPLETED = "completed"
    FAILED = "failed"


class Project(Base, UUIDMixin, TimestampMixin):
    """A video localization project."""

    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    source_lang: Mapped[str] = mapped_column(String(10), nullable=False, default="auto")
    target_lang: Mapped[str] = mapped_column(String(10), nullable=False, default="vi")
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status"),
        nullable=False,
        default=ProjectStatus.DRAFT,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    settings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)

    # Relationships
    video = relationship("Video", back_populates="project", uselist=False, cascade="all, delete-orphan")
    transcript = relationship("Transcript", back_populates="project", uselist=False, cascade="all, delete-orphan")
    translation = relationship("Translation", back_populates="project", uselist=False, cascade="all, delete-orphan")
    dubbing = relationship("Dubbing", back_populates="project", uselist=False, cascade="all, delete-orphan")
    subtitle = relationship("Subtitle", back_populates="project", uselist=False, cascade="all, delete-orphan")
    branding = relationship("Branding", back_populates="project", uselist=False, cascade="all, delete-orphan")
    render_tasks = relationship("RenderTask", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Project {self.title} ({self.status.value})>"