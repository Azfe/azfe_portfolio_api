from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.database import connect_to_mongo, close_mongo_connection
from app.routes.work_experience_route import router as work_experience_router

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="API para gestionar portfolio y CV"
)

# Configurar CORS (para permitir requests desde el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eventos de inicio y cierre
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Ruta raíz
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Portfolio API",
        "version": settings.api_version,
        "docs": "/docs"
    }

# Incluir rutas
app.include_router(work_experience_router, prefix="/api/v1")