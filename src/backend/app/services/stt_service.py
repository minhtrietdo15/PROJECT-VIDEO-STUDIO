"""
Speech-to-Text Service
Whisper integration stub
"""

from sqlalchemy.ext.asyncio import AsyncSession


class STTService:
    """Service layer for speech-to-text operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def transcribe(self, project_id: str, model_size: str = "medium"):
        """Transcribe video audio to text."""
        raise NotImplementedError("STT not yet implemented")