"""
YouTube API Router
YouTube publishing metadata endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.schemas.youtube import YouTubeMetadataResponse

router = APIRouter()


@router.get("/{project_id}", response_model=YouTubeMetadataResponse)
async def get_youtube_metadata(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> YouTubeMetadataResponse:
    """Get YouTube metadata for a project."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not yet implemented")


@router.put("/{project_id}", response_model=YouTubeMetadataResponse)
async def update_youtube_metadata(
    project_id: str,
    data: YouTubeMetadataResponse,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> YouTubeMetadataResponse:
    """Update YouTube metadata for a project."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not yet implemented")