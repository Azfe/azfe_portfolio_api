from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_add_additional_training_use_case,
    get_additional_training_repository,
    get_delete_additional_training_use_case,
    get_edit_additional_training_use_case,
    get_list_additional_trainings_use_case,
)
from app.api.schemas.additional_training_schema import (
    AdditionalTrainingCreate,
    AdditionalTrainingResponse,
    AdditionalTrainingUpdate,
)
from app.api.schemas.common_schema import MessageResponse
from app.application.dto import (
    AddAdditionalTrainingRequest,
    AdditionalTrainingResponse as AdditionalTrainingDTO,
    DeleteAdditionalTrainingRequest,
    EditAdditionalTrainingRequest,
    ListAdditionalTrainingsRequest,
)
from app.application.use_cases.additional_training import (
    AddAdditionalTrainingUseCase,
    DeleteAdditionalTrainingUseCase,
    EditAdditionalTrainingUseCase,
    ListAdditionalTrainingsUseCase,
)
from app.infrastructure.repositories import AdditionalTrainingRepository
from app.shared.shared_exceptions import NotFoundException

router = APIRouter(prefix="/additional-training", tags=["Additional Training"])

PROFILE_ID = "default_profile"


@router.get(
    "",
    response_model=list[AdditionalTrainingResponse],
    summary="Listar formación adicional",
    description="Obtiene toda la formación complementaria ordenada por orderIndex",
)
async def get_additional_trainings(
    use_case: ListAdditionalTrainingsUseCase = Depends(
        get_list_additional_trainings_use_case
    ),
):
    result = await use_case.execute(
        ListAdditionalTrainingsRequest(profile_id=PROFILE_ID)
    )
    return result.trainings


@router.get(
    "/{training_id}",
    response_model=AdditionalTrainingResponse,
    summary="Obtener formación adicional",
    description="Obtiene una formación adicional específica por ID",
)
async def get_additional_training(
    training_id: str,
    repo: AdditionalTrainingRepository = Depends(get_additional_training_repository),
):
    entity = await repo.get_by_id(training_id)
    if not entity:
        raise NotFoundException("AdditionalTraining", training_id)
    return AdditionalTrainingDTO.from_entity(entity)


@router.post(
    "",
    response_model=AdditionalTrainingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear formación adicional",
    description="Crea una nueva formación adicional asociada al perfil",
)
async def create_additional_training(
    training_data: AdditionalTrainingCreate,
    use_case: AddAdditionalTrainingUseCase = Depends(
        get_add_additional_training_use_case
    ),
):
    result = await use_case.execute(
        AddAdditionalTrainingRequest(
            profile_id=PROFILE_ID,
            title=training_data.title,
            provider=training_data.provider,
            completion_date=training_data.completion_date,
            order_index=training_data.order_index,
            duration=training_data.duration,
            certificate_url=training_data.certificate_url,
            description=training_data.description,
        )
    )
    return result


@router.put(
    "/{training_id}",
    response_model=AdditionalTrainingResponse,
    summary="Actualizar formación adicional",
    description="Actualiza una formación adicional existente",
)
async def update_additional_training(
    training_id: str,
    training_data: AdditionalTrainingUpdate,
    use_case: EditAdditionalTrainingUseCase = Depends(
        get_edit_additional_training_use_case
    ),
):
    result = await use_case.execute(
        EditAdditionalTrainingRequest(
            training_id=training_id,
            title=training_data.title,
            provider=training_data.provider,
            completion_date=training_data.completion_date,
            duration=training_data.duration,
            certificate_url=training_data.certificate_url,
            description=training_data.description,
        )
    )
    return result


@router.delete(
    "/{training_id}",
    response_model=MessageResponse,
    summary="Eliminar formación adicional",
    description="Elimina una formación adicional del perfil",
)
async def delete_additional_training(
    training_id: str,
    use_case: DeleteAdditionalTrainingUseCase = Depends(
        get_delete_additional_training_use_case
    ),
):
    await use_case.execute(DeleteAdditionalTrainingRequest(training_id=training_id))
    return MessageResponse(
        success=True,
        message=f"Formación adicional '{training_id}' eliminada correctamente",
    )


@router.patch(
    "/reorder",
    response_model=list[AdditionalTrainingResponse],
    summary="Reordenar formación adicional",
    description="Actualiza el orderIndex de múltiples formaciones de una vez",
)
async def reorder_additional_trainings(_training_orders: list[dict]):
    # TODO: Implement with ReorderAdditionalTrainingsUseCase
    return []
