"""
Branding Service
Branding configuration stub
"""

from sqlalchemy.ext.asyncio import AsyncSession


class BrandingService:
    """Service layer for branding operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_branding(self, project_id: str):
        """Get branding configuration for a project."""
        raise NotImplementedError("Branding not yet implemented")