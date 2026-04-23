import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.middleware import setup_middleware
from app.api.v1.router import api_v1_router
from app.config.settings import settings
from app.infrastructure.database.mongo_client import MongoDBClient

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación.
    Se ejecuta al inicio y al cierre del servidor.
    """
    # Startup
    logger.info(f"🚀 Iniciando {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"📍 Entorno: {settings.ENVIRONMENT}")

    # Conectar a MongoDB
    await MongoDBClient.connect()

    yield  # Aquí la aplicación está corriendo

    # Shutdown
    logger.info("🛑 Deteniendo aplicación...")
    await MongoDBClient.disconnect()
    logger.info("✓ Aplicación detenida")


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API REST para portfolio personal - Clean Architecture",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configurar middlewares
setup_middleware(app)

# Registrar exception handlers
register_exception_handlers(app)

# Incluir routers
app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": f"¡Bienvenido a {settings.PROJECT_NAME}!",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
