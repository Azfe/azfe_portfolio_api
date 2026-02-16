from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_add_language_use_case,
    get_delete_language_use_case,
    get_edit_language_use_case,
    get_language_repository,
    get_list_languages_use_case,
)
from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.language_schema import (
    LanguageCreate,
    LanguageResponse,
    LanguageUpdate,
)
from app.application.dto import (
    AddLanguageRequest,
    DeleteLanguageRequest,
    EditLanguageRequest,
    ListLanguagesRequest,
)
from app.application.dto import LanguageResponse as LanguageDTO
from app.application.use_cases.language import (
    AddLanguageUseCase,
    DeleteLanguageUseCase,
    EditLanguageUseCase,
    ListLanguagesUseCase,
)
from app.infrastructure.repositories import LanguageRepository
from app.shared.shared_exceptions import NotFoundException

router = APIRouter(prefix="/languages", tags=["Languages"])

PROFILE_ID = "default_profile"


@router.get(
    "",
    response_model=list[LanguageResponse],
    summary="Listar idiomas",
)
async def list_languages(
    proficiency: str | None = None,
    use_case: ListLanguagesUseCase = Depends(get_list_languages_use_case),
):
    result = await use_case.execute(ListLanguagesRequest(profile_id=PROFILE_ID))
    languages = result.languages
    if proficiency:
        languages = [
            lang for lang in languages if lang.proficiency == proficiency.lower()
        ]
    return languages


@router.get(
    "/{language_id}",
    response_model=LanguageResponse,
    summary="Obtener idioma por ID",
)
async def get_language(
    language_id: str,
    repo: LanguageRepository = Depends(get_language_repository),
):
    entity = await repo.get_by_id(language_id)
    if not entity:
        raise NotFoundException("Language", language_id)
    return LanguageDTO.from_entity(entity)


@router.post(
    "",
    response_model=LanguageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear idioma",
)
async def create_language(
    data: LanguageCreate,
    use_case: AddLanguageUseCase = Depends(get_add_language_use_case),
):
    result = await use_case.execute(
        AddLanguageRequest(
            profile_id=PROFILE_ID,
            name=data.name,
            order_index=data.order_index,
            proficiency=data.proficiency,
        )
    )
    return result


@router.put(
    "/{language_id}",
    response_model=LanguageResponse,
    summary="Actualizar idioma",
)
async def update_language(
    language_id: str,
    data: LanguageUpdate,
    use_case: EditLanguageUseCase = Depends(get_edit_language_use_case),
):
    result = await use_case.execute(
        EditLanguageRequest(
            language_id=language_id,
            name=data.name,
            proficiency=data.proficiency,
        )
    )
    return result


@router.delete(
    "/{language_id}",
    response_model=MessageResponse,
    summary="Eliminar idioma",
)
async def delete_language(
    language_id: str,
    use_case: DeleteLanguageUseCase = Depends(get_delete_language_use_case),
):
    await use_case.execute(DeleteLanguageRequest(language_id=language_id))
    return MessageResponse(
        success=True, message=f"Idioma '{language_id}' eliminado correctamente"
    )
