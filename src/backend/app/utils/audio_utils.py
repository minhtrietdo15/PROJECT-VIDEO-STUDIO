"""
Audio Utilities
Audio processing helpers
"""


def normalize_lufs(audio_path: str, target_lufs: float = -16.0) -> str:
    """Normalize audio loudness to target LUFS."""
    # Placeholder - will use ffmpeg-python or pydub
    raise NotImplementedError("Audio normalization not yet implemented")