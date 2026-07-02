"""
Text-to-Speech Service
TTS engine integration stub
"""

from sqlalchemy.ext.asyncio import AsyncSession


class TTSService:
    """Service layer for text-to-speech operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_audio(self, project_id: str, voice_id: str, text: str):
        """Generate audio from text using TTS."""
        raise NotImplementedError("TTS not yet implemented")