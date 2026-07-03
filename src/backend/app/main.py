"""
FastAPI Application Entry Point
Video Localization AI Studio
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.events import lifespan_events
from app.core.logging import setup_logging
from app.core.middleware import RequestLoggingMiddleware
from app.models import base  # noqa: F401
from app.models import branding, chat, dubbing, project, render_task, subtitle, transcript, translation, video, voice_profile, youtube_metadata  # noqa: F401,E501


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown events."""
    setup_logging()
    await lifespan_events.startup(app)
    yield
    await lifespan_events.shutdown(app)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# ─── Middleware ───────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

# ─── Routers ─────────────────────────────────────────────────
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root health check."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
    }