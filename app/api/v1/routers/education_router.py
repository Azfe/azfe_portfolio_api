from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_add_education_use_case,
    get_delete_education_use_case,
    get_edit_education_use_case,
    get_education_repository,
)
from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.education_schema import (
    EducationCreate,
    EducationResponse,
    EducationUpdate,
)
from app.application.dto import (
    AddEducationRequest,
    DeleteEducationRequest,
    EditEducationRequest,
    EducationResponse as EducationDTO,
)
from app.application.use_cases import (
    AddEducationUseCase,
    DeleteEducationUseCase,
    EditEducationUseCase,
)
from app.infrastructure.repositories import EducationRepository
from app.shared.shared_exceptions import NotFoundException

router = APIRouter(prefix="/education", tags=["Education"])

PROFILE_ID = "default_profile"


@router.get(
    "",
    response_model=list[EducationResponse],
    summary="Listar formación académica",
    description="Obtiene toda la formación académica ordenada por orderIndex",
)
async def get_education(
    repo: EducationRepository = Depends(get_education_repository),
):
    entities = await repo.find_by(profile_id=PROFILE_ID)
    entities.sort(key=lambda e: e.order_index)
    return [EducationDTO.from_entity(e) for e in entities]


@router.get(
    "/{education_id}",
    response_model=EducationResponse,
    summary="Obtener formación académica",
    description="Obtiene una formación académica específica por ID",
)
async def get_education_by_id(
    education_id: str,
    repo: EducationRepository = Depends(get_education_repository),
):
    entity = await repo.get_by_id(education_id)
    if not entity:
        raise NotFoundException("Education", education_id)
    return EducationDTO.from_entity(entity)


@router.post(
    "",
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear formación académica",
    description="Crea una nueva formación académica asociada al perfil",
)
async def create_education(
    education_data: EducationCreate,
    use_case: AddEducationUseCase = Depends(get_add_education_use_case),
):
    result = await use_case.execute(
        AddEducationRequest(
            profile_id=PROFILE_ID,
            institution=education_data.institution,
            degree=education_data.degree,
            field=education_data.field,
            start_date=education_data.start_date,
            order_index=education_data.order_index,
            description=education_data.description,
            end_date=education_data.end_date,
        )
    )
    return result


@router.put(
    "/{education_id}",
    response_model=EducationResponse,
    summary="Actualizar formación académica",
    description="Actualiza una formación académica existente",
)
async def update_education(
    education_id: str,
    education_data: EducationUpdate,
    use_case: EditEducationUseCase = Depends(get_edit_education_use_case),
):
    result = await use_case.execute(
        EditEducationRequest(
            education_id=education_id,
            institution=education_data.institution,
            degree=education_data.degree,
            field=education_data.field,
            description=education_data.description,
            start_date=education_data.start_date,
            end_date=education_data.end_date,
        )
    )
    return result


@router.delete(
    "/{education_id}",
    response_model=MessageResponse,
    summary="Eliminar formación académica",
    description="Elimina una formación académica del perfil",
)
async def delete_education(
    education_id: str,
    use_case: DeleteEducationUseCase = Depends(get_delete_education_use_case),
):
    await use_case.execute(DeleteEducationRequest(education_id=education_id))
    return MessageResponse(
        success=True,
        message=f"Formación académica '{education_id}' eliminada correctamente",
    )


@router.patch(
    "/reorder",
    response_model=list[EducationResponse],
    summary="Reordenar formación académica",
    description="Actualiza el orderIndex de múltiples formaciones de una vez",
)
async def reorder_education(_education_orders: list[dict]):
    # TODO: Implement with ReorderEducationUseCase
    return []
