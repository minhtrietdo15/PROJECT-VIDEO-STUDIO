"""
Dubbing Model
Stores TTS (text-to-speech) output configuration and audio paths
"""

from typing import Optional

from sqlalchemy import Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

import enum


class DubbingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Dubbing(Base, UUIDMixin, TimestampMixin):
    """Voice dubbing (TTS) configuration and output."""

    project_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    status: Mapped[DubbingStatus] = mapped_column(
        Enum(DubbingStatus, name="dubbing_status"),
        nullable=False,
        default=DubbingStatus.PENDING,
    )
    voice_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    voice_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    engine_used: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    audio_path: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    speed: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    pitch: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    volume: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    segments: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=list)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationship
    project = relationship("Project", back_populates="dubbing")

    def __repr__(self) -> str:
        return f"<Dubbing {self.project_id} ({self.status.value})>"