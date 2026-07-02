"""
Chat Service
AI assistant service stub
"""

from sqlalchemy.ext.asyncio import AsyncSession


class ChatService:
    """Service layer for AI assistant operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def send_message(self, user_id: str, message: str, project_id: str | None = None):
        """Send a message to the AI assistant."""
        raise NotImplementedError("Chat not yet implemented")