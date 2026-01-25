from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime

from app.api.schemas.tools_schema import (
    ToolResponse,
    ToolCreate,
    ToolUpdate,
    ToolCategory,
    ToolKnowledgeLevel,
)
from app.api.schemas.common_schema import MessageResponse

router = APIRouter(prefix="/tools", tags=["Tools"])

# Mock data - Herramientas del perfil único
MOCK_TOOLS = [
    # IDE
    ToolResponse(
        id="tool_001",
        name="VS Code",
        category="ide",
        knowledge_level="expert",
        order_index=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ToolResponse(
        id="tool_002",
        name="PyCharm",
        category="ide",
        knowledge_level="advanced",
        order_index=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # Version Control
    ToolResponse(
        id="tool_003",
        name="Git",
        category="version_control",
        knowledge_level="expert",
        order_index=2,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ToolResponse(
        id="tool_004",
        name="GitHub",
        category="version_control",
        knowledge_level="expert",
        order_index=3,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # Containerization
    ToolResponse(
        id="tool_005",
        name="Docker",
        category="containerization",
        knowledge_level="advanced",
        order_index=4,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ToolResponse(
        id="tool_006",
        name="Kubernetes",
        category="containerization",
        knowledge_level="intermediate",
        order_index=5,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # Cloud
    ToolResponse(
        id="tool_007",
        name="AWS",
        category="cloud",
        knowledge_level="intermediate",
        order_index=6,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ToolResponse(
        id="tool_008",
        name="Vercel",
        category="cloud",
        knowledge_level="advanced",
        order_index=7,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # CI/CD
    ToolResponse(
        id="tool_009",
        name="GitHub Actions",
        category="ci_cd",
        knowledge_level="advanced",
        order_index=8,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ToolResponse(
        id="tool_010",
        name="Jenkins",
        category="ci_cd",
        knowledge_level="intermediate",
        order_index=9,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # Database Tools
    ToolResponse(
        id="tool_011",
        name="MongoDB Compass",
        category="database_tools",
        knowledge_level="advanced",
        order_index=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ToolResponse(
        id="tool_012",
        name="pgAdmin",
        category="database_tools",
        knowledge_level="intermediate",
        order_index=11,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # Testing Tools
    ToolResponse(
        id="tool_013",
        name="Postman",
        category="testing_tools",
        knowledge_level="expert",
        order_index=12,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # Design
    ToolResponse(
        id="tool_014",
        name="Figma",
        category="design",
        knowledge_level="intermediate",
        order_index=13,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # Project Management
    ToolResponse(
        id="tool_015",
        name="Jira",
        category="project_management",
        knowledge_level="advanced",
        order_index=14,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ToolResponse(
        id="tool_016",
        name="Notion",
        category="project_management",
        knowledge_level="advanced",
        order_index=15,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # Communication
    ToolResponse(
        id="tool_017",
        name="Slack",
        category="communication",
        knowledge_level="expert",
        order_index=16,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # Monitoring
    ToolResponse(
        id="tool_018",
        name="Grafana",
        category="monitoring",
        knowledge_level="basic",
        order_index=17,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]


@router.get(
    "",
    response_model=List[ToolResponse],
    summary="Listar herramientas",
    description="Obtiene todas las herramientas del perfil",
)
async def get_tools(
    category: ToolCategory = None, knowledge_level: ToolKnowledgeLevel = None
):
    """
    Lista todas las herramientas del perfil único del sistema.

    Puede filtrar por categoría y/o nivel de conocimiento.

    Args:
        category: Filtrar por categoría (ide, cloud, ci_cd, etc.)
        knowledge_level: Filtrar por nivel (basic, intermediate, advanced, expert)

    Returns:
        List[ToolResponse]: Lista de herramientas ordenadas por order_index

    Relación:
    - Todas las herramientas pertenecen al Profile único del sistema

    Ejemplos:
    - GET /tools?category=ide
    - GET /tools?knowledge_level=expert
    - GET /tools?category=cloud&knowledge_level=advanced

    TODO: Implementar con GetToolsUseCase
    TODO: Ordenar por order_index ASC
    """
    tools = MOCK_TOOLS

    if category:
        tools = [t for t in tools if t.category == category]

    if knowledge_level:
        tools = [t for t in tools if t.knowledge_level == knowledge_level]

    return sorted(tools, key=lambda x: x.order_index)


@router.get(
    "/{tool_id}",
    response_model=ToolResponse,
    summary="Obtener herramienta",
    description="Obtiene una herramienta específica por ID",
)
async def get_tool(tool_id: str):
    """
    Obtiene una herramienta por su ID.

    Args:
        tool_id: ID único de la herramienta

    Returns:
        ToolResponse: Herramienta encontrada

    Raises:
        HTTPException 404: Si la herramienta no existe

    TODO: Implementar con GetToolUseCase
    """
    for tool in MOCK_TOOLS:
        if tool.id == tool_id:
            return tool

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Herramienta con ID '{tool_id}' no encontrada",
    )


@router.post(
    "",
    response_model=ToolResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear herramienta",
    description="Crea una nueva herramienta asociada al perfil",
)
async def create_tool(tool_data: ToolCreate):
    """
    Crea una nueva herramienta y la asocia al perfil único del sistema.

    **Invariantes que se validan automáticamente:**
    - `name` no puede estar vacío (min_length=1)
    - `category` debe ser un valor permitido
    - `orderIndex` debe ser único dentro del perfil
    - `knowledge_level` si se proporciona, debe ser un valor permitido

    Args:
        tool_data: Datos de la herramienta a crear

    Returns:
        ToolResponse: Herramienta creada

    Raises:
        HTTPException 422: Si category o knowledge_level no son valores permitidos
        HTTPException 409: Si orderIndex ya está en uso
        HTTPException 400: Si los datos no cumplen las invariantes

    Nota sobre knowledge_level:
    - Es opcional, útil para herramientas que quieres destacar tu nivel de dominio
    - Puedes omitirlo si solo quieres listar la herramienta sin especificar nivel

    TODO: Implementar con CreateToolUseCase
    TODO: Validar que orderIndex sea único dentro del perfil
    TODO: Considerar auto-incrementar orderIndex si no se proporciona
    TODO: Requiere autenticación de admin
    """
    # Mock: Validar orderIndex único
    # if any(t.order_index == tool_data.order_index for t in MOCK_TOOLS):
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail=f"Ya existe una herramienta con orderIndex {tool_data.order_index}"
    #     )

    return MOCK_TOOLS[0]


@router.put(
    "/{tool_id}",
    response_model=ToolResponse,
    summary="Actualizar herramienta",
    description="Actualiza una herramienta existente",
)
async def update_tool(tool_id: str, tool_data: ToolUpdate):
    """
    Actualiza una herramienta existente.

    **Invariantes:**
    - Si se actualiza `name`, no puede estar vacío
    - Si se actualiza `category`, debe ser un valor permitido
    - Si se actualiza `knowledge_level`, debe ser un valor permitido
    - Si se actualiza `orderIndex`, debe ser único dentro del perfil

    Args:
        tool_id: ID de la herramienta a actualizar
        tool_data: Datos a actualizar (campos opcionales)

    Returns:
        ToolResponse: Herramienta actualizada

    Raises:
        HTTPException 404: Si la herramienta no existe
        HTTPException 422: Si category o knowledge_level no son válidos
        HTTPException 409: Si el nuevo orderIndex ya está en uso

    Caso de uso común:
    - Actualizar knowledge_level cuando mejoras en el uso de la herramienta
      (ej: de "intermediate" a "advanced")

    TODO: Implementar con UpdateToolUseCase
    TODO: Validar que orderIndex sea único si se actualiza
    TODO: Requiere autenticación de admin
    """
    for tool in MOCK_TOOLS:
        if tool.id == tool_id:
            return tool

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Herramienta con ID '{tool_id}' no encontrada",
    )


@router.delete(
    "/{tool_id}",
    response_model=MessageResponse,
    summary="Eliminar herramienta",
    description="Elimina una herramienta del perfil",
)
async def delete_tool(tool_id: str):
    """
    Elimina una herramienta del perfil.

    Nota: Al eliminar una herramienta, puede ser necesario reordenar
    los orderIndex de las herramientas restantes para mantener la coherencia.

    Args:
        tool_id: ID de la herramienta a eliminar

    Returns:
        MessageResponse: Confirmación de eliminación

    Raises:
        HTTPException 404: Si la herramienta no existe

    TODO: Implementar con DeleteToolUseCase
    TODO: Considerar reordenamiento automático de orderIndex
    TODO: Requiere autenticación de admin
    """
    return MessageResponse(
        success=True, message=f"Herramienta '{tool_id}' eliminada correctamente"
    )


@router.patch(
    "/reorder",
    response_model=List[ToolResponse],
    summary="Reordenar herramientas",
    description="Actualiza el orderIndex de múltiples herramientas de una vez",
)
async def reorder_tools(tool_orders: List[dict]):
    """
    Reordena múltiples herramientas de una sola vez.

    Útil para drag & drop en el panel de administración.

    Args:
        tool_orders: Lista de objetos con {id, orderIndex}
        Ejemplo: [
            {"id": "tool_001", "orderIndex": 0},
            {"id": "tool_002", "orderIndex": 1}
        ]

    Returns:
        List[ToolResponse]: Herramientas reordenadas

    Raises:
        HTTPException 400: Si hay orderIndex duplicados
        HTTPException 404: Si algún tool_id no existe

    TODO: Implementar con ReorderToolsUseCase
    TODO: Validar que todos los orderIndex sean únicos
    TODO: Validar que todos los tool_id existan
    TODO: Hacer update en transacción (todo o nada)
    TODO: Requiere autenticación de admin
    """
    return sorted(MOCK_TOOLS, key=lambda x: x.order_index)


@router.get(
    "/grouped/by-category",
    response_model=dict,
    summary="Agrupar herramientas por categoría",
    description="Obtiene herramientas agrupadas por categoría",
)
async def get_tools_grouped_by_category():
    """
    Agrupa herramientas por categoría.

    Útil para mostrar herramientas organizadas en secciones en el portfolio.

    Returns:
        dict: Diccionario con categorías como keys y listas de tools como values
        Ejemplo:
        {
            "ide": [tool1, tool2],
            "cloud": [tool3, tool4],
            "ci_cd": [tool5]
        }

    TODO: Implementar con GetToolsGroupedByCategoryUseCase
    TODO: Ordenar tools dentro de cada categoría por order_index
    TODO: Considerar ordenar categorías por prioridad
    """
    grouped = {}
    for tool in MOCK_TOOLS:
        if tool.category not in grouped:
            grouped[tool.category] = []
        grouped[tool.category].append(tool)

    # Ordenar tools dentro de cada categoría por order_index
    for category in grouped:
        grouped[category] = sorted(grouped[category], key=lambda x: x.order_index)

    return grouped


@router.get(
    "/grouped/by-knowledge-level",
    response_model=dict,
    summary="Agrupar herramientas por nivel de conocimiento",
    description="Obtiene herramientas agrupadas por nivel de conocimiento",
)
async def get_tools_grouped_by_knowledge_level():
    """
    Agrupa herramientas por nivel de conocimiento.

    Útil para destacar herramientas donde tienes expertise.

    Returns:
        dict: Diccionario con niveles como keys y listas de tools como values
        Ejemplo:
        {
            "expert": [tool1, tool2],
            "advanced": [tool3, tool4],
            "intermediate": [tool5],
            "none": [tool6]  # Herramientas sin knowledge_level
        }

    TODO: Implementar con GetToolsGroupedByKnowledgeLevelUseCase
    TODO: Ordenar tools dentro de cada nivel por order_index
    """
    grouped = {}
    for tool in MOCK_TOOLS:
        level = tool.knowledge_level or "none"
        if level not in grouped:
            grouped[level] = []
        grouped[level].append(tool)

    # Ordenar tools dentro de cada nivel por order_index
    for level in grouped:
        grouped[level] = sorted(grouped[level], key=lambda x: x.order_index)

    return grouped


@router.get(
    "/stats/summary",
    response_model=dict,
    summary="Estadísticas de herramientas",
    description="Obtiene estadísticas sobre las herramientas del perfil",
)
async def get_tools_stats():
    """
    Calcula estadísticas sobre las herramientas.

    Útil para mostrar métricas en el portfolio o admin panel.

    Returns:
        dict: Estadísticas
        Ejemplo:
        {
            "total": 18,
            "by_category": {
                "ide": 2,
                "cloud": 2,
                "ci_cd": 2,
                "version_control": 2,
                "containerization": 2
            },
            "by_knowledge_level": {
                "expert": 4,
                "advanced": 7,
                "intermediate": 6,
                "basic": 1
            },
            "with_knowledge_level": 18,
            "without_knowledge_level": 0
        }

    TODO: Implementar con GetToolsStatsUseCase
    """
    stats = {
        "total": len(MOCK_TOOLS),
        "by_category": {},
        "by_knowledge_level": {},
        "with_knowledge_level": 0,
        "without_knowledge_level": 0,
    }

    # Contar por categoría y nivel
    for tool in MOCK_TOOLS:
        # Por categoría
        stats["by_category"][tool.category] = (
            stats["by_category"].get(tool.category, 0) + 1
        )

        # Por nivel de conocimiento
        if tool.knowledge_level:
            stats["by_knowledge_level"][tool.knowledge_level] = (
                stats["by_knowledge_level"].get(tool.knowledge_level, 0) + 1
            )
            stats["with_knowledge_level"] += 1
        else:
            stats["without_knowledge_level"] += 1

    return stats
