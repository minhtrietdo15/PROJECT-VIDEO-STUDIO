"""
YouTube Service
YouTube metadata management stub
"""

from sqlalchemy.ext.asyncio import AsyncSession


class YouTubeService:
    """Service layer for YouTube operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_metadata(self, project_id: str):
        """Get YouTube metadata for a project."""
        raise NotImplementedError("YouTube service not yet implemented")

    async def update_metadata(self, project_id: str, metadata: dict):
        """Update YouTube metadata for a project."""
        raise NotImplementedError("YouTube service not yet implemented")