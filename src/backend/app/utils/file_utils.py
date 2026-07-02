"""
File Utilities
Path management, format validation, and file I/O helpers
"""

import os
import shutil
from pathlib import Path
from typing import Optional

from app.core.config import settings


def get_project_dir(project_id: str) -> Path:
    """Get the project data directory, creating it if needed."""
    project_dir = settings.UPLOAD_DIR / project_id
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir


def get_video_dir(project_id: str) -> Path:
    """Get the video directory for a project."""
    video_dir = get_project_dir(project_id) / "video"
    video_dir.mkdir(parents=True, exist_ok=True)
    return video_dir


def get_audio_dir(project_id: str) -> Path:
    """Get the audio directory for a project."""
    audio_dir = get_project_dir(project_id) / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    return audio_dir


def get_output_dir(project_id: str) -> Path:
    """Get the output directory for a project."""
    output_dir = get_project_dir(project_id) / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_subtitle_dir(project_id: str) -> Path:
    """Get the subtitle directory for a project."""
    subtitle_dir = get_project_dir(project_id) / "subtitles"
    subtitle_dir.mkdir(parents=True, exist_ok=True)
    return subtitle_dir


def get_branding_dir(project_id: str) -> Path:
    """Get the branding directory for a project."""
    branding_dir = get_project_dir(project_id) / "branding"
    branding_dir.mkdir(parents=True, exist_ok=True)
    return branding_dir


def get_thumbnail_path(project_id: str) -> Path:
    """Get the thumbnail path for a project."""
    return get_video_dir(project_id) / "thumbnail.jpg"


def get_video_path(project_id: str, filename: str) -> Path:
    """Get the full path for a stored video file."""
    return get_video_dir(project_id) / filename


def validate_file_size(file_size: int, max_size: Optional[int] = None) -> bool:
    """Check if file size is within allowed limits."""
    if max_size is None:
        max_size = settings.MAX_UPLOAD_SIZE
    return 0 < file_size <= max_size


def validate_video_extension(filename: str) -> bool:
    """Check if the video extension is in the allowed list."""
    ext = Path(filename).suffix.lower().lstrip(".")
    return ext in settings.ALLOWED_VIDEO_FORMATS


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename to prevent directory traversal and special chars."""
    # Remove directory components
    name = Path(filename).name
    # Replace potentially problematic characters
    sanitized = "".join(c for c in name if c.isalnum() or c in "._- ")
    return sanitized if sanitized else "untitled"


def ensure_dir(path: Path) -> Path:
    """Ensure a directory exists, creating it if necessary."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def cleanup_project(project_id: str) -> None:
    """Remove all files associated with a project."""
    project_dir = settings.UPLOAD_DIR / project_id
    if project_dir.exists():
        shutil.rmtree(project_dir)


def get_disk_usage(path: Optional[Path] = None) -> dict:
    """Get disk usage statistics for the data directory."""
    target = path or settings.DATA_ROOT
    if not target.exists():
        return {"total": 0, "used": 0, "free": 0}

    stat = os.statvfs(str(target))
    total = stat.f_frsize * stat.f_blocks
    free = stat.f_frsize * stat.f_bfree
    used = total - free

    return {
        "total": total,
        "used": used,
        "free": free,
    }