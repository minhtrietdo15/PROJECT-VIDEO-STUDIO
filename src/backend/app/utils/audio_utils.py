"""
Audio Utilities
Audio processing helpers
"""

import subprocess
from pathlib import Path


def normalize_lufs(audio_path: str, target_lufs: float = -16.0) -> str:
    """Normalize audio loudness to target LUFS."""
    # Placeholder - will use ffmpeg-python or pydub
    raise NotImplementedError("Audio normalization not yet implemented")


def extract_audio_for_stt(video_path: Path, output_path: Path, sample_rate: int = 16000) -> Path:
    """
    Extract a 16kHz mono WAV audio track from a video file for STT.

    Whisper expects 16kHz mono PCM audio. This helper uses FFmpeg to
    produce a consistent input format regardless of the source video.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        str(sample_rate),
        "-ac",
        "1",
        str(output_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path
