"""
Render Service
Video rendering/export stub
"""

from sqlalchemy.ext.asyncio import AsyncSession


class RenderService:
    """Service layer for video rendering operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def start_render(self, project_id: str, settings: dict):
        """Start video rendering process."""
        raise NotImplementedError("Render not yet implemented")