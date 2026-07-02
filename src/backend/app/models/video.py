"""
Video Model
Stores metadata about uploaded video files
"""

from typing import Optional

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Video(Base, UUIDMixin, TimestampMixin):
    """Uploaded video metadata."""

    project_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    filepath: Mapped[str] = mapped_column(String(1000), nullable=False)
    duration: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    fps: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    codec: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    thumbnail_path: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    audio_codec: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    audio_channels: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    audio_sample_rate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationship
    project = relationship("Project", back_populates="video")

    def __repr__(self) -> str:
        return f"<Video {self.filename} ({self.width}x{self.height})>"