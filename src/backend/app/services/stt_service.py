"""
Whisper Integration Service
Supports all model sizes, GPU/CPU fallback, and language auto-detection.
"""

import logging
import subprocess
from pathlib import Path
from typing import Optional

import whisper
import torch
from app.core.config import settings

logger = logging.getLogger(__name__)

# ── Valid model sizes ────────────────────────────────────────────────
VALID_MODEL_SIZES = {"tiny", "base", "small", "medium", "large"}

# ── Known languages whisper supports (ISO 639-1 subset) ──────────────
SUPPORTED_LANGUAGES = {
    "en", "vi", "zh", "ja", "ko", "th", "id", "ms", "tl",
    "fr", "es", "pt", "de", "it", "nl", "ru", "ar", "tr",
    "hi", "bn", "ur", "fa",
}


def _detect_gpu() -> bool:
    """Return True if CUDA is available and GPU is enabled in config."""
    if not settings.GPU_ENABLED:
        return False
    return torch.cuda.is_available()


def _get_device() -> str:
    """Return 'cuda' or 'cpu' based on availability and config."""
    return "cuda" if _detect_gpu() else "cpu"


def _get_whisper_model_size(model_size: str) -> str:
    """Validate and return the model size, falling back to config default."""
    size = model_size.strip().lower()
    if size not in VALID_MODEL_SIZES:
        logger.warning(
            "Invalid model size '%s', falling back to '%s'",
            size,
            settings.WHISPER_MODEL,
        )
        size = settings.WHISPER_MODEL
    return size


def _extract_audio(
    video_path: Path,
    output_path: Path,
) -> None:
    """Extract 16 kHz mono WAV audio from video using FFmpeg."""
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        str(output_path),
    ]
    logger.info("Extracting audio: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Audio extraction failed (rc={result.returncode}): {result.stderr}"
        )


def _merge_short_segments(
    segments: list[dict],
    min_duration: float = 1.0,
    max_duration: float = 10.0,
) -> list[dict]:
    """Merge consecutive segments shorter than min_duration and split
    segments that exceed max_duration.

    Each segment dict is expected to have at least:
        start, end, text
    """
    if not segments:
        return []

    merged: list[dict] = []
    buffer: list[dict] = []

    for seg in segments:
        buffer.append(seg)
        buf_dur = buffer[-1]["end"] - buffer[0]["start"]
        if buf_dur >= max_duration:
            merged.append(_merge_buffer(buffer))
            buffer = []

    if buffer:
        merged.append(_merge_buffer(buffer))

    # Now split any extra-long merged segments at natural boundaries
    final: list[dict] = []
    for seg in merged:
        dur = seg["end"] - seg["start"]
        if dur <= max_duration:
            final.append(seg)
        else:
            final.extend(_split_segment(seg, max_duration))

    return final


def _merge_buffer(buffer: list[dict]) -> dict:
    """Merge a list of segment dicts into one."""
    return {
        "start": buffer[0]["start"],
        "end": buffer[-1]["end"],
        "text": " ".join(s["text"].strip() for s in buffer).strip(),
    }


def _split_segment(seg: dict, max_dur: float) -> list[dict]:
    """Split a single segment into multiple chunks at natural splits."""
    text = seg.get("text", "")
    words = text.split()
    if not words:
        return [seg]

    dur = seg["end"] - seg["start"]
    n_chunks = max(1, int(dur / max_dur))
    chunk_size = len(words) // n_chunks
    chunk_dur = dur / n_chunks

    result: list[dict] = []
    for i in range(n_chunks):
        start = i * chunk_size
        end = start + chunk_size if i < n_chunks - 1 else len(words)
        chunk_text = " ".join(words[start:end])
        result.append({
            "start": seg["start"] + i * chunk_dur,
            "end": seg["start"] + (i + 1) * chunk_dur,
            "text": chunk_text,
        })
    return result


