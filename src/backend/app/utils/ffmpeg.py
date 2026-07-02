"""
FFmpeg Utilities
Command builder and video/audio processing helpers
"""

from pathlib import Path


def build_ffmpeg_command(inputs: list[dict], filters: str, output: str, **kwargs) -> list[str]:
    """Build an FFmpeg command from inputs, filters, and output settings."""
    cmd = ["ffmpeg", "-y"]

    for inp in inputs:
        if "file" in inp:
            cmd.extend(["-i", str(inp["file"])])

    if filters:
        cmd.extend(["-filter_complex", filters])

    for key, value in kwargs.items():
        cmd.extend([f"-{key}", str(value)])

    cmd.append(output)
    return cmd


def extract_audio(video_path: Path, output_path: Path, sample_rate: int = 16000) -> Path:
    """Extract audio from video file."""
    cmd = build_ffmpeg_command(
        [{"file": str(video_path)}],
        filters="",
        output=str(output_path),
        v="0",
        acodec="pcm_s16le",
        ar=sample_rate,
        ac="1",
    )
    return output_path