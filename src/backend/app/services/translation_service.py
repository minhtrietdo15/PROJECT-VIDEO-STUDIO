"""
Translation Service
LLM-based translation stub
"""

from sqlalchemy.ext.asyncio import AsyncSession


class TranslationService:
    """Service layer for translation operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def translate(self, project_id: str, style: str = "neutral"):
        """Translate transcript to Vietnamese."""
        raise NotImplementedError("Translation not yet implemented")