"""
Dubbing API Router
TTS voice dubbing endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.schemas.dubbing import DubbingResponse

router = APIRouter()


@router.get("/{project_id}", response_model=DubbingResponse)
async def get_dubbing(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DubbingResponse:
    """Get dubbing configuration for a project."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not yet implemented")