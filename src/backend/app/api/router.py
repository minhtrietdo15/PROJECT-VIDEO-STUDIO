"""
API Router Aggregation
Mounts all v1 routers under /api/v1
"""

from fastapi import APIRouter

from app.api.v1 import (
    branding,
    chat,
    dubbing,
    files,
    projects,
    renders,
    subtitles,
    transcripts,
    translations,
    videos,
    voice_profiles,
    youtube,
)

api_router = APIRouter()

api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
api_router.include_router(transcripts.router, prefix="/transcripts", tags=["transcripts"])
api_router.include_router(translations.router, prefix="/translations", tags=["translations"])
api_router.include_router(dubbing.router, prefix="/dubbing", tags=["dubbing"])
api_router.include_router(subtitles.router, prefix="/subtitles", tags=["subtitles"])
api_router.include_router(branding.router, prefix="/branding", tags=["branding"])
api_router.include_router(renders.router, prefix="/renders", tags=["renders"])
api_router.include_router(voice_profiles.router, prefix="/voice-profiles", tags=["voice-profiles"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(youtube.router, prefix="/youtube", tags=["youtube"])
api_router.include_router(files.router, prefix="/files", tags=["files"])