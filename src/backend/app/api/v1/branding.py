"""
Branding API Router
Branding configuration endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.schemas.branding import BrandingResponse

router = APIRouter()


@router.get("/{project_id}", response_model=BrandingResponse)
async def get_branding(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BrandingResponse:
    """Get branding configuration for a project."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not yet implemented")