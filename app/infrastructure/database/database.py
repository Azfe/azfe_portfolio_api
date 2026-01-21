from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    
db = MongoDB()

async def connect_to_mongo():
    """Conectar a MongoDB"""
    db.client = AsyncIOMotorClient(settings.mongodb_url)
    print(f"✅ Conectado a MongoDB: {settings.database_name}")

async def close_mongo_connection():
    """Cerrar conexión a MongoDB"""
    db.client.close()
    print("❌ Conexión a MongoDB cerrada")

def get_database():
    """Obtener instancia de la base de datos"""
    return db.client[settings.database_name]