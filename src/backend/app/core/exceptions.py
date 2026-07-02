"""
Custom Exception Classes
Hierarchical exception system for structured error handling
"""

from typing import Any, Dict, Optional


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str = "An application error occurred",
        status_code: int = 500,
        detail: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(self.message)


# ─── 404 Not Found ───────────────────────────────────────────
class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", detail: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=404, detail=detail)


class ProjectNotFoundException(NotFoundException):
    def __init__(self, project_id: str):
        super().__init__(message=f"Project '{project_id}' not found", detail={"project_id": project_id})


class VideoNotFoundException(NotFoundException):
    def __init__(self, video_id: str):
        super().__init__(message=f"Video '{video_id}' not found", detail={"video_id": video_id})


class TranscriptNotFoundException(NotFoundException):
    def __init__(self, project_id: str):
        super().__init__(message=f"Transcript for project '{project_id}' not found", detail={"project_id": project_id})


class VoiceProfileNotFoundException(NotFoundException):
    def __init__(self, voice_id: str):
        super().__init__(message=f"Voice profile '{voice_id}' not found", detail={"voice_id": voice_id})


# ─── 400 Validation ──────────────────────────────────────────
class ValidationException(AppException):
    def __init__(self, message: str = "Validation error", detail: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=400, detail=detail)


class InvalidFileFormatException(ValidationException):
    def __init__(self, format: str):
        super().__init__(message=f"Invalid file format: '{format}'", detail={"format": format})


class FileTooLargeException(ValidationException):
    def __init__(self, size: int, max_size: int):
        super().__init__(
            message=f"File too large: {size} bytes (max {max_size} bytes)",
            detail={"size": size, "max_size": max_size},
        )


class PipelineStepMissingException(ValidationException):
    def __init__(self, step: str):
        super().__init__(message=f"Pipeline step '{step}' must be completed first", detail={"step": step})


# ─── 409 Conflict ────────────────────────────────────────────
class TaskException(AppException):
    def __init__(self, message: str = "Task error", status_code: int = 409, detail: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=status_code, detail=detail)


class TaskInProgressException(TaskException):
    def __init__(self, task_type: str):
        super().__init__(message=f"Task '{task_type}' is already in progress", detail={"task_type": task_type})


class EngineUnavailableException(TaskException):
    def __init__(self, engine: str):
        super().__init__(
            message=f"Engine '{engine}' is not available",
            status_code=503,
            detail={"engine": engine},
        )


class GPUNotAvailableException(TaskException):
    def __init__(self):
        super().__init__(
            message="GPU is not available, falling back to CPU",
            status_code=503,
            detail={"fallback": "cpu"},
        )


# ─── 500 Internal ────────────────────────────────────────────
class InternalException(AppException):
    def __init__(self, message: str = "Internal server error", detail: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=500, detail=detail)


class DatabaseException(InternalException):
    def __init__(self, message: str = "Database operation failed", detail: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, detail=detail)