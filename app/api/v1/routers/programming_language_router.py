from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_add_programming_language_use_case,
    get_delete_programming_language_use_case,
    get_edit_programming_language_use_case,
    get_list_programming_languages_use_case,
    get_programming_language_repository,
)
from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.programming_language_schema import (
    ProgrammingLanguageCreate,
    ProgrammingLanguageResponse,
    ProgrammingLanguageUpdate,
)
from app.application.dto import (
    AddProgrammingLanguageRequest,
    DeleteProgrammingLanguageRequest,
    EditProgrammingLanguageRequest,
    ListProgrammingLanguagesRequest,
)
from app.application.dto import ProgrammingLanguageResponse as ProgrammingLanguageDTO
from app.application.use_cases.programming_language import (
    AddProgrammingLanguageUseCase,
    DeleteProgrammingLanguageUseCase,
    EditProgrammingLanguageUseCase,
    ListProgrammingLanguagesUseCase,
)
from app.infrastructure.repositories import ProgrammingLanguageRepository
from app.shared.shared_exceptions import NotFoundException

router = APIRouter(prefix="/programming-languages", tags=["Programming Languages"])

PROFILE_ID = "default_profile"


@router.get(
    "",
    response_model=list[ProgrammingLanguageResponse],
    summary="Listar lenguajes de programación",
)
async def list_programming_languages(
    level: str | None = None,
    use_case: ListProgrammingLanguagesUseCase = Depends(
        get_list_programming_languages_use_case
    ),
):
    result = await use_case.execute(
        ListProgrammingLanguagesRequest(profile_id=PROFILE_ID)
    )
    languages = result.programming_languages
    if level:
        languages = [pl for pl in languages if pl.level == level.lower()]
    return languages


@router.get(
    "/{programming_language_id}",
    response_model=ProgrammingLanguageResponse,
    summary="Obtener lenguaje de programación por ID",
)
async def get_programming_language(
    programming_language_id: str,
    repo: ProgrammingLanguageRepository = Depends(get_programming_language_repository),
):
    entity = await repo.get_by_id(programming_language_id)
    if not entity:
        raise NotFoundException("ProgrammingLanguage", programming_language_id)
    return ProgrammingLanguageDTO.from_entity(entity)


@router.post(
    "",
    response_model=ProgrammingLanguageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear lenguaje de programación",
)
async def create_programming_language(
    data: ProgrammingLanguageCreate,
    use_case: AddProgrammingLanguageUseCase = Depends(
        get_add_programming_language_use_case
    ),
):
    result = await use_case.execute(
        AddProgrammingLanguageRequest(
            profile_id=PROFILE_ID,
            name=data.name,
            order_index=data.order_index,
            level=data.level,
        )
    )
    return result


@router.put(
    "/{programming_language_id}",
    response_model=ProgrammingLanguageResponse,
    summary="Actualizar lenguaje de programación",
)
async def update_programming_language(
    programming_language_id: str,
    data: ProgrammingLanguageUpdate,
    use_case: EditProgrammingLanguageUseCase = Depends(
        get_edit_programming_language_use_case
    ),
):
    result = await use_case.execute(
        EditProgrammingLanguageRequest(
            programming_language_id=programming_language_id,
            name=data.name,
            level=data.level,
        )
    )
    return result


@router.delete(
    "/{programming_language_id}",
    response_model=MessageResponse,
    summary="Eliminar lenguaje de programación",
)
async def delete_programming_language(
    programming_language_id: str,
    use_case: DeleteProgrammingLanguageUseCase = Depends(
        get_delete_programming_language_use_case
    ),
):
    await use_case.execute(
        DeleteProgrammingLanguageRequest(
            programming_language_id=programming_language_id
        )
    )
    return MessageResponse(
        success=True,
        message=f"Lenguaje de programación '{programming_language_id}' eliminado correctamente",
    )
