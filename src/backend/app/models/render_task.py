"""
RenderTask Model
Tracks video rendering/export jobs
"""

from typing import Optional

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

import enum


class RenderStatus(str, enum.Enum):
    PENDING = "pending"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RenderTask(Base, UUIDMixin, TimestampMixin):
    """Video rendering/export task."""

    project_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[RenderStatus] = mapped_column(
        Enum(RenderStatus, name="render_status"),
        nullable=False,
        default=RenderStatus.PENDING,
        index=True,
    )
    progress: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    output_path: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    settings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    error_log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    started_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    completed_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relationship
    project = relationship("Project", back_populates="render_tasks")

    def __repr__(self) -> str:
        return f"<RenderTask {self.id} ({self.status.value})>"