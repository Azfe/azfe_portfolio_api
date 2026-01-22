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
        allow_origins=settings.cors_origins_list,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.cors_methods_list,
        allow_headers=settings.cors_headers_list,
    )
    
    logger.info(f"✓ CORS configurado: {settings.cors_origins_list}")