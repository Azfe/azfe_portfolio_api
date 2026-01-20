from fastapi import APIRouter
from app.api.v1.routers import (
    health_router,
    profile_router,
    contact_info_router,
    social_networks_router,
    projects_router,
    work_experience_router,
    skill_router,
    tools_router,
    education_router,
    additional_training_router,
    certification_router,
    contact_messages_router,
    cv_router
)

# Router principal de la versión 1 de la API
api_v1_router = APIRouter()

# ===== SISTEMA =====
api_v1_router.include_router(health_router.router)

# ===== INFORMACIÓN PERSONAL =====
api_v1_router.include_router(profile_router.router)
api_v1_router.include_router(contact_info_router.router)
api_v1_router.include_router(social_networks_router.router)

# ===== EXPERIENCIA PROFESIONAL =====
api_v1_router.include_router(work_experience_router.router)
api_v1_router.include_router(projects_router.router)

# ===== HABILIDADES =====
api_v1_router.include_router(skill_router.router)
api_v1_router.include_router(tools_router.router)

# ===== FORMACIÓN =====
api_v1_router.include_router(education_router.router)
api_v1_router.include_router(additional_training_router.router)
api_v1_router.include_router(certification_router.router)

# ===== CONTACTO =====
api_v1_router.include_router(contact_messages_router.router)

# ===== CV COMPLETO =====
api_v1_router.include_router(cv_router.router)