"""
YouTube Metadata Model
Stores YouTube publishing metadata
"""

from typing import Optional

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

import enum


class VisibilityType(str, enum.Enum):
    PUBLIC = "public"
    UNLISTED = "unlisted"
    PRIVATE = "private"


class YouTubeMetadata(Base, UUIDMixin, TimestampMixin):
    """YouTube publishing metadata."""

    project_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=list)
    category_id: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    visibility: Mapped[VisibilityType] = mapped_column(
        Enum(VisibilityType, name="visibility_type"),
        nullable=False,
        default=VisibilityType.PRIVATE,
    )
    playlist_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    chapters: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=list)
    thumbnail_path: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    exported_metadata_path: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    def __repr__(self) -> str:
        return f"<YouTubeMetadata {self.project_id}>"