from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.skill_schema import (
    SkillCreate,
    SkillLevel,
    SkillResponse,
    SkillUpdate,
)

router = APIRouter(prefix="/skills", tags=["Skills"])

# Mock data - Habilidades técnicas del perfil único
MOCK_SKILLS = [
    # Backend
    SkillResponse(
        id="skill_001",
        name="Python",
        level="expert",
        category="backend",
        order_index=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    SkillResponse(
        id="skill_002",
        name="FastAPI",
        level="expert",
        category="backend",
        order_index=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    SkillResponse(
        id="skill_003",
        name="Node.js",
        level="advanced",
        category="backend",
        order_index=2,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # Frontend
    SkillResponse(
        id="skill_004",
        name="React",
        level="advanced",
        category="frontend",
        order_index=3,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    SkillResponse(
        id="skill_005",
        name="TypeScript",
        level="advanced",
        category="frontend",
        order_index=4,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    SkillResponse(
        id="skill_006",
        name="Vue.js",
        level="intermediate",
        category="frontend",
        order_index=5,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # Database
    SkillResponse(
        id="skill_007",
        name="MongoDB",
        level="advanced",
        category="database",
        order_index=6,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    SkillResponse(
        id="skill_008",
        name="PostgreSQL",
        level="advanced",
        category="database",
        order_index=7,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # DevOps
    SkillResponse(
        id="skill_009",
        name="Docker",
        level="advanced",
        category="devops",
        order_index=8,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    SkillResponse(
        id="skill_010",
        name="Kubernetes",
        level="intermediate",
        category="devops",
        order_index=9,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # Cloud
    SkillResponse(
        id="skill_011",
        name="AWS",
        level="intermediate",
        category="cloud",
        order_index=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    # Testing
    SkillResponse(
        id="skill_012",
        name="Pytest",
        level="advanced",
        category="testing",
        order_index=11,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]


@router.get(
    "",
    response_model=list[SkillResponse],
    summary="Listar habilidades técnicas",
    description="Obtiene todas las habilidades técnicas del perfil",
)
async def get_skills(category: str | None = None, level: SkillLevel | None = None):
    """
    Lista todas las habilidades técnicas del perfil único del sistema.

    Puede filtrar por categoría y/o nivel.

    Args:
        category: Filtrar por categoría (backend, frontend, devops, etc.)
        level: Filtrar por nivel (basic, intermediate, advanced, expert)

    Returns:
        List[SkillResponse]: Lista de habilidades ordenadas por order_index

    Relación:
    - Todas las habilidades pertenecen al Profile único del sistema

    Ejemplos:
    - GET /skills?category=backend
    - GET /skills?level=expert
    - GET /skills?category=frontend&level=advanced

    TODO: Implementar con GetSkillsUseCase
    TODO: Ordenar por order_index ASC
    """
    skills = MOCK_SKILLS

    if category:
        skills = [s for s in skills if s.category == category]

    if level:
        skills = [s for s in skills if s.level == level]

    return sorted(skills, key=lambda x: x.order_index)


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Obtener habilidad técnica",
    description="Obtiene una habilidad técnica específica por ID",
)
async def get_skill(skill_id: str):
    """
    Obtiene una habilidad técnica por su ID.

    Args:
        skill_id: ID único de la habilidad

    Returns:
        SkillResponse: Habilidad encontrada

    Raises:
        HTTPException 404: Si la habilidad no existe

    TODO: Implementar con GetSkillUseCase
    """
    for skill in MOCK_SKILLS:
        if skill.id == skill_id:
            return skill

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Habilidad con ID '{skill_id}' no encontrada",
    )


@router.post(
    "",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear habilidad técnica",
    description="Crea una nueva habilidad técnica asociada al perfil",
)
async def create_skill(_skill_data: SkillCreate):
    """
    Crea una nueva habilidad técnica y la asocia al perfil único del sistema.

    **Invariantes que se validan automáticamente:**
    - `name` no puede estar vacío (min_length=1)
    - `level` debe ser: basic, intermediate, advanced, expert
    - `category` debe ser un valor válido
    - `orderIndex` debe ser único dentro del perfil

    Args:
        skill_data: Datos de la habilidad a crear

    Returns:
        SkillResponse: Habilidad creada

    Raises:
        HTTPException 422: Si level o category no son valores permitidos
        HTTPException 409: Si orderIndex ya está en uso
        HTTPException 400: Si los datos no cumplen las invariantes

    TODO: Implementar con CreateSkillUseCase
    TODO: Validar que orderIndex sea único dentro del perfil
    TODO: Considerar auto-incrementar orderIndex si no se proporciona
    TODO: Requiere autenticación de admin
    """
    return MOCK_SKILLS[0]


@router.put(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Actualizar habilidad técnica",
    description="Actualiza una habilidad técnica existente",
)
async def update_skill(skill_id: str, _skill_data: SkillUpdate):
    """
    Actualiza una habilidad técnica existente.

    **Invariantes:**
    - Si se actualiza `name`, no puede estar vacío
    - Si se actualiza `level`, debe ser un valor permitido
    - Si se actualiza `category`, debe ser un valor permitido
    - Si se actualiza `orderIndex`, debe ser único dentro del perfil

    Args:
        skill_id: ID de la habilidad a actualizar
        skill_data: Datos a actualizar (campos opcionales)

    Returns:
        SkillResponse: Habilidad actualizada

    Raises:
        HTTPException 404: Si la habilidad no existe
        HTTPException 422: Si level o category no son válidos
        HTTPException 409: Si el nuevo orderIndex ya está en uso

    TODO: Implementar con UpdateSkillUseCase
    TODO: Validar que orderIndex sea único si se actualiza
    TODO: Requiere autenticación de admin
    """
    for skill in MOCK_SKILLS:
        if skill.id == skill_id:
            return skill

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Habilidad con ID '{skill_id}' no encontrada",
    )


@router.delete(
    "/{skill_id}",
    response_model=MessageResponse,
    summary="Eliminar habilidad técnica",
    description="Elimina una habilidad técnica del perfil",
)
async def delete_skill(skill_id: str):
    """
    Elimina una habilidad técnica del perfil.

    Nota: Al eliminar una habilidad, puede ser necesario reordenar
    los orderIndex de las habilidades restantes para mantener la coherencia.

    Args:
        skill_id: ID de la habilidad a eliminar

    Returns:
        MessageResponse: Confirmación de eliminación

    Raises:
        HTTPException 404: Si la habilidad no existe

    TODO: Implementar con DeleteSkillUseCase
    TODO: Considerar reordenamiento automático de orderIndex
    TODO: Requiere autenticación de admin
    """
    return MessageResponse(
        success=True, message=f"Habilidad '{skill_id}' eliminada correctamente"
    )


@router.patch(
    "/reorder",
    response_model=list[SkillResponse],
    summary="Reordenar habilidades técnicas",
    description="Actualiza el orderIndex de múltiples habilidades de una vez",
)
async def reorder_skills(_skill_orders: list[dict]):
    """
    Reordena múltiples habilidades técnicas de una sola vez.

    Útil para drag & drop en el panel de administración.

    Args:
        skill_orders: Lista de objetos con {id, orderIndex}
        Ejemplo: [
            {"id": "skill_001", "orderIndex": 0},
            {"id": "skill_002", "orderIndex": 1}
        ]

    Returns:
        List[SkillResponse]: Habilidades reordenadas

    Raises:
        HTTPException 400: Si hay orderIndex duplicados
        HTTPException 404: Si algún skill_id no existe

    TODO: Implementar con ReorderSkillsUseCase
    TODO: Validar que todos los orderIndex sean únicos
    TODO: Validar que todos los skill_id existan
    TODO: Hacer update en transacción (todo o nada)
    TODO: Requiere autenticación de admin
    """
    return sorted(MOCK_SKILLS, key=lambda x: x.order_index)


@router.get(
    "/grouped/by-category",
    response_model=dict,
    summary="Agrupar habilidades por categoría",
    description="Obtiene habilidades agrupadas por categoría",
)
async def get_skills_grouped_by_category():
    """
    Agrupa habilidades técnicas por categoría.

    Útil para mostrar skills organizadas en secciones en el portfolio.

    Returns:
        dict: Diccionario con categorías como keys y listas de skills como values
        Ejemplo:
        {
            "backend": [skill1, skill2],
            "frontend": [skill3, skill4],
            "devops": [skill5]
        }

    TODO: Implementar con GetSkillsGroupedByCategoryUseCase
    TODO: Ordenar skills dentro de cada categoría por order_index
    TODO: Considerar ordenar categorías por prioridad
    """
    grouped: dict[str, list[SkillResponse]] = {}
    for skill in MOCK_SKILLS:
        if skill.category not in grouped:
            grouped[skill.category] = []
        grouped[skill.category].append(skill)

    # Ordenar skills dentro de cada categoría por order_index
    for category in grouped:
        grouped[category] = sorted(grouped[category], key=lambda x: x.order_index)

    return grouped


@router.get(
    "/grouped/by-level",
    response_model=dict,
    summary="Agrupar habilidades por nivel",
    description="Obtiene habilidades agrupadas por nivel de dominio",
)
async def get_skills_grouped_by_level():
    """
    Agrupa habilidades técnicas por nivel de dominio.

    Útil para destacar expertise (mostrar primero las "expert").

    Returns:
        dict: Diccionario con niveles como keys y listas de skills como values
        Ejemplo:
        {
            "expert": [skill1, skill2],
            "advanced": [skill3, skill4],
            "intermediate": [skill5]
        }

    TODO: Implementar con GetSkillsGroupedByLevelUseCase
    TODO: Ordenar skills dentro de cada nivel por order_index
    """
    grouped: dict[str, list[SkillResponse]] = {}
    for skill in MOCK_SKILLS:
        level: SkillLevel = skill.level if skill.level is not None else "none"
        if level not in grouped:
            grouped[level] = []
        grouped[level].append(skill)

    # Ordenar skills dentro de cada nivel por order_index
    for key in grouped:
        grouped[key] = sorted(grouped[key], key=lambda x: x.order_index)

    return grouped


@router.get(
    "/stats/summary",
    response_model=dict,
    summary="Estadísticas de habilidades",
    description="Obtiene estadísticas sobre las habilidades del perfil",
)
async def get_skills_stats():
    """
    Calcula estadísticas sobre las habilidades técnicas.

    Útil para mostrar métricas en el portfolio o admin panel.

    Returns:
        dict: Estadísticas
        Ejemplo:
        {
            "total": 12,
            "by_level": {
                "expert": 2,
                "advanced": 6,
                "intermediate": 3,
                "basic": 1
            },
            "by_category": {
                "backend": 3,
                "frontend": 3,
                "database": 2,
                "devops": 2,
                "cloud": 1,
                "testing": 1
            }
        }

    TODO: Implementar con GetSkillsStatsUseCase
    """
    stats: dict[str, Any] = {
        "total": len(MOCK_SKILLS),
        "by_level": {},
        "by_category": {},
    }

    # Contar por nivel
    for skill in MOCK_SKILLS:
        level: SkillLevel = skill.level if skill.level is not None else "none"
        stats["by_level"][level] = stats["by_level"].get(level, 0) + 1
        stats["by_category"][skill.category] = (
            stats["by_category"].get(skill.category, 0) + 1
        )

    return stats