class STTService:
    """Whisper-based speech-to-text service with GPU/CPU fallback."""

    def __init__(self, db_session=None):
        self._model: Optional[whisper.Whisper] = None
        self._model_size: str = ""
        self._device: str = _get_device()
        self._db = db_session

    # ── Public API ──────────────────────────────────────────────────

    async def transcribe(
        self,
        project_id: str,
        model_size: str = "medium",
        language: Optional[str] = None,
        word_timestamps: bool = True,
    ) -> dict:
        """Run Whisper transcription for a project.

        Args:
            project_id: UUID of the project to transcribe.
            model_size: One of tiny / base / small / medium / large.
            language: ISO 639-1 code or None for auto-detection.
            word_timestamps: Whether to include word-level timestamps.

        Returns:
            Dict with keys: project_id, status, segment_count, language,
            model_used, segments, raw_text, duration_seconds.
        """
        logger.info(
            "Transcribing project %s | model=%s lang=%s device=%s",
            project_id,
            model_size,
            language or "auto",
            self._device,
        )

        if language and language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language code: {language}")

        resolved_size = _get_whisper_model_size(model_size)
        self._load_model(resolved_size)

        options = {
            "word_timestamps": word_timestamps,
        }
        if language:
            options["language"] = language

        video_path = self._resolve_video_path(project_id)

        audio_path = video_path.with_suffix(".wav")
        if not audio_path.exists():
            _extract_audio(video_path, audio_path)

        result = self._model.transcribe(
            str(audio_path),
            **options,
        )

        detected_language: str = result.get("language", language or "unknown")
        raw_text: str = result.get("text", "").strip()

        raw_segments: list[dict] = result.get("segments", [])
        normalised_segments = self._normalise_segments(
            raw_segments,
            word_timestamps,
        )
        processed_segments = _merge_short_segments(normalised_segments)

        duration = 0.0
        if processed_segments:
            duration = processed_segments[-1]["end"]

        result_payload = {
            "project_id": str(project_id),
            "status": "completed",
            "segment_count": len(processed_segments),
            "language": detected_language,
            "model_used": resolved_size,
            "segments": processed_segments,
            "raw_text": raw_text,
            "duration_seconds": duration,
        }

        logger.info(
            "Transcription complete for %s: %d segments, lang=%s",
            project_id,
            len(processed_segments),
            detected_language,
        )

        return result_payload

    # ── Internal helpers ────────────────────────────────────────────

    def _load_model(self, model_size: str) -> None:
        """Load or reload the Whisper model if the size differs."""
        if self._model is not None and self._model_size == model_size:
            return

        logger.info("Loading Whisper model '%s' on %s …", model_size, self._device)
        model_dir = settings.WHISPER_MODEL_DIR
        download_root = str(model_dir) if model_dir else None

        self._model = whisper.load_model(
            model_size,
            device=self._device,
            download_root=download_root,
        )
        self._model_size = model_size
        logger.info("Whisper model '%s' loaded successfully", model_size)

    def _normalise_segments(
        self,
        segments: list[dict],
        word_timestamps: bool,
    ) -> list[dict]:
        """Convert raw whisper segments into the canonical format."""
        result: list[dict] = []
        for seg in segments:
            entry = {
                "start": round(seg.get("start", 0.0), 3),
                "end": round(seg.get("end", 0.0), 3),
                "text": seg.get("text", "").strip(),
            }
            if word_timestamps and seg.get("words"):
                entry["words"] = [
                    {
                        "word": w.get("word", ""),
                        "start": round(w.get("start", 0.0), 3),
                        "end": round(w.get("end", 0.0), 3),
                        "probability": round(w.get("probability", 1.0), 4),
                    }
                    for w in seg["words"]
                ]
            result.append(entry)
        return result

    def _resolve_video_path(self, project_id: str) -> Path:
        """Resolve the project video file path from the data directory."""
        video_dir = settings.UPLOAD_DIR / str(project_id) / "video"
        for ext in settings.ALLOWED_VIDEO_FORMATS:
            candidate = video_dir / f"original.{ext}"
            if candidate.exists():
                return candidate
        raise FileNotFoundError(
            f"No video found for project {project_id} in {video_dir}"
        )
