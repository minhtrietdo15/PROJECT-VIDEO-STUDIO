"""
Video Render Service
FFmpeg-based video processing and assembly pipeline
"""

from enum import Enum
from pathlib import Path
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings


class VideoCodec(str, Enum):
    H264 = "h264"
    H265 = "h265"


class QualityPreset(str, Enum):
    FAST = "fast"
    BALANCED = "balanced"
    BEST = "best"


class RenderService:
    """Service layer for video rendering and processing."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def build_render_command(
        self,
        project_id: str,
        intro_path: Optional[Path] = None,
        main_video_path: Optional[Path] = None,
        outro_path: Optional[Path] = None,
        audio_path: Optional[Path] = None,
        subtitle_path: Optional[Path] = None,
        output_path: Optional[Path] = None,
        codec: VideoCodec = VideoCodec.H264,
        quality_preset: QualityPreset = QualityPreset.BALANCED,
        resolution_scale: Optional[str] = None,
    ) -> list[str]:
        """
        Build FFmpeg command for video assembly pipeline.

        Args:
            project_id: Project identifier
            intro_path: Optional intro video path
            main_video_path: Main video path
            outro_path: Optional outro video path
            audio_path: Optional voice-over audio path
            subtitle_path: Optional subtitle file path (SRT/ASS)
            output_path: Output file path
            codec: Video codec selection
            quality_preset: Encoding quality preset
            resolution_scale: Optional resolution scale (e.g., "1920:1080")

        Returns:
            FFmpeg command as list of strings
        """
        if not main_video_path or not output_path:
            raise ValueError("main_video_path and output_path are required")

        cmd = ["ffmpeg", "-y", "-i", str(main_video_path)]

        # Add audio if provided
        if audio_path and audio_path.exists():
            cmd.extend(["-i", str(audio_path)])

        # Build filter complex for assembly
        filters = []
        input_count = 1

        # Resolution scaling if specified
        if resolution_scale:
            filters.append(f"[{input_count}:v]scale={resolution_scale}[v{input_count}]")
            input_count += 1

        # Subtitle burning (hardcode)
        if subtitle_path and subtitle_path.exists():
            # Escape special characters for ASS format
            subtitle_escaped = str(subtitle_path).replace(":", "\\:")
            filters.append(f"[{input_count}:v]subtitles='{subtitle_escaped}'[v{input_count}]")
            input_count += 1

        if filters:
            cmd.extend(["-filter_complex", ";".join(filters)])

        # Codec settings
        codec_map = {
            VideoCodec.H264: ["-c:v", "libx264"],
            VideoCodec.H265: ["-c:v", "libx265"],
        }
        cmd.extend(codec_map.get(codec, codec_map[VideoCodec.H264]))

        # Quality preset mapping
        preset_map = {
            QualityPreset.FAST: "ultrafast",
            QualityPreset.BALANCED: "medium",
            QualityPreset.BEST: "slow",
        }
        cmd.extend(["-preset", preset_map.get(quality_preset, "medium")])

        # Audio codec
        cmd.extend(["-c:a", "aac", "-b:a", "192k"])

        # Output path
        cmd.append(str(output_path))

        return cmd

    async def normalize_audio(
        self,
        input_path: Path,
        output_path: Path,
        target_lufs: float = -16.0,
    ) -> list[str]:
        """
        Build FFmpeg command for volume normalization (EBU R128 / LUFS).

        Args:
            input_path: Input audio/video path
            output_path: Output path
            target_lufs: Target LUFS level (default -16.0 for speech)

        Returns:
            FFmpeg command as list of strings
        """
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_path),
            "-af",
            f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11",
            "-ar",
            "48000",
            str(output_path),
        ]
        return cmd

    async def apply_noise_reduction(
        self,
        input_path: Path,
        output_path: Path,
        strength: float = 0.5,
    ) -> list[str]:
        """
        Build FFmpeg command for noise reduction (afftdn filter).

        Args:
            input_path: Input audio path
            output_path: Output path
            strength: Noise reduction strength (0.0 to 1.0)

        Returns:
            FFmpeg command as list of strings
        """
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_path),
            "-af",
            f"afftdn=nf={strength}",
            str(output_path),
        ]
        return cmd

    async def crossfade_segments(
        self,
        segment_paths: list[Path],
        output_path: Path,
        crossfade_duration: float = 0.5,
    ) -> list[str]:
        """
        Build FFmpeg command to stitch segments with crossfade.

        Args:
            segment_paths: List of segment file paths
            output_path: Output path
            crossfade_duration: Crossfade duration in seconds

        Returns:
            FFmpeg command as list of strings
        """
        if not segment_paths:
            raise ValueError("At least one segment is required")

        if len(segment_paths) == 1:
            return ["cp", str(segment_paths[0]), str(output_path)]

        # Build complex filter for crossfade
        inputs = []
        for seg in segment_paths:
            inputs.extend(["-i", str(seg)])

        # Crossfade filter (pairwise)
        filters = []
        num_inputs = len(segment_paths)
        for i in range(num_inputs - 1):
            if i == 0:
                filters.append(
                    f"[{i}:a][{i+1}:a]acrossfade=d={crossfade_duration}c1=tri2[a{i}]"
                )
            else:
                filters.append(f"[a{i-1}][{i+1}:a]acrossfade=d={crossfade_duration}c1=tri2[a{i}]")

        filter_complex = ";".join(filters)
        last_stream = f"a{num_inputs-2}"

        cmd = [
            "ffmpeg",
            "-y",
            *inputs,
            "-filter_complex",
            filter_complex,
            "-map",
            f"[{last_stream}]",
            str(output_path),
        ]
        return cmd