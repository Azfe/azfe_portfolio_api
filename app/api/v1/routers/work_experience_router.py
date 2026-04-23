from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_add_experience_use_case,
    get_delete_experience_use_case,
    get_edit_experience_use_case,
    get_list_experiences_use_case,
    get_work_experience_repository,
)
from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.work_experience_schema import (
    WorkExperienceCreate,
    WorkExperienceResponse,
    WorkExperienceUpdate,
)
from app.application.dto import (
    AddExperienceRequest,
    DeleteExperienceRequest,
    EditExperienceRequest,
    ListExperiencesRequest,
    WorkExperienceResponse as WorkExperienceDTO,
)
from app.application.use_cases import (
    AddExperienceUseCase,
    DeleteExperienceUseCase,
    EditExperienceUseCase,
    ListExperiencesUseCase,
)
from app.infrastructure.repositories import WorkExperienceRepository
from app.shared.shared_exceptions import NotFoundException

router = APIRouter(prefix="/work-experiences", tags=["Work Experience"])

PROFILE_ID = "default_profile"


@router.get(
    "",
    response_model=list[WorkExperienceResponse],
    summary="Listar experiencias laborales",
    description="Obtiene todas las experiencias laborales ordenadas por orderIndex",
)
async def get_work_experiences(
    use_case: ListExperiencesUseCase = Depends(get_list_experiences_use_case),
):
    result = await use_case.execute(ListExperiencesRequest(profile_id=PROFILE_ID))
    return result.experiences


@router.get(
    "/{experience_id}",
    response_model=WorkExperienceResponse,
    summary="Obtener experiencia laboral",
    description="Obtiene una experiencia laboral específica por ID",
)
async def get_work_experience(
    experience_id: str,
    repo: WorkExperienceRepository = Depends(get_work_experience_repository),
):
    entity = await repo.get_by_id(experience_id)
    if not entity:
        raise NotFoundException("WorkExperience", experience_id)
    return WorkExperienceDTO.from_entity(entity)


@router.post(
    "",
    response_model=WorkExperienceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear experiencia laboral",
    description="Crea una nueva experiencia laboral asociada al perfil",
)
async def create_work_experience(
    experience_data: WorkExperienceCreate,
    use_case: AddExperienceUseCase = Depends(get_add_experience_use_case),
):
    result = await use_case.execute(
        AddExperienceRequest(
            profile_id=PROFILE_ID,
            role=experience_data.role,
            company=experience_data.company,
            start_date=experience_data.start_date,
            order_index=experience_data.order_index,
            description=experience_data.description,
            end_date=experience_data.end_date,
            responsibilities=experience_data.responsibilities or [],
        )
    )
    return result


@router.put(
    "/{experience_id}",
    response_model=WorkExperienceResponse,
    summary="Actualizar experiencia laboral",
    description="Actualiza una experiencia laboral existente",
)
async def update_work_experience(
    experience_id: str,
    experience_data: WorkExperienceUpdate,
    use_case: EditExperienceUseCase = Depends(get_edit_experience_use_case),
):
    result = await use_case.execute(
        EditExperienceRequest(
            experience_id=experience_id,
            role=experience_data.role,
            company=experience_data.company,
            description=experience_data.description,
            start_date=experience_data.start_date,
            end_date=experience_data.end_date,
            responsibilities=experience_data.responsibilities,
        )
    )
    return result


@router.delete(
    "/{experience_id}",
    response_model=MessageResponse,
    summary="Eliminar experiencia laboral",
    description="Elimina una experiencia laboral del perfil",
)
async def delete_work_experience(
    experience_id: str,
    use_case: DeleteExperienceUseCase = Depends(get_delete_experience_use_case),
):
    await use_case.execute(DeleteExperienceRequest(experience_id=experience_id))
    return MessageResponse(
        success=True,
        message=f"Experiencia laboral '{experience_id}' eliminada correctamente",
    )


@router.patch(
    "/reorder",
    response_model=list[WorkExperienceResponse],
    summary="Reordenar experiencias laborales",
    description="Actualiza el orderIndex de múltiples experiencias de una vez",
)
async def reorder_work_experiences(_experience_orders: list[dict]):
    # TODO: Implement with ReorderWorkExperiencesUseCase
    return []


@router.get(
    "/current/active",
    response_model=list[WorkExperienceResponse],
    summary="Obtener empleos actuales",
    description="Obtiene experiencias laborales donde aún se trabaja (endDate = None)",
)
async def get_current_work_experiences(
    use_case: ListExperiencesUseCase = Depends(get_list_experiences_use_case),
):
    result = await use_case.execute(ListExperiencesRequest(profile_id=PROFILE_ID))
    return [exp for exp in result.experiences if exp.is_current]


@router.get(
    "/by-company/{company}",
    response_model=list[WorkExperienceResponse],
    summary="Filtrar experiencias por empresa",
    description="Obtiene experiencias laborales de una empresa específica",
)
async def get_experiences_by_company(
    company: str,
    use_case: ListExperiencesUseCase = Depends(get_list_experiences_use_case),
):
    result = await use_case.execute(ListExperiencesRequest(profile_id=PROFILE_ID))
    company_lower = company.lower()
    return [exp for exp in result.experiences if company_lower in exp.company.lower()]
