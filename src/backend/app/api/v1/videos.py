"""
Videos API Router
Video upload, metadata, and management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.schemas.video import VideoResponse

router = APIRouter()


@router.get("/{project_id}", response_model=VideoResponse)
async def get_video(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VideoResponse:
    """Get video metadata for a project."""
    # Placeholder - will be implemented with proper model queries
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not yet implemented")