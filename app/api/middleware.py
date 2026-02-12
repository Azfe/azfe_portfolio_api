"""
Middleware registration.

Centralises the configuration and registration of all application middlewares.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.middlewares import LoggingMiddleware, ProcessTimeMiddleware
from app.config.settings import settings

logger = logging.getLogger(__name__)


def setup_middleware(app: FastAPI) -> None:
    """Register all middlewares on the FastAPI application.

    Registration order matters — middlewares execute in reverse order of
    registration (last registered runs first).  We register them so that
    the execution order is:

    1. ProcessTimeMiddleware  (outermost - measures total time)
    2. LoggingMiddleware      (logs after response is ready)
    3. CORSMiddleware         (innermost - handles preflight)
    """
    # --- CORS (innermost - registered first) ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.cors_methods_list,
        allow_headers=settings.cors_headers_list,
    )

    # --- Logging ---
    app.add_middleware(LoggingMiddleware)

    # --- Process time (outermost - registered last) ---
    app.add_middleware(ProcessTimeMiddleware)

    logger.info("Middlewares configured: CORS, Logging, ProcessTime")
    logger.info("CORS origins: %s", settings.cors_origins_list)
