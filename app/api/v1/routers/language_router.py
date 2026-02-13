from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.language_schema import (
    LanguageCreate,
    LanguageResponse,
    LanguageUpdate,
)

router = APIRouter(prefix="/languages", tags=["Languages"])

# Mock data
MOCK_LANGUAGES = [
    LanguageResponse(
        id="lang_001",
        name="Español",
        proficiency="c2",
        order_index=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    LanguageResponse(
        id="lang_002",
        name="English",
        proficiency="c1",
        order_index=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    LanguageResponse(
        id="lang_003",
        name="Français",
        proficiency="b1",
        order_index=2,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]


@router.get(
    "",
    response_model=list[LanguageResponse],
    summary="Listar idiomas",
)
async def list_languages(
    proficiency: str | None = None,
):
    """Obtener todos los idiomas del perfil."""
    results = MOCK_LANGUAGES
    if proficiency:
        results = [lang for lang in results if lang.proficiency == proficiency.lower()]
    return results


@router.get(
    "/{language_id}",
    response_model=LanguageResponse,
    summary="Obtener idioma por ID",
)
async def get_language(language_id: str):
    """Obtener un idioma por su ID."""
    for lang in MOCK_LANGUAGES:
        if lang.id == language_id:
            return lang
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Language {language_id} not found",
    )


@router.post(
    "",
    response_model=LanguageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear idioma",
)
async def create_language(data: LanguageCreate):
    """Crear un nuevo idioma."""
    return LanguageResponse(
        id="lang_new",
        name=data.name,
        proficiency=data.proficiency,
        order_index=data.order_index,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@router.put(
    "/{language_id}",
    response_model=LanguageResponse,
    summary="Actualizar idioma",
)
async def update_language(language_id: str, data: LanguageUpdate):
    """Actualizar un idioma existente."""
    for lang in MOCK_LANGUAGES:
        if lang.id == language_id:
            return LanguageResponse(
                id=lang.id,
                name=data.name or lang.name,
                proficiency=(
                    data.proficiency
                    if data.proficiency is not None
                    else lang.proficiency
                ),
                order_index=(
                    data.order_index
                    if data.order_index is not None
                    else lang.order_index
                ),
                created_at=lang.created_at,
                updated_at=datetime.now(),
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Language {language_id} not found",
    )


@router.delete(
    "/{language_id}",
    response_model=MessageResponse,
    summary="Eliminar idioma",
)
async def delete_language(language_id: str):
    """Eliminar un idioma."""
    for lang in MOCK_LANGUAGES:
        if lang.id == language_id:
            return MessageResponse(message=f"Language {language_id} deleted")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Language {language_id} not found",
    )
