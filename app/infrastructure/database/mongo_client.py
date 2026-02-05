import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config.settings import settings

logger = logging.getLogger(__name__)


class MongoDBClient:
    """Cliente MongoDB usando Motor (async)"""

    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None

    @classmethod
    async def connect(cls):
        """Conectar a MongoDB"""
        try:
            logger.info(f"Conectando a MongoDB: {settings.MONGODB_URL}")
            cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
            cls.db = cls.client[settings.MONGODB_DB_NAME]

            # Test de conexión
            await cls.client.admin.command("ping")
            logger.info(f"✓ Conectado a MongoDB: {settings.MONGODB_DB_NAME}")

        except Exception as e:
            logger.error(f"✗ Error conectando a MongoDB: {e}")
            raise

    @classmethod
    async def disconnect(cls):
        """Desconectar de MongoDB"""
        if cls.client:
            logger.info("Desconectando de MongoDB")
            cls.client.close()
            logger.info("✓ Desconectado de MongoDB")

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """Obtener instancia de la base de datos"""
        if cls.db is None:
            raise RuntimeError(
                "Base de datos no inicializada. Llama a connect() primero."
            )
        return cls.db


# Función helper para dependency injection en FastAPI
async def get_database() -> AsyncIOMotorDatabase:
    """Dependency para obtener la BD en los routers"""
    return MongoDBClient.get_db()
