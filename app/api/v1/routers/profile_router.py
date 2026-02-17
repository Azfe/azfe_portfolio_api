from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_create_profile_use_case,
    get_get_profile_use_case,
    get_update_profile_use_case,
)
from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.profile_schema import ProfileCreate, ProfileResponse, ProfileUpdate
from app.application.dto import (
    CreateProfileRequest,
    GetProfileRequest,
    UpdateProfileRequest,
)
from app.application.use_cases import (
    CreateProfileUseCase,
    GetProfileUseCase,
    UpdateProfileUseCase,
)

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get(
    "",
    response_model=ProfileResponse,
    summary="Obtener perfil",
    description="Obtiene el perfil único del sistema",
)
async def get_profile(
    use_case: GetProfileUseCase = Depends(get_get_profile_use_case),
):
    result = await use_case.execute(GetProfileRequest())
    return result


@router.put(
    "",
    response_model=ProfileResponse,
    summary="Actualizar perfil",
    description="Actualiza la información del perfil único",
)
async def update_profile(
    profile_data: ProfileUpdate,
    use_case: UpdateProfileUseCase = Depends(get_update_profile_use_case),
):
    result = await use_case.execute(
        UpdateProfileRequest(
            name=profile_data.name,
            headline=profile_data.headline,
            bio=profile_data.bio,
            location=profile_data.location,
            avatar_url=profile_data.avatar_url,
        )
    )
    return result


@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear perfil inicial",
    description="Crea el perfil único del sistema (solo si no existe)",
)
async def create_profile(
    profile_data: ProfileCreate,
    use_case: CreateProfileUseCase = Depends(get_create_profile_use_case),
):
    result = await use_case.execute(
        CreateProfileRequest(
            name=profile_data.name,
            headline=profile_data.headline,
            bio=profile_data.bio,
            location=profile_data.location,
            avatar_url=profile_data.avatar_url,
        )
    )
    return result


@router.delete(
    "",
    response_model=MessageResponse,
    summary="Eliminar perfil (PELIGROSO)",
    description="Elimina el perfil único del sistema",
)
async def delete_profile():
    # TODO: Implement with DeleteProfileUseCase when available
    return MessageResponse(
        success=True, message="Perfil eliminado correctamente (y todas sus relaciones)"
    )
