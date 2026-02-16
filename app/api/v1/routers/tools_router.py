from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_add_tool_use_case,
    get_delete_tool_use_case,
    get_edit_tool_use_case,
    get_list_tools_use_case,
    get_tool_repository,
)
from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.tools_schema import ToolCreate, ToolResponse, ToolUpdate
from app.application.dto import (
    AddToolRequest,
    DeleteToolRequest,
    EditToolRequest,
    ListToolsRequest,
)
from app.application.dto import ToolResponse as ToolDTO
from app.application.use_cases.tool import (
    AddToolUseCase,
    DeleteToolUseCase,
    EditToolUseCase,
    ListToolsUseCase,
)
from app.infrastructure.repositories import ToolRepository
from app.shared.shared_exceptions import NotFoundException

router = APIRouter(prefix="/tools", tags=["Tools"])

PROFILE_ID = "default_profile"


@router.get(
    "",
    response_model=list[ToolResponse],
    summary="Listar herramientas",
    description="Obtiene todas las herramientas del perfil",
)
async def get_tools(
    category: str | None = None,
    use_case: ListToolsUseCase = Depends(get_list_tools_use_case),
):
    result = await use_case.execute(
        ListToolsRequest(profile_id=PROFILE_ID, category=category)
    )
    return result.tools


@router.get(
    "/grouped/by-category",
    response_model=dict,
    summary="Agrupar herramientas por categoría",
    description="Obtiene herramientas agrupadas por categoría",
)
async def get_tools_grouped_by_category(
    use_case: ListToolsUseCase = Depends(get_list_tools_use_case),
):
    result = await use_case.execute(ListToolsRequest(profile_id=PROFILE_ID))
    grouped: dict[str, list] = {}
    for tool in result.tools:
        if tool.category not in grouped:
            grouped[tool.category] = []
        grouped[tool.category].append(tool)
    return grouped


@router.get(
    "/stats/summary",
    response_model=dict,
    summary="Estadísticas de herramientas",
    description="Obtiene estadísticas sobre las herramientas del perfil",
)
async def get_tools_stats(
    use_case: ListToolsUseCase = Depends(get_list_tools_use_case),
):
    result = await use_case.execute(ListToolsRequest(profile_id=PROFILE_ID))
    stats: dict[str, Any] = {
        "total": len(result.tools),
        "by_category": {},
    }
    for tool in result.tools:
        stats["by_category"][tool.category] = (
            stats["by_category"].get(tool.category, 0) + 1
        )
    return stats


@router.get(
    "/{tool_id}",
    response_model=ToolResponse,
    summary="Obtener herramienta",
    description="Obtiene una herramienta específica por ID",
)
async def get_tool(
    tool_id: str,
    repo: ToolRepository = Depends(get_tool_repository),
):
    entity = await repo.get_by_id(tool_id)
    if not entity:
        raise NotFoundException("Tool", tool_id)
    return ToolDTO.from_entity(entity)


@router.post(
    "",
    response_model=ToolResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear herramienta",
    description="Crea una nueva herramienta asociada al perfil",
)
async def create_tool(
    tool_data: ToolCreate,
    use_case: AddToolUseCase = Depends(get_add_tool_use_case),
):
    result = await use_case.execute(
        AddToolRequest(
            profile_id=PROFILE_ID,
            name=tool_data.name,
            category=tool_data.category,
            order_index=tool_data.order_index,
            icon_url=tool_data.icon_url,
        )
    )
    return result


@router.put(
    "/{tool_id}",
    response_model=ToolResponse,
    summary="Actualizar herramienta",
    description="Actualiza una herramienta existente",
)
async def update_tool(
    tool_id: str,
    tool_data: ToolUpdate,
    use_case: EditToolUseCase = Depends(get_edit_tool_use_case),
):
    result = await use_case.execute(
        EditToolRequest(
            tool_id=tool_id,
            name=tool_data.name,
            category=tool_data.category,
            icon_url=tool_data.icon_url,
        )
    )
    return result


@router.delete(
    "/{tool_id}",
    response_model=MessageResponse,
    summary="Eliminar herramienta",
    description="Elimina una herramienta del perfil",
)
async def delete_tool(
    tool_id: str,
    use_case: DeleteToolUseCase = Depends(get_delete_tool_use_case),
):
    await use_case.execute(DeleteToolRequest(tool_id=tool_id))
    return MessageResponse(
        success=True, message=f"Herramienta '{tool_id}' eliminada correctamente"
    )


@router.patch(
    "/reorder",
    response_model=list[ToolResponse],
    summary="Reordenar herramientas",
    description="Actualiza el orderIndex de múltiples herramientas de una vez",
)
async def reorder_tools(_tool_orders: list[dict]):
    # TODO: Implementar con ReorderToolsUseCase
    return []
