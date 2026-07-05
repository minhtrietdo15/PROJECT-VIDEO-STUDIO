"""
Batch Processing Model
"""

from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class BatchQueue(Base, UUIDMixin, TimestampMixin):
    """Batch queue for managing multiple projects processing."""

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_paused: Mapped[bool] = mapped_column(Boolean, default=False)
    max_concurrent: Mapped[int] = mapped_column(Integer, default=3)

    # Relationships
    items = relationship("BatchItem", back_populates="queue", cascade="all, delete-orphan")
    user = relationship("User", back_populates="batch_queues")

    def __repr__(self) -> str:
        return f"<BatchQueue {self.name}>"


class BatchItem(Base, UUIDMixin, TimestampMixin):
    """Individual item in a batch queue."""

    queue_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("batch_queues.id", ondelete="CASCADE"), nullable=False
    )
    project_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    priority: Mapped[int] = mapped_column(Integer, default=2)  # 1=high, 2=normal, 3=low
    status: Mapped[str] = mapped_column(String(20), default="pending")
    progress: Mapped[int] = mapped_column(Integer, default=0)
    eta: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    error_log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    queue = relationship("BatchQueue", back_populates="items")
    project = relationship("Project")

    def __repr__(self) -> str:
        return f"<BatchItem {self.project_id} in {self.queue_id}>"