from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from app.api.schemas.profile_schema import (
    ProfileResponse,
    ProfileCreate,
    ProfileUpdate
)
from app.api.schemas.common_schema import MessageResponse

router = APIRouter(prefix="/profile", tags=["Profile"])

# Mock data - Simula el ÚNICO perfil del sistema
MOCK_PROFILE = ProfileResponse(
    id="profile_001",
    full_name="Juan Pérez García",
    headline="Full Stack Developer & Software Engineer",
    about="Desarrollador Full Stack apasionado por crear soluciones escalables y maintener código limpio. Especializado en Python, FastAPI, React y arquitecturas limpias. Con más de 5 años de experiencia en desarrollo web y APIs RESTful.",
    location="Valencia, España (Remoto)",
    profile_image="https://example.com/images/profile.jpg",
    banner_image="https://example.com/images/banner.jpg",
    created_at=datetime.now(),
    updated_at=datetime.now()
)


@router.get(
    "",
    response_model=ProfileResponse,
    summary="Obtener perfil",
    description="Obtiene el perfil único del sistema"
)
async def get_profile():
    """
    Obtiene el perfil profesional.
    
    **Invariante**: Solo existe UN perfil en el sistema.
    
    Returns:
        ProfileResponse: El perfil único del usuario
    
    TODO: Implementar con GetProfileUseCase
    """
    return MOCK_PROFILE


@router.put(
    "",
    response_model=ProfileResponse,
    summary="Actualizar perfil",
    description="Actualiza la información del perfil único"
)
async def update_profile(profile_data: ProfileUpdate):
    """
    Actualiza el perfil profesional.
    
    **Invariantes**:
    - `full_name` no puede estar vacío
    - `headline` no puede estar vacío
    
    Args:
        profile_data: Datos a actualizar (campos opcionales)
    
    Returns:
        ProfileResponse: Perfil actualizado
    
    TODO: Implementar con UpdateProfileUseCase
    TODO: Validar que full_name y headline no queden vacíos
    """
    return MOCK_PROFILE


@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear perfil inicial",
    description="Crea el perfil único del sistema (solo si no existe)"
)
async def create_profile(profile_data: ProfileCreate):
    """
    Crea el perfil profesional inicial.
    
    **Invariante crítico**: Solo puede existir UN perfil en el sistema.
    
    Este endpoint solo debe ejecutarse UNA VEZ en la vida del sistema,
    durante la configuración inicial.
    
    Args:
        profile_data: Datos del perfil a crear
    
    Returns:
        ProfileResponse: Perfil creado
    
    Raises:
        HTTPException 409: Si ya existe un perfil en el sistema
    
    TODO: Implementar con CreateProfileUseCase
    TODO: Validar que NO exista ya un perfil antes de crear
    """
    # Mock: Simular que ya existe un perfil
    # raise HTTPException(
    #     status_code=status.HTTP_409_CONFLICT,
    #     detail="Ya existe un perfil en el sistema. Solo puede haber uno."
    # )
    
    return MOCK_PROFILE


@router.delete(
    "",
    response_model=MessageResponse,
    summary="Eliminar perfil (PELIGROSO)",
    description="Elimina el perfil único del sistema"
)
async def delete_profile():
    """
    Elimina el perfil del sistema.
    
    ⚠️ **ENDPOINT PELIGROSO**: Esto eliminará TODA la información del perfil.
    
    Dado que el perfil tiene relaciones con:
    - Projects
    - Education
    - AdditionalTraining
    - Certification
    - TechnicalSkill
    - Tool
    - ContactInformation
    - ContactMessage
    - SocialNetwork
    
    Se debe decidir la estrategia de cascada (eliminar todo o fallar).
    
    TODO: Implementar con DeleteProfileUseCase
    TODO: Decidir estrategia de eliminación en cascada
    TODO: Requiere autenticación de admin
    TODO: Considerar soft delete en vez de hard delete
    """
    return MessageResponse(
        success=True,
        message="Perfil eliminado correctamente (y todas sus relaciones)"
    )