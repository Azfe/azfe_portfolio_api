from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener URL de MongoDB
MONGODB_URL = os.getenv("MONGODB_URL")

try:
    # Intentar conectar
    client = MongoClient(MONGODB_URL)
    
    # Listar bases de datos
    print("✅ Conexión exitosa!")
    print("Bases de datos disponibles:")
    print(client.list_database_names())
    
except Exception as e:
    print(f"❌ Error de conexión: {e}")