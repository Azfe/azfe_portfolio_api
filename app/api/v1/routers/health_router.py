from datetime import datetime

from fastapi import APIRouter

from app.config.settings import settings
from app.infrastructure.database.mongo_client import MongoDBClient

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Health check básico"""
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/health/db")
async def health_check_db():
    """Health check con verificación de base de datos"""
    db_ok = await MongoDBClient.health_check()

    return {
        "status": "ok" if db_ok else "error",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": "connected" if db_ok else "disconnected",
        "timestamp": datetime.utcnow().isoformat(),
    }
