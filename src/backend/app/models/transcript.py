"""
Transcript Model
Stores speech-to-text output segments
"""

from typing import Optional

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

import enum


class TranscriptStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Transcript(Base, UUIDMixin, TimestampMixin):
    """Speech-to-text transcript output."""

    project_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    status: Mapped[TranscriptStatus] = mapped_column(
        Enum(TranscriptStatus, name="transcript_status"),
        nullable=False,
        default=TranscriptStatus.PENDING,
    )
    language: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    segments: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=list)
    raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationship
    project = relationship("Project", back_populates="transcript")
    translation = relationship("Translation", back_populates="transcript", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Transcript {self.project_id} ({self.status.value})>"