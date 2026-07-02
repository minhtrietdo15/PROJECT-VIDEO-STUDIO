"""
Renders API Router
Video rendering/export endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.schemas.render import RenderTaskResponse, RenderRequest

router = APIRouter()


@router.post("", response_model=RenderTaskResponse)
async def create_render_task(
    data: RenderRequest,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> RenderTaskResponse:
    """Start a video render task."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not yet implemented")


@router.get("/{task_id}", response_model=RenderTaskResponse)
async def get_render_task(
    task_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> RenderTaskResponse:
    """Get render task status."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not yet implemented")