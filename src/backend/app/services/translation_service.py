"""
Translation Service
LLM-based translation with multiple engine adapters (Strategy pattern)
"""

from enum import Enum
from typing import Protocol, runtime_checkable

from sqlalchemy.ext.asyncio import AsyncSession


class TranslationEngine(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    GEMINI = "gemini"
    CLAUDE = "claude"


class TranslationStyle(str, Enum):
    NEUTRAL = "neutral"
    NATURAL = "natural"
    SHORT_VIDEO = "short_video"
    EDUCATIONAL = "educational"


@runtime_checkable
class TranslationAdapter(Protocol):
    """Interface for translation engine adapters."""

    async def translate_text(self, text: str, source_lang: str, target_lang: str, style: TranslationStyle) -> str:
        """Translate a single text segment."""
        ...


class OllamaAdapter:
    """Local LLM adapter using Ollama / Llama.cpp."""

    async def translate_text(self, text: str, source_lang: str, target_lang: str, style: TranslationStyle) -> str:
        raise NotImplementedError("Ollama adapter not yet implemented")


class OpenAIAdapter:
    """OpenAI API adapter."""

    async def translate_text(self, text: str, source_lang: str, target_lang: str, style: TranslationStyle) -> str:
        raise NotImplementedError("OpenAI adapter not yet implemented")


class GeminiAdapter:
    """Gemini API adapter."""

    async def translate_text(self, text: str, source_lang: str, target_lang: str, style: TranslationStyle) -> str:
        raise NotImplementedError("Gemini adapter not yet implemented")


class ClaudeAdapter:
    """Claude API adapter."""

    async def translate_text(self, text: str, source_lang: str, target_lang: str, style: TranslationStyle) -> str:
        raise NotImplementedError("Claude adapter not yet implemented")


# Registry of available adapters
_ADAPTERS: dict[TranslationEngine, TranslationAdapter] = {
    TranslationEngine.OLLAMA: OllamaAdapter(),
    TranslationEngine.OPENAI: OpenAIAdapter(),
    TranslationEngine.GEMINI: GeminiAdapter(),
    TranslationEngine.CLAUDE: ClaudeAdapter(),
}


def get_adapter(engine: TranslationEngine) -> TranslationAdapter:
    """Return the requested translation adapter."""
    try:
        return _ADAPTERS[engine]
    except KeyError:
        raise ValueError(f"Unsupported translation engine: {engine}")


class TranslationService:
    """Service layer for translation operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def translate(self, project_id: str, engine: TranslationEngine = TranslationEngine.OPENAI, style: TranslationStyle = TranslationStyle.NEUTRAL):
        """Translate transcript to target language."""
        raise NotImplementedError("Batch translation not yet implemented")

    async def translate_segment(self, text: str, source_lang: str = "auto", target_lang: str = "vi", engine: TranslationEngine = TranslationEngine.OPENAI, style: TranslationStyle = TranslationStyle.NEUTRAL) -> str:
        """Translate a single text segment using the selected engine."""
        adapter = get_adapter(engine)
        return await adapter.translate_text(text, source_lang, target_lang, style)