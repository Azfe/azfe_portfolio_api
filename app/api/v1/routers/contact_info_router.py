from datetime import datetime

from fastapi import APIRouter, status

from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.contact_info_schema import (
    ContactInformationCreate,
    ContactInformationResponse,
    ContactInformationUpdate,
)

router = APIRouter(prefix="/contact-information", tags=["Contact Information"])

# Mock data - Información de contacto ÚNICA del perfil
MOCK_CONTACT_INFO = ContactInformationResponse(
    id="contact_001",
    email="juan.perez@example.com",
    phone="+34 600 123 456",
    location="Valencia, España",
    website="https://juanperez.dev",
    created_at=datetime.now(),
    updated_at=datetime.now(),
)


@router.get(
    "",
    response_model=ContactInformationResponse,
    summary="Obtener información de contacto",
    description="Obtiene la información de contacto pública del perfil",
)
async def get_contact_information():
    """
    Obtiene la información de contacto del perfil único del sistema.

    **Invariante**: Solo existe UNA información de contacto por perfil (relación 1-a-1).

    Returns:
        ContactInformationResponse: Información de contacto del perfil

    Relación:
    - Pertenece al Profile único del sistema
    - Relación 1-a-1 (un perfil tiene una sola info de contacto)

    TODO: Implementar con GetContactInformationUseCase
    """
    return MOCK_CONTACT_INFO


@router.put(
    "",
    response_model=ContactInformationResponse,
    summary="Actualizar información de contacto",
    description="Actualiza la información de contacto del perfil",
)
async def update_contact_information(_contact_data: ContactInformationUpdate):
    """
    Actualiza la información de contacto del perfil.

    **Invariante**: Solo puede haber UNA información de contacto por perfil.

    Este endpoint actualiza el registro único existente, no crea uno nuevo.

    Args:
        contact_data: Datos a actualizar (campos opcionales)

    Returns:
        ContactInformationResponse: Información de contacto actualizada

    Raises:
        HTTPException 404: Si no existe información de contacto
        HTTPException 422: Si email no es válido

    TODO: Implementar con UpdateContactInformationUseCase
    TODO: Requiere autenticación de admin
    """
    return MOCK_CONTACT_INFO


@router.post(
    "",
    response_model=ContactInformationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear información de contacto inicial",
    description="Crea la información de contacto del perfil (solo si no existe)",
)
async def create_contact_information(_contact_data: ContactInformationCreate):
    """
    Crea la información de contacto inicial del perfil.

    **Invariante crítico**: Solo puede existir UNA información de contacto por perfil.

    Este endpoint solo debe ejecutarse UNA VEZ en la vida del sistema,
    durante la configuración inicial del perfil.

    Args:
        contact_data: Datos de la información de contacto

    Returns:
        ContactInformationResponse: Información de contacto creada

    Raises:
        HTTPException 409: Si ya existe información de contacto en el perfil
        HTTPException 422: Si email no es válido

    TODO: Implementar con CreateContactInformationUseCase
    TODO: Validar que NO exista ya información de contacto antes de crear
    TODO: Requiere autenticación de admin
    """
    # Mock: Simular que ya existe información de contacto
    # raise HTTPException(
    #     status_code=status.HTTP_409_CONFLICT,
    #     detail="Ya existe información de contacto para este perfil. Solo puede haber una."
    # )

    return MOCK_CONTACT_INFO


@router.delete(
    "",
    response_model=MessageResponse,
    summary="Eliminar información de contacto (PELIGROSO)",
    description="Elimina la información de contacto del perfil",
)
async def delete_contact_information():
    """
    Elimina la información de contacto del perfil.

    ⚠️ **ENDPOINT PELIGROSO**: Esto eliminará toda la información de contacto.

    Dado que la información de contacto tiene una relación 1-a-1 con Profile,
    eliminarla dejará el perfil sin datos de contacto públicos.

    Returns:
        MessageResponse: Confirmación de eliminación

    Raises:
        HTTPException 404: Si no existe información de contacto

    TODO: Implementar con DeleteContactInformationUseCase
    TODO: Considerar soft delete en vez de hard delete
    TODO: Requiere autenticación de admin
    TODO: Considerar si debe permitirse eliminar o solo actualizar
    """
    return MessageResponse(
        success=True, message="Información de contacto eliminada correctamente"
    )
