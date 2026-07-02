import pytest
from src.backend.app.services.stt_service import STTService

def test_transcribe():
    stt_service = STTService()
    audio_path = "test_audio.wav"  # Replace with actual test audio file path
    result = stt_service.transcribe(audio_path)
    assert "transcription" in result