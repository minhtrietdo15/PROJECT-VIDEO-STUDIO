"""
Video Service
Business logic for video upload and metadata extraction
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.video import Video


class VideoService:
    """Service layer for video operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_video(self, project_id: str, filename: str, filepath: str) -> Video:
        """Create a video record."""
        video = Video(
            project_id=project_id,
            filename=filename,
            filepath=filepath,
        )
        self.db.add(video)
        await self.db.flush()
        await self.db.refresh(video)
        return video

    async def get_video(self, project_id: str) -> Video | None:
        """Get video for a project."""
        from sqlalchemy import select
        stmt = select(Video).where(Video.project_id == project_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()