"""
Translation Model
Stores translated transcript segments
"""

from typing import Optional

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

import enum


class TranslationStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Translation(Base, UUIDMixin, TimestampMixin):
    """Translated transcript output."""

    project_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    transcript_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transcripts.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[TranslationStatus] = mapped_column(
        Enum(TranslationStatus, name="translation_status"),
        nullable=False,
        default=TranslationStatus.PENDING,
    )
    translated_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    segments: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=list)
    style: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    engine_used: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    project = relationship("Project", back_populates="translation")
    transcript = relationship("Transcript", back_populates="translation")

    def __repr__(self) -> str:
        return f"<Translation {self.project_id} ({self.status.value})>"