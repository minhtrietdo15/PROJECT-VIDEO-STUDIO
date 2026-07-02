"""
File Service
File I/O management stub
"""

import os
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession


class FileService:
    """Service layer for file operations."""

    def __init__(self, db: AsyncSession, data_root: Path):
        self.db = db
        self.data_root = data_root

    async def save_upload(self, project_id: str, filename: str, content: bytes) -> Path:
        """Save an uploaded file."""
        raise NotImplementedError("File upload not yet implemented")

    async def get_file_path(self, project_id: str, file_type: str) -> Path:
        """Get the path for a project file."""
        raise NotImplementedError("File path resolution not yet implemented")