from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_create_contact_information_use_case,
    get_delete_contact_information_use_case,
    get_get_contact_information_use_case,
    get_update_contact_information_use_case,
)
from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.contact_info_schema import (
    ContactInformationCreate,
    ContactInformationResponse,
    ContactInformationUpdate,
)
from app.application.dto import (
    CreateContactInformationRequest,
    DeleteContactInformationRequest,
    GetContactInformationRequest,
    UpdateContactInformationRequest,
)
from app.application.use_cases.contact_information import (
    CreateContactInformationUseCase,
    DeleteContactInformationUseCase,
    GetContactInformationUseCase,
    UpdateContactInformationUseCase,
)

router = APIRouter(prefix="/contact-information", tags=["Contact Information"])

PROFILE_ID = "default_profile"


@router.get(
    "",
    response_model=ContactInformationResponse,
    summary="Obtener información de contacto",
    description="Obtiene la información de contacto pública del perfil",
)
async def get_contact_information(
    use_case: GetContactInformationUseCase = Depends(
        get_get_contact_information_use_case
    ),
):
    result = await use_case.execute(GetContactInformationRequest(profile_id=PROFILE_ID))
    return result


@router.post(
    "",
    response_model=ContactInformationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear información de contacto inicial",
    description="Crea la información de contacto del perfil (solo si no existe)",
)
async def create_contact_information(
    contact_data: ContactInformationCreate,
    use_case: CreateContactInformationUseCase = Depends(
        get_create_contact_information_use_case
    ),
):
    result = await use_case.execute(
        CreateContactInformationRequest(
            profile_id=PROFILE_ID,
            email=contact_data.email,
            phone=contact_data.phone,
            linkedin=contact_data.linkedin,
            github=contact_data.github,
            website=contact_data.website,
        )
    )
    return result


@router.put(
    "",
    response_model=ContactInformationResponse,
    summary="Actualizar información de contacto",
    description="Actualiza la información de contacto del perfil",
)
async def update_contact_information(
    contact_data: ContactInformationUpdate,
    use_case: UpdateContactInformationUseCase = Depends(
        get_update_contact_information_use_case
    ),
):
    result = await use_case.execute(
        UpdateContactInformationRequest(
            profile_id=PROFILE_ID,
            email=contact_data.email,
            phone=contact_data.phone,
            linkedin=contact_data.linkedin,
            github=contact_data.github,
            website=contact_data.website,
        )
    )
    return result


@router.delete(
    "",
    response_model=MessageResponse,
    summary="Eliminar información de contacto",
    description="Elimina la información de contacto del perfil",
)
async def delete_contact_information(
    use_case: DeleteContactInformationUseCase = Depends(
        get_delete_contact_information_use_case
    ),
):
    await use_case.execute(DeleteContactInformationRequest(profile_id=PROFILE_ID))
    return MessageResponse(
        success=True, message="Información de contacto eliminada correctamente"
    )
