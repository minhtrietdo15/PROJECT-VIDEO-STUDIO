"""
Pytest Configuration and Fixtures
Shared test fixtures and configuration
"""

import os

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.api.dependencies import get_current_user, get_db
from app.core.config import settings
from app.main import app
from app.models.base import Base


@pytest.fixture(scope="session", autouse=True)
def test_settings():
    """Override settings for testing before app imports."""
    settings.DATABASE_URL = os.environ.get(
        "TEST_DATABASE_URL",
        "postgresql+asyncpg://videostudio:videostudio@localhost:5432/videostudio",
    )
    settings.DEBUG = True
    return settings


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        future=True,
        poolclass=NullPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db(engine):
    # Create a fresh session for each test case
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def client(engine):
    # Create a fresh session maker for the override
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with async_session_maker() as session:
            yield session
            await session.commit()

    async def override_get_current_user():
        return "test-user-id"

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            yield ac
    app.dependency_overrides.clear()
