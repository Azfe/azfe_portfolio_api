from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)


def setup_middleware(app: FastAPI):
    """Configurar middlewares de la aplicación"""
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )
    
    logger.info(f"✓ CORS configurado: {settings.CORS_ORIGINS}")