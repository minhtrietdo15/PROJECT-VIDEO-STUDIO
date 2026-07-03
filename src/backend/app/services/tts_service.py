"""
Text-to-Speech Service
TTS engine integration with Strategy pattern
"""

from enum import Enum
from typing import Protocol, runtime_checkable

from sqlalchemy.ext.asyncio import AsyncSession


class TTSEngine(str, Enum):
    COQUI = "coqui"
    PIPER = "piper"
    EDGE_TTS = "edge_tts"


@runtime_checkable
class TTSAdapter(Protocol):
    """Interface for TTS engine adapters."""

    async def generate_audio(self, text: str, voice_id: str, speed: float = 1.0, pitch: float = 1.0) -> str:
        """Generate audio from text and return path to output file."""
        ...


class CoquiTTSAdapter:
    """Coqui TTS adapter (local, supports Vietnamese models)."""

    async def generate_audio(self, text: str, voice_id: str, speed: float = 1.0, pitch: float = 1.0) -> str:
        raise NotImplementedError("Coqui TTS adapter not yet implemented")


class PiperTTSAdapter:
    """Piper TTS adapter (lightweight local)."""

    async def generate_audio(self, text: str, voice_id: str, speed: float = 1.0, pitch: float = 1.0) -> str:
        raise NotImplementedError("Piper TTS adapter not yet implemented")


class EdgeTTSAdapter:
    """Edge-TTS adapter (free online service)."""

    async def generate_audio(self, text: str, voice_id: str, speed: float = 1.0, pitch: float = 1.0) -> str:
        raise NotImplementedError("Edge-TTS adapter not yet implemented")


# Registry of available adapters
_TTS_ADAPTERS: dict[TTSEngine, TTSAdapter] = {
    TTSEngine.COQUI: CoquiTTSAdapter(),
    TTSEngine.PIPER: PiperTTSAdapter(),
    TTSEngine.EDGE_TTS: EdgeTTSAdapter(),
}


def get_tts_adapter(engine: TTSEngine) -> TTSAdapter:
    """Return the requested TTS adapter."""
    try:
        return _TTS_ADAPTERS[engine]
    except KeyError:
        raise ValueError(f"Unsupported TTS engine: {engine}")


class TTSService:
    """Service layer for text-to-speech operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_audio_segment(self, text: str, voice_id: str, engine: TTSEngine = TTSEngine.EDGE_TTS, speed: float = 1.0, pitch: float = 1.0) -> str:
        """Generate audio for a single text segment."""
        adapter = get_tts_adapter(engine)
        return await adapter.generate_audio(text, voice_id, speed, pitch)