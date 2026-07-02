"""
Subtitle Service
Subtitle generation and styling stub
"""

from sqlalchemy.ext.asyncio import AsyncSession


class SubtitleService:
    """Service layer for subtitle operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_subtitles(self, project_id: str, format: str = "srt"):
        """Generate subtitles from translation segments."""
        raise NotImplementedError("Subtitle generation not yet implemented")