"""
Video Service
Business logic for video upload and metadata extraction
"""

import uuid
from pathlib import Path
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.project import Project, ProjectStatus
from app.models.video import Video
from app.utils.ffmpeg import extract_metadata, generate_thumbnail, validate_video_format
from app.utils.file_utils import (
    get_video_dir,
    get_thumbnail_path,
    sanitize_filename,
    validate_video_extension,
    validate_file_size,
)


class VideoService:
    """Service layer for video operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def upload_video(
        self,
        project_id: str,
        filename: str,
        content: bytes,
    ) -> Video:
        """
        Save an uploaded video file, extract metadata, and generate a thumbnail.

        Args:
            project_id: The project UUID.
            filename: Original filename from the upload.
            content: Raw file bytes.

        Returns:
            The created Video model instance.

        Raises:
            ValueError: If file validation fails.
        """
        # Validate filename
        safe_name = sanitize_filename(filename)
        if not safe_name:
            raise ValueError("Invalid filename")

        # Validate extension
        if not validate_video_extension(safe_name):
            raise ValueError(
                f"Unsupported video format: {Path(safe_name).suffix}. "
                f"Allowed: {', '.join(settings.ALLOWED_VIDEO_FORMATS)}"
            )

        # Validate file size
        if not validate_file_size(len(content)):
            max_gb = settings.MAX_UPLOAD_SIZE / (1024**3)
            raise ValueError(f"File exceeds maximum upload size of {max_gb:.1f}GB")

        # Save file to disk
        video_dir = get_video_dir(project_id)
        file_path = video_dir / safe_name

        # Ensure unique filename to avoid collisions
        if file_path.exists():
            stem = file_path.stem
            suffix = file_path.suffix
            file_path = video_dir / f"{stem}_{uuid.uuid4().hex[:8]}{suffix}"

        file_path.write_bytes(content)

        # Extract video metadata using FFprobe
        try:
            metadata = extract_metadata(file_path)
        except Exception as e:
            # Clean up the saved file if metadata extraction fails
            file_path.unlink(missing_ok=True)
            raise ValueError(f"Failed to process video file: {e}")

        # Generate thumbnail
        thumbnail_path = get_thumbnail_path(project_id)
        try:
            generate_thumbnail(
                video_path=file_path,
                output_path=thumbnail_path,
                time_seconds=min(5.0, metadata.get("duration", 10) / 2),
                width=320,
            )
        except Exception:
            # Thumbnail generation failure is non-fatal
            thumbnail_path = None

        # Create video record
        video = Video(
            project_id=project_id,
            filename=safe_name,
            filepath=str(file_path),
            duration=metadata.get("duration"),
            width=metadata.get("width"),
            height=metadata.get("height"),
            fps=metadata.get("fps"),
            file_size=metadata.get("file_size"),
            codec=metadata.get("codec"),
            audio_codec=metadata.get("audio_codec"),
            audio_channels=metadata.get("audio_channels"),
            audio_sample_rate=metadata.get("audio_sample_rate"),
            thumbnail_path=str(thumbnail_path) if thumbnail_path else None,
        )

        self.db.add(video)

        # Update project status
        stmt = select(Project).where(Project.id == project_id)
        result = await self.db.execute(stmt)
        project = result.scalar_one_or_none()
        if project and project.status == ProjectStatus.DRAFT:
            project.status = ProjectStatus.VIDEO_IMPORTED

        await self.db.flush()
        await self.db.refresh(video)
        return video

    async def create_from_url(
        self,
        project_id: str,
        url: str,
        filename: Optional[str] = None,
    ) -> tuple[Video, str]:
        """
        Register a URL import in the database.
        The actual download is handled by a Celery task.

        Args:
            project_id: The project UUID.
            url: The source URL of the video.
            filename: Optional filename override.

        Returns:
            Tuple of (Video model, download task_id string).
        """
        safe_name = sanitize_filename(filename or url.split("/")[-1] or "downloaded_video")
        if not safe_name:
            safe_name = f"url_import_{uuid.uuid4().hex[:8]}.mp4"

        video = Video(
            project_id=project_id,
            filename=safe_name,
            filepath="",  # Will be updated after download
        )
        self.db.add(video)
        await self.db.flush()
        await self.db.refresh(video)

        # Return a placeholder task_id — actual download via Celery in Phase 1.1-1.3
        task_id = uuid.uuid4().hex
        return video, task_id

    async def get_video(self, project_id: str) -> Optional[Video]:
        """Get video for a project."""
        stmt = select(Video).where(Video.project_id == project_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_video(self, project_id: str) -> bool:
        """
        Delete a video record and its associated files.

        Returns True if a video was deleted, False if none existed.
        """
        video = await self.get_video(project_id)
        if not video:
            return False

        # Delete file from disk
        if video.filepath:
            Path(video.filepath).unlink(missing_ok=True)
        if video.thumbnail_path:
            Path(video.thumbnail_path).unlink(missing_ok=True)

        await self.db.delete(video)
        await self.db.flush()
        return True

    async def get_video_metadata(self, project_id: str) -> dict:
        """Get enriched video metadata including derived fields."""
        video = await self.get_video(project_id)
        if not video:
            return {}

        return {
            "id": str(video.id),
            "project_id": str(video.project_id),
            "filename": video.filename,
            "duration_seconds": video.duration,
            "duration_formatted": self._format_duration(video.duration),
            "resolution": f"{video.width}x{video.height}" if video.width and video.height else None,
            "width": video.width,
            "height": video.height,
            "fps": video.fps,
            "file_size_bytes": video.file_size,
            "file_size_formatted": self._format_size(video.file_size),
            "codec": video.codec,
            "audio_codec": video.audio_codec,
            "audio_channels": video.audio_channels,
            "audio_sample_rate": video.audio_sample_rate,
            "thumbnail_url": f"/api/v1/files/thumbnails/{project_id}.jpg" if video.thumbnail_path else None,
            "created_at": video.created_at.isoformat() if video.created_at else None,
        }

    def _format_duration(self, seconds: Optional[float]) -> Optional[str]:
        """Format duration in seconds to HH:MM:SS."""
        if seconds is None:
            return None
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"

    def _format_size(self, size_bytes: Optional[int]) -> Optional[str]:
        """Format file size in human-readable format."""
        if size_bytes is None:
            return None
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"