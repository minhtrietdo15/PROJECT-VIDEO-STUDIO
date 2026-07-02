"""
Branding Model
Stores intro/outro/watermark/bg-music configuration
"""

from typing import Optional

from sqlalchemy import Boolean, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Branding(Base, UUIDMixin, TimestampMixin):
    """Branding configuration for a project."""

    project_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    # Intro
    intro_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    intro_template_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    intro_duration: Mapped[float] = mapped_column(Float, default=5.0)

    # Outro
    outro_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    outro_template_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Watermark
    watermark_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    watermark_config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)

    # Background Music
    bg_music_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    bg_music_path: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    bg_music_volume: Mapped[float] = mapped_column(Float, default=0.3)

    # Relationship
    project = relationship("Project", back_populates="branding")

    def __repr__(self) -> str:
        return f"<Branding {self.project_id}>"