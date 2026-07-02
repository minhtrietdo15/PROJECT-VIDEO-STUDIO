"""
Subtitle Model
Stores generated subtitle content and styling configuration
"""

from typing import Optional

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

import enum


class SubtitleFormat(str, enum.Enum):
    SRT = "srt"
    ASS = "ass"
    VTT = "vtt"
    SSA = "ssa"


class Subtitle(Base, UUIDMixin, TimestampMixin):
    """Generated subtitle file."""

    project_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    format: Mapped[SubtitleFormat] = mapped_column(
        Enum(SubtitleFormat, name="subtitle_format"),
        nullable=False,
        default=SubtitleFormat.SRT,
    )
    content: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=list)
    style_config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    file_path: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    # Relationship
    project = relationship("Project", back_populates="subtitle")

    def __repr__(self) -> str:
        return f"<Subtitle {self.project_id} ({self.format.value})>"