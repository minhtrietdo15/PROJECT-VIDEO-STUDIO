"""
FFmpeg Utilities
Command builder and video/audio processing helpers
"""

import json
import subprocess
from pathlib import Path
from typing import Optional


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
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def extract_metadata(video_path: Path) -> dict:
    """
    Extract video metadata using FFprobe.

    Returns a dict with: duration, width, height, fps, codec, audio_codec,
    audio_sample_rate, audio_channels, file_size.
    """
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(video_path),
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)

    metadata = {
        "file_size": int(data.get("format", {}).get("size", 0)),
        "duration": float(data.get("format", {}).get("duration", 0)),
    }

    for stream in data.get("streams", []):
        codec_type = stream.get("codec_type")
        if codec_type == "video":
            metadata["width"] = stream.get("width", 0)
            metadata["height"] = stream.get("height", 0)
            # Calculate FPS from avg_frame_rate or r_frame_rate
            fps_str = stream.get("avg_frame_rate") or stream.get("r_frame_rate", "0/1")
            try:
                num, den = fps_str.split("/")
                metadata["fps"] = float(num) / float(den) if float(den) > 0 else 0.0
            except (ValueError, ZeroDivisionError):
                metadata["fps"] = 0.0
            metadata["codec"] = stream.get("codec_name", "")
        elif codec_type == "audio":
            metadata["audio_codec"] = stream.get("codec_name", "")
            metadata["audio_sample_rate"] = int(stream.get("sample_rate", 0))
            metadata["audio_channels"] = stream.get("channels", 0)

    return metadata


def generate_thumbnail(
    video_path: Path,
    output_path: Path,
    time_seconds: float = 5.0,
    width: Optional[int] = None,
) -> Path:
    """
    Generate a thumbnail from a video at the specified time.

    Args:
        video_path: Path to the input video.
        output_path: Path for the output thumbnail image.
        time_seconds: Time offset in seconds to capture the frame.
        width: Optional width to scale the thumbnail to.

    Returns:
        Path to the generated thumbnail.
    """
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(time_seconds),
        "-i", str(video_path),
        "-vframes", "1",
        "-q:v", "2",
    ]
    if width:
        cmd.extend(["-vf", f"scale={width}:-1"])
    cmd.append(str(output_path))

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def validate_video_format(filename: str, allowed_formats: list[str]) -> bool:
    """Check if the video file extension is in the allowed list."""
    ext = Path(filename).suffix.lower().lstrip(".")
    return ext in allowed_formats


def get_video_duration(video_path: Path) -> float:
    """Quickly get video duration in seconds using FFprobe."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return float(result.stdout.strip())