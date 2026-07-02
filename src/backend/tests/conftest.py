"""
Pytest Configuration and Fixtures
Shared test fixtures and configuration
"""

import pytest

from app.core.config import settings


@pytest.fixture
def test_settings():
    """Override settings for testing."""
    settings.DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    settings.DEBUG = True
    return settings