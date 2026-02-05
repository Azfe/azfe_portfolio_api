from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import settings


class MongoDB:
    client: AsyncIOMotorClient | None = None


db = MongoDB()


async def connect_to_mongo():
    """Conectar a MongoDB"""
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    print(f"✅ Conectado a MongoDB: {settings.MONGODB_DB_NAME}")


async def close_mongo_connection():
    """Cerrar conexión a MongoDB"""
    if db.client:
        db.client.close()
        print("❌ Conexión a MongoDB cerrada")


def get_database():
    """Obtener instancia de la base de datos"""
    if db.client is None:
        raise RuntimeError(
            "MongoDB client not initialized. Call connect_to_mongo() first."
        )
    return db.client[settings.MONGODB_DB_NAME]
