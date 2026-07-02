"""
Subtitles API Router
Subtitle generation and management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.schemas.subtitle import SubtitleResponse

router = APIRouter()


@router.get("/{project_id}", response_model=SubtitleResponse)
async def get_subtitle(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SubtitleResponse:
    """Get subtitle for a project."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not yet implemented")