"""
Translations API Router
Translation endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.schemas.translation import TranslationResponse

router = APIRouter()


@router.get("/{project_id}", response_model=TranslationResponse)
async def get_translation(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TranslationResponse:
    """Get translation for a project."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not yet implemented")