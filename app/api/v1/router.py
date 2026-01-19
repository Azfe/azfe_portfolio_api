from fastapi import APIRouter
from app.api.v1.routers import health_router

# Router principal de la versión 1 de la API
api_v1_router = APIRouter()

# Incluir todos los routers
api_v1_router.include_router(
    health_router.router,
    tags=["Health"]
)

# Aquí añadirás más routers conforme los vayas creando:
# api_v1_router.include_router(profile_router.router, prefix="/profile", tags=["Profile"])
# api_v1_router.include_router(experience_router.router, prefix="/experiences", tags=["Experience"])
# api_v1_router.include_router(skill_router.router, prefix="/skills", tags=["Skills"])
# api_v1_router.include_router(cv_router.router, prefix="/cv", tags=["CV"])