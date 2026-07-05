"""
Subtitle Service.
Handles subtitle generation and styling using pysubs2.
"""

from typing import Any
from app.models.subtitle import Subtitle


class SubtitleService:
    """Service for generating and managing subtitles."""

    def generate_subtitle_file(
        self,
        segments: list[dict[str, Any]],
        format: str = "srt",
        style_config: dict[str, Any] | None = None,
    ) -> str:
        """
        Generate subtitle file content from segments.

        Args:
            segments: List of segment dicts with start, end, text
            format: Output format (srt, ass, vtt)
            style_config: Optional styling configuration

        Returns:
            Formatted subtitle string
        """
        # Basic implementation without pysubs2 dependency
        # Can be enhanced with pysubs2 for ASS styling
        if format == "srt":
            return self._generate_srt(segments)
        elif format == "vtt":
            return self._generate_vtt(segments)
        elif format == "ass":
            return self._generate_ass(segments, style_config)
        else:
            return self._generate_srt(segments)

    def _generate_srt(self, segments: list[dict[str, Any]]) -> str:
        """Generate SRT format subtitles."""
        lines = []
        for index, seg in enumerate(segments, 1):
            start_time = self._format_time_srt(seg["start"])
            end_time = self._format_time_srt(seg["end"])
            lines.append(f"{index}")
            lines.append(f"{start_time} --> {end_time}")
            lines.append(seg["text"])
            lines.append("")
        return "\n".join(lines)

    def _generate_vtt(self, segments: list[dict[str, Any]]) -> str:
        """Generate WebVTT format subtitles."""
        lines = ["WEBVTT", ""]
        for seg in segments:
            start_time = self._format_time_vtt(seg["start"])
            end_time = self._format_time_vtt(seg["end"])
            lines.append(f"{start_time} --> {end_time}")
            lines.append(seg["text"])
            lines.append("")
        return "\n".join(lines)

    def _generate_ass(
        self,
        segments: list[dict[str, Any]],
        style_config: dict[str, Any] | None = None,
    ) -> str:
        """Generate ASS format subtitles with styling."""
        # Default style
        default_style = {
            "fontFamily": "Arial",
            "fontSize": 24,
            "color": "#FFFFFF",
            "backgroundColor": "#000000",
            "borderColor": "#000000",
            "borderWidth": 2,
            "shadow": True,
            "position": "bottom",
            "animation": "none",
        }
        if style_config:
            default_style.update(style_config)

        header = f"""[Script Info]
Title: Subtitle
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, AlphaLevel, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{default_style['fontFamily']},{default_style['fontSize']},&H{default_style['color'][1:]},&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,{default_style['borderWidth']},{1 if default_style['shadow'] else 0},2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        lines = [header]
        for seg in segments:
            start_time = self._format_time_ass(seg["start"])
            end_time = self._format_time_ass(seg["end"])
            lines.append(f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{seg['text'].replace(chr(10), '\\N')}")

        return "\n".join(lines)

    def _format_time_srt(self, seconds: float) -> str:
        """Format time for SRT (HH:MM:SS.cc)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        hundredths = int((seconds % 1) * 100)
        return f"{hours}:{minutes:02d}:{secs:02d}.{hundredths:02d}"

    def _format_time_vtt(self, seconds: float) -> str:
        """Format time for VTT (HH:MM:SS.ccc)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}:{minutes:02d}:{secs:06.3f}"

    def _format_time_ass(self, seconds: float) -> str:
        """Format time for ASS (H:MM:SS.cc)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        hundredths = int((seconds % 1) * 100)
        return f"{hours}:{minutes:02d}:{secs:02d}.{hundredths:02d}"