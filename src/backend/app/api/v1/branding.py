"""
Branding API Router
Branding configuration endpoints
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.models.branding import Branding
from app.schemas.branding import BrandingCreate, BrandingResponse, BrandingUpdate

router = APIRouter()


@router.get("/{project_id}", response_model=BrandingResponse)
async def get_branding(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BrandingResponse:
    """Get branding configuration for a project."""
    stmt = select(Branding).where(Branding.project_id == uuid.UUID(project_id))
    result = await db.execute(stmt)
    branding = result.scalar_one_or_none()
    if not branding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branding not found")
    return BrandingResponse.model_validate(branding)


@router.post("", response_model=BrandingResponse, status_code=status.HTTP_201_CREATED)
async def create_branding(
    data: BrandingCreate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BrandingResponse:
    """Create branding configuration for a project."""
    stmt = select(Branding).where(Branding.project_id == uuid.UUID(data.project_id))
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Branding already exists")

    branding = Branding(
        project_id=data.project_id,
        intro_enabled=data.intro_enabled,
        outro_enabled=data.outro_enabled,
        watermark_enabled=data.watermark_enabled,
        bg_music_enabled=data.bg_music_enabled,
        intro_config=data.intro_config or {},
        outro_config=data.outro_config or {},
        watermark_config=data.watermark_config or {},
        bg_music_config=data.bg_music_config or {},
        bg_music_volume=data.bg_music_volume,
    )
    db.add(branding)
    await db.flush()
    await db.refresh(branding)
    return BrandingResponse.model_validate(branding)


@router.put("/{project_id}", response_model=BrandingResponse)
async def update_branding(
    project_id: str,
    data: BrandingUpdate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BrandingResponse:
    """Update branding configuration for a project."""
    stmt = select(Branding).where(Branding.project_id == uuid.UUID(project_id))
    result = await db.execute(stmt)
    branding = result.scalar_one_or_none()
    if not branding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branding not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(branding, field, value)

    await db.flush()
    await db.refresh(branding)
    return BrandingResponse.model_validate(branding)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_branding(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete branding configuration for a project."""
    stmt = select(Branding).where(Branding.project_id == uuid.UUID(project_id))
    result = await db.execute(stmt)
    branding = result.scalar_one_or_none()
    if not branding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branding not found")
    await db.delete(branding)
    await db.flush()