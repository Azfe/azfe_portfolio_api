from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.programming_language_schema import (
    ProgrammingLanguageCreate,
    ProgrammingLanguageResponse,
    ProgrammingLanguageUpdate,
)

router = APIRouter(prefix="/programming-languages", tags=["Programming Languages"])

# Mock data
MOCK_PROGRAMMING_LANGUAGES = [
    ProgrammingLanguageResponse(
        id="pl_001",
        name="Python",
        level="expert",
        order_index=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ProgrammingLanguageResponse(
        id="pl_002",
        name="TypeScript",
        level="advanced",
        order_index=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ProgrammingLanguageResponse(
        id="pl_003",
        name="Rust",
        level="intermediate",
        order_index=2,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ProgrammingLanguageResponse(
        id="pl_004",
        name="Go",
        level="basic",
        order_index=3,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]


@router.get(
    "",
    response_model=list[ProgrammingLanguageResponse],
    summary="Listar lenguajes de programación",
)
async def list_programming_languages(
    level: str | None = None,
):
    """Obtener todos los lenguajes de programación del perfil."""
    results = MOCK_PROGRAMMING_LANGUAGES
    if level:
        results = [pl for pl in results if pl.level == level.lower()]
    return results


@router.get(
    "/{programming_language_id}",
    response_model=ProgrammingLanguageResponse,
    summary="Obtener lenguaje de programación por ID",
)
async def get_programming_language(programming_language_id: str):
    """Obtener un lenguaje de programación por su ID."""
    for pl in MOCK_PROGRAMMING_LANGUAGES:
        if pl.id == programming_language_id:
            return pl
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Programming language {programming_language_id} not found",
    )


@router.post(
    "",
    response_model=ProgrammingLanguageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear lenguaje de programación",
)
async def create_programming_language(data: ProgrammingLanguageCreate):
    """Crear un nuevo lenguaje de programación."""
    return ProgrammingLanguageResponse(
        id="pl_new",
        name=data.name,
        level=data.level,
        order_index=data.order_index,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@router.put(
    "/{programming_language_id}",
    response_model=ProgrammingLanguageResponse,
    summary="Actualizar lenguaje de programación",
)
async def update_programming_language(
    programming_language_id: str, data: ProgrammingLanguageUpdate
):
    """Actualizar un lenguaje de programación existente."""
    for pl in MOCK_PROGRAMMING_LANGUAGES:
        if pl.id == programming_language_id:
            return ProgrammingLanguageResponse(
                id=pl.id,
                name=data.name or pl.name,
                level=data.level if data.level is not None else pl.level,
                order_index=data.order_index
                if data.order_index is not None
                else pl.order_index,
                created_at=pl.created_at,
                updated_at=datetime.now(),
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Programming language {programming_language_id} not found",
    )


@router.delete(
    "/{programming_language_id}",
    response_model=MessageResponse,
    summary="Eliminar lenguaje de programación",
)
async def delete_programming_language(programming_language_id: str):
    """Eliminar un lenguaje de programación."""
    for pl in MOCK_PROGRAMMING_LANGUAGES:
        if pl.id == programming_language_id:
            return MessageResponse(
                message=f"Programming language {programming_language_id} deleted"
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Programming language {programming_language_id} not found",
    )
