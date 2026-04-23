"""
Request/Response logging middleware.

Logs method, path, status code and duration for every request.
Skips noisy paths like /docs, /openapi.json and /health to keep logs clean.
"""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("app.api.access")

SKIP_PATHS = {"/docs", "/redoc", "/openapi.json", "/favicon.ico"}


class LoggingMiddleware(BaseHTTPMiddleware):
    """Logs every request with method, path, status and duration."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path = request.url.path

        if path in SKIP_PATHS:
            return await call_next(request)

        method = request.method
        start = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start) * 1000
        status_code = response.status_code

        logger.info(
            "%s %s → %d (%.1fms)",
            method,
            path,
            status_code,
            duration_ms,
        )

        return response
