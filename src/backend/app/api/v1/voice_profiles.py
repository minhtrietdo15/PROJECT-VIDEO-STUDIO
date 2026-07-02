"""
Voice Profiles API Router
TTS voice profile management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.schemas.voice import VoiceProfileCreate, VoiceProfileResponse, VoiceProfileUpdate

router = APIRouter()


@router.post("", response_model=VoiceProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_voice_profile(
    data: VoiceProfileCreate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VoiceProfileResponse:
    """Create a new voice profile."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not yet implemented")


@router.get("", response_model=list[VoiceProfileResponse])
async def list_voice_profiles(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[VoiceProfileResponse]:
    """List all voice profiles for the current user."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not yet implemented")


@router.patch("/{profile_id}", response_model=VoiceProfileResponse)
async def update_voice_profile(
    profile_id: str,
    data: VoiceProfileUpdate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> VoiceProfileResponse:
    """Update a voice profile."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not yet implemented")


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_voice_profile(
    profile_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a voice profile."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not yet implemented")