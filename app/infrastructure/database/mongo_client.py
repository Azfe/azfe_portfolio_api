import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config.settings import settings

logger = logging.getLogger(__name__)


class MongoDBClient:
    """Cliente MongoDB usando Motor (async). Patrón singleton a nivel de clase."""

    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None

    @classmethod
    async def connect(cls) -> None:
        """Inicializa el cliente y verifica la conexión a MongoDB."""
        try:
            logger.info("Conectando a MongoDB: %s", settings.MONGODB_URL)
            cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
            cls.db = cls.client[settings.MONGODB_DB_NAME]

            await cls.client.admin.command("ping")
            logger.info("Conectado a MongoDB: %s", settings.MONGODB_DB_NAME)

        except Exception as e:
            logger.error("Error conectando a MongoDB: %s", e)
            raise

    @classmethod
    async def disconnect(cls) -> None:
        """Cierra la conexión a MongoDB."""
        if cls.client is not None:
            logger.info("Desconectando de MongoDB")
            cls.client.close()
            cls.client = None
            cls.db = None
            logger.info("Desconectado de MongoDB")

    @classmethod
    async def health_check(cls) -> bool:
        """Verifica que la conexión a MongoDB esté activa."""
        if cls.client is None:
            return False
        try:
            await cls.client.admin.command("ping")
            return True
        except Exception:
            return False

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """Obtiene la instancia de la base de datos."""
        if cls.db is None:
            raise RuntimeError(
                "Base de datos no inicializada. Llama a connect() primero."
            )
        return cls.db


async def get_database() -> AsyncIOMotorDatabase:
    """Dependency injection para obtener la BD en los routers de FastAPI."""
    return MongoDBClient.get_db()
