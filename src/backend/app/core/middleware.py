"""
FastAPI Middleware
Request logging, timing, error handling
"""

import logging
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all incoming requests with duration and status."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        try:
            response = await call_next(request)
        except AppException as exc:
            # Re-raise to let FastAPI exception handlers deal with it
            raise
        except Exception as exc:
            logger.exception("Unhandled exception in request")
            raise

        duration = time.time() - start_time
        logger.info(
            "%s %s → %d (%.3fs)",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )
        return response


class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    """Add X-Process-Time header to responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.3f}"
        return response