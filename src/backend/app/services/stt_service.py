"""
Speech-to-Text Service
Whisper integration with model size selection, GPU/CPU fallback, and
segment post-processing.
"""

import logging
import uuid
from pathlib import Path
from typing import Optional

import torch
import whisper
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import (
    EngineUnavailableException,
    NotFoundException,
    ProjectNotFoundException,
    VideoNotFoundException,
)
from app.models.project import Project, ProjectStatus
from app.models.transcript import Transcript, TranscriptStatus
from app.models.video import Video
from app.utils.audio_utils import extract_audio_for_stt
from app.utils.file_utils import get_audio_dir

logger = logging.getLogger(__name__)

# Valid Whisper model sizes ordered from smallest to largest.
WHISPER_MODEL_SIZES = ("tiny", "base", "small", "medium", "large")

# Target segment length for post-processing (seconds).
MIN_SEGMENT_SECONDS = 1.0
MAX_SEGMENT_SECONDS = 10.0


class STTService:
    """Service layer for speech-to-text operations using OpenAI Whisper."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def transcribe(
        self,
        project_id: str,
        model_size: str = "medium",
        language: Optional[str] = None,
        word_timestamps: bool = True,
    ) -> Transcript:
        """
        Transcribe the video audio for a project.

        Args:
            project_id: UUID of the project to transcribe.
            model_size: Whisper model size (tiny, base, small, medium, large).
            language: Optional ISO 639-1 language code. If None, Whisper
                auto-detects the language.
            word_timestamps: Whether to include word-level timestamps.

        Returns:
            The created/updated Transcript model instance.

        Raises:
            ProjectNotFoundException: If the project does not exist.
            VideoNotFoundException: If the project has no video file.
            EngineUnavailableException: If Whisper cannot be loaded.
        """
        project = await self._get_project(project_id)
        if not project:
            raise ProjectNotFoundException(project_id)

        video = await self._get_video(project_id)
        if not video or not video.filepath:
            raise VideoNotFoundException(project_id)

        video_path = Path(video.filepath)
        if not video_path.exists():
            raise VideoNotFoundException(project_id)

        # Create or reset transcript record
        transcript = await self._get_or_create_transcript(project_id)
        transcript.status = TranscriptStatus.PROCESSING
        transcript.error_message = None
        transcript.model_used = model_size
        project.status = ProjectStatus.TRANSCRIBING
        await self.db.flush()

        try:
            audio_path = await self._prepare_audio(project_id, video_path)
            result = await self._run_whisper(
                audio_path=audio_path,
                model_size=model_size,
                language=language,
                word_timestamps=word_timestamps,
            )

            detected_language = result.get("language") or language
            segments = self._normalize_segments(result.get("segments", []))
            segments = self._post_process_segments(segments)

            transcript.status = TranscriptStatus.COMPLETED
            transcript.language = detected_language
            transcript.segments = segments
            transcript.raw_text = result.get("text", "").strip()
            transcript.duration_seconds = video.duration
            project.status = ProjectStatus.TRANSCRIPT_READY

            await self.db.flush()
            await self.db.refresh(transcript)
            return transcript
        except Exception as exc:
            logger.exception("STT failed for project %s", project_id)
            transcript.status = TranscriptStatus.FAILED
            transcript.error_message = str(exc)
            project.status = ProjectStatus.FAILED
            await self.db.flush()
            raise EngineUnavailableException("whisper") from exc

    async def _get_project(self, project_id: str) -> Optional[Project]:
        """Fetch a project by ID."""
        stmt = select(Project).where(Project.id == uuid.UUID(project_id))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_video(self, project_id: str) -> Optional[Video]:
        """Fetch the video record for a project."""
        stmt = select(Video).where(Video.project_id == uuid.UUID(project_id))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_or_create_transcript(self, project_id: str) -> Transcript:
        """Get existing transcript or create a new one."""
        stmt = select(Transcript).where(Transcript.project_id == uuid.UUID(project_id))
        result = await self.db.execute(stmt)
        transcript = result.scalar_one_or_none()
        if transcript:
            return transcript

        new_transcript = Transcript(
            project_id=uuid.UUID(project_id),
            status=TranscriptStatus.PENDING,
        )
        self.db.add(new_transcript)
        await self.db.flush()
        return new_transcript

    async def _prepare_audio(self, project_id: str, video_path: Path) -> Path:
        """Extract 16kHz mono WAV audio suitable for Whisper."""
        audio_dir = get_audio_dir(project_id)
        audio_path = audio_dir / "stt_input.wav"
        extract_audio_for_stt(video_path, audio_path)
        return audio_path

    async def _run_whisper(
        self,
        audio_path: Path,
        model_size: str,
        language: Optional[str],
        word_timestamps: bool,
    ) -> dict:
        """
        Load Whisper model and run transcription.

        Falls back to CPU if CUDA is unavailable or GPU loading fails.
        Falls back to a smaller model size if the requested model cannot be
        loaded due to memory constraints.
        """
        model_size = self._validate_model_size(model_size)
        device = self._select_device()

        # Try requested model size, then progressively smaller sizes on failure.
        sizes_to_try = self._model_size_fallback_chain(model_size)
        last_error: Optional[Exception] = None

        for size in sizes_to_try:
            try:
                logger.info("Loading Whisper model '%s' on %s", size, device)
                model = whisper.load_model(size, device=device)
                logger.info("Transcribing audio: %s", audio_path)
                result = model.transcribe(
                    str(audio_path),
                    language=language,
                    word_timestamps=word_timestamps,
                    verbose=False,
                )
                return result
            except (RuntimeError, torch.cuda.OutOfMemoryError) as exc:
                last_error = exc
                logger.warning(
                    "Whisper model '%s' failed on %s: %s. Trying fallback.",
                    size,
                    device,
                    exc,
                )
                # If GPU OOM, switch to CPU for subsequent attempts.
                if device != "cpu" and "out of memory" in str(exc).lower():
                    device = "cpu"
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                logger.warning("Whisper model '%s' failed: %s", size, exc)

        raise EngineUnavailableException("whisper") from last_error

    def _validate_model_size(self, model_size: str) -> str:
        """Normalize and validate the requested model size."""
        size = model_size.lower().strip()
        if size not in WHISPER_MODEL_SIZES:
            logger.warning("Invalid model size '%s', defaulting to '%s'", model_size, settings.WHISPER_MODEL)
            return settings.WHISPER_MODEL
        return size

    def _model_size_fallback_chain(self, model_size: str) -> tuple[str, ...]:
        """Return a tuple of model sizes to try, starting from requested."""
        index = WHISPER_MODEL_SIZES.index(model_size)
        return WHISPER_MODEL_SIZES[index:]

    def _select_device(self) -> str:
        """Select CUDA if enabled and available, otherwise CPU."""
        if settings.GPU_ENABLED and torch.cuda.is_available():
            return "cuda"
        return "cpu"

    def _normalize_segments(self, raw_segments: list[dict]) -> list[dict]:
        """
        Convert Whisper segments into a normalized JSON format.

        Each segment contains: id, start, end, text, words (optional).
        Times are stored in milliseconds.
        """
        normalized: list[dict] = []
        for index, segment in enumerate(raw_segments):
            words = segment.get("words") or []
            normalized_words = [
                {
                    "word": str(word.get("word", "")).strip(),
                    "start_ms": int(float(word.get("start", 0)) * 1000),
                    "end_ms": int(float(word.get("end", 0)) * 1000),
                    "confidence": word.get("probability"),
                }
                for word in words
                if word.get("word")
            ]

            normalized.append(
                {
                    "segment_index": index,
                    "start_ms": int(float(segment.get("start", 0)) * 1000),
                    "end_ms": int(float(segment.get("end", 0)) * 1000),
                    "text": str(segment.get("text", "")).strip(),
                    "words": normalized_words,
                }
            )
        return normalized

    def _post_process_segments(self, segments: list[dict]) -> list[dict]:
        """
        Merge short segments and split overly long segments.

        Target segment length is between MIN_SEGMENT_SECONDS and
        MAX_SEGMENT_SECONDS.
        """
        if not segments:
            return []

        # Merge segments shorter than MIN_SEGMENT_SECONDS with the next one.
        merged: list[dict] = []
        buffer: Optional[dict] = None
        for segment in segments:
            duration_ms = segment["end_ms"] - segment["start_ms"]
            if buffer is None:
                buffer = segment
                continue

            buffer_duration = buffer["end_ms"] - buffer["start_ms"]
            if buffer_duration < MIN_SEGMENT_SECONDS * 1000:
                buffer = self._merge_two_segments(buffer, segment)
            else:
                merged.append(buffer)
                buffer = segment

        if buffer is not None:
            merged.append(buffer)

        # Split segments longer than MAX_SEGMENT_SECONDS.
        final_segments: list[dict] = []
        for segment in merged:
            duration_ms = segment["end_ms"] - segment["start_ms"]
            if duration_ms > MAX_SEGMENT_SECONDS * 1000:
                final_segments.extend(self._split_segment(segment))
            else:
                final_segments.append(segment)

        # Re-index after merging/splitting.
        for index, segment in enumerate(final_segments):
            segment["segment_index"] = index

        return final_segments

    def _merge_two_segments(self, first: dict, second: dict) -> dict:
        """Merge two adjacent segments into one."""
        words = (first.get("words") or []) + (second.get("words") or [])
        return {
            "segment_index": first["segment_index"],
            "start_ms": first["start_ms"],
            "end_ms": second["end_ms"],
            "text": f"{first['text']} {second['text']}".strip(),
            "words": words,
        }

    def _split_segment(self, segment: dict) -> list[dict]:
        """Split a long segment into chunks of roughly equal duration."""
        duration_ms = segment["end_ms"] - segment["start_ms"]
        num_parts = max(2, int(duration_ms / (MAX_SEGMENT_SECONDS * 1000)) + 1)
        chunk_duration = duration_ms // num_parts

        words = segment.get("words") or []
        split_segments: list[dict] = []
        for i in range(num_parts):
            start_ms = segment["start_ms"] + i * chunk_duration
            end_ms = start_ms + chunk_duration if i < num_parts - 1 else segment["end_ms"]
            segment_words = [
                word
                for word in words
                if start_ms <= word["start_ms"] < end_ms
                or start_ms <= word["end_ms"] <= end_ms
            ]
            split_segments.append(
                {
                    "segment_index": i,
                    "start_ms": start_ms,
                    "end_ms": end_ms,
                    "text": segment["text"],  # Keep full text; caller may refine.
                    "words": segment_words,
                }
            )
        return split_segments

    async def get_transcript(self, project_id: str) -> Optional[Transcript]:
        """Get the transcript record for a project."""
        stmt = select(Transcript).where(Transcript.project_id == uuid.UUID(project_id))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_segment(
        self,
        project_id: str,
        segment_index: int,
        text: Optional[str] = None,
        start_ms: Optional[int] = None,
        end_ms: Optional[int] = None,
    ) -> Optional[dict]:
        """Update a single transcript segment in-place."""
        transcript = await self.get_transcript(project_id)
        if not transcript or not transcript.segments:
            raise NotFoundException(f"Segment {segment_index} not found")

        segments = list(transcript.segments)
        if segment_index < 0 or segment_index >= len(segments):
            raise NotFoundException(f"Segment {segment_index} not found")

        segment = dict(segments[segment_index])
        if text is not None:
            segment["text"] = text.strip()
        if start_ms is not None:
            segment["start_ms"] = start_ms
        if end_ms is not None:
            segment["end_ms"] = end_ms

        segments[segment_index] = segment
        transcript.segments = segments
        await self.db.flush()
        await self.db.refresh(transcript)
        return segment

    async def split_segment(
        self,
        project_id: str,
        segment_index: int,
        split_at_ms: int,
    ) -> list[dict]:
        """Split a transcript segment at the given timestamp."""
        transcript = await self.get_transcript(project_id)
        if not transcript or not transcript.segments:
            raise NotFoundException(f"Segment {segment_index} not found")

        segments = list(transcript.segments)
        if segment_index < 0 or segment_index >= len(segments):
            raise NotFoundException(f"Segment {segment_index} not found")

        segment = dict(segments[segment_index])
        if split_at_ms <= segment["start_ms"] or split_at_ms >= segment["end_ms"]:
            raise ValueError("split_at_ms must be inside the segment time range")

        words = segment.get("words") or []
        first_words = [w for w in words if w["end_ms"] <= split_at_ms]
        second_words = [w for w in words if w["start_ms"] >= split_at_ms]

        first_text = " ".join(w["word"] for w in first_words).strip()
        second_text = " ".join(w["word"] for w in second_words).strip()

        first = {
            "segment_index": segment_index,
            "start_ms": segment["start_ms"],
            "end_ms": split_at_ms,
            "text": first_text or segment["text"],
            "words": first_words,
        }
        second = {
            "segment_index": segment_index + 1,
            "start_ms": split_at_ms,
            "end_ms": segment["end_ms"],
            "text": second_text or "",
            "words": second_words,
        }

        segments[segment_index] = first
        segments.insert(segment_index + 1, second)

        # Re-index
        for index, seg in enumerate(segments):
            seg["segment_index"] = index

        transcript.segments = segments
        await self.db.flush()
        await self.db.refresh(transcript)
        return [first, second]

    async def merge_segment_with_next(
        self,
        project_id: str,
        segment_index: int,
    ) -> dict:
        """Merge a segment with the following segment."""
        transcript = await self.get_transcript(project_id)
        if not transcript or not transcript.segments:
            raise NotFoundException(f"Segment {segment_index} not found")

        segments = list(transcript.segments)
        if segment_index < 0 or segment_index >= len(segments) - 1:
            raise NotFoundException(f"Segment {segment_index} or next segment not found")

        merged = self._merge_two_segments(segments[segment_index], segments[segment_index + 1])
        segments[segment_index] = merged
        del segments[segment_index + 1]

        for index, seg in enumerate(segments):
            seg["segment_index"] = index

        transcript.segments = segments
        await self.db.flush()
        await self.db.refresh(transcript)
        return merged
