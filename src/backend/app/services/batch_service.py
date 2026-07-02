"""
Batch Service
Batch processing orchestration stub
"""

from sqlalchemy.ext.asyncio import AsyncSession


class BatchService:
    """Service layer for batch processing operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_batch(self, user_id: str, project_ids: list[str]):
        """Create a batch processing job."""
        raise NotImplementedError("Batch processing not yet implemented")