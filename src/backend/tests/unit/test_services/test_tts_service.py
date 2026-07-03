"""
Unit tests for TTS Service (Strategy pattern adapters)
"""

import pytest

from app.services.tts_service import (
    TTSEngine,
    TTSService,
    get_tts_adapter,
)


class DummyDB:
    pass


@pytest.fixture
def service():
    return TTSService(db=DummyDB())


@pytest.mark.asyncio
async def test_generate_audio_segment_raises_not_implemented(service):
    with pytest.raises(NotImplementedError):
        await service.generate_audio_segment("hello", voice_id="v1", engine=TTSEngine.COQUI)


@pytest.mark.asyncio
async def test_get_tts_adapter_returns_adapter():
    adapter = get_tts_adapter(TTSEngine.EDGE_TTS)
    assert hasattr(adapter, "generate_audio")


@pytest.mark.asyncio
async def test_get_tts_adapter_invalid_engine():
    with pytest.raises(ValueError):
        get_tts_adapter("invalid_engine")