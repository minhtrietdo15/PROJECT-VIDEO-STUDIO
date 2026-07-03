"""
Unit tests for Translation Service (Strategy pattern adapters)
"""

import pytest

from app.services.translation_service import (
    TranslationEngine,
    TranslationStyle,
    TranslationService,
    get_adapter,
)


class DummyDB:
    pass


@pytest.fixture
def service():
    return TranslationService(db=DummyDB())


@pytest.mark.asyncio
async def test_translate_segment_raises_not_implemented(service):
    with pytest.raises(NotImplementedError):
        await service.translate_segment("hello", engine=TranslationEngine.OPENAI)


@pytest.mark.asyncio
async def test_translate_raises_not_implemented(service):
    with pytest.raises(NotImplementedError):
        await service.translate(project_id="proj-1")


@pytest.mark.asyncio
async def test_get_adapter_returns_adapter():
    adapter = get_adapter(TranslationEngine.OLLAMA)
    assert hasattr(adapter, "translate_text")


@pytest.mark.asyncio
async def test_get_adapter_invalid_engine():
    with pytest.raises(ValueError):
        get_adapter("invalid_engine")