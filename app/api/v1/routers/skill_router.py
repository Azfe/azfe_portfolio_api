from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_add_skill_use_case,
    get_delete_skill_use_case,
    get_edit_skill_use_case,
    get_list_skills_use_case,
    get_skill_repository,
)
from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.skill_schema import (
    SkillCreate,
    SkillLevel,
    SkillResponse,
    SkillUpdate,
)
from app.application.dto import (
    AddSkillRequest,
    DeleteSkillRequest,
    EditSkillRequest,
    ListSkillsRequest,
    SkillResponse as SkillDTO,
)
from app.application.use_cases import (
    AddSkillUseCase,
    DeleteSkillUseCase,
    EditSkillUseCase,
    ListSkillsUseCase,
)
from app.infrastructure.repositories import SkillRepository
from app.shared.shared_exceptions import NotFoundException

router = APIRouter(prefix="/skills", tags=["Skills"])

PROFILE_ID = "default_profile"


@router.get(
    "",
    response_model=list[SkillResponse],
    summary="Listar habilidades técnicas",
    description="Obtiene todas las habilidades técnicas del perfil",
)
async def get_skills(
    category: str | None = None,
    level: SkillLevel | None = None,
    use_case: ListSkillsUseCase = Depends(get_list_skills_use_case),
):
    result = await use_case.execute(
        ListSkillsRequest(profile_id=PROFILE_ID, category=category)
    )
    skills = result.skills
    if level:
        skills = [s for s in skills if s.level == level]
    return skills


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Obtener habilidad técnica",
    description="Obtiene una habilidad técnica específica por ID",
)
async def get_skill(
    skill_id: str,
    repo: SkillRepository = Depends(get_skill_repository),
):
    skill = await repo.get_by_id(skill_id)
    if not skill:
        raise NotFoundException("Skill", skill_id)
    return SkillDTO.from_entity(skill)


@router.post(
    "",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear habilidad técnica",
    description="Crea una nueva habilidad técnica asociada al perfil",
)
async def create_skill(
    skill_data: SkillCreate,
    use_case: AddSkillUseCase = Depends(get_add_skill_use_case),
):
    result = await use_case.execute(
        AddSkillRequest(
            profile_id=PROFILE_ID,
            name=skill_data.name,
            category=skill_data.category,
            order_index=skill_data.order_index,
            level=skill_data.level,
        )
    )
    return result


@router.put(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Actualizar habilidad técnica",
    description="Actualiza una habilidad técnica existente",
)
async def update_skill(
    skill_id: str,
    skill_data: SkillUpdate,
    use_case: EditSkillUseCase = Depends(get_edit_skill_use_case),
):
    result = await use_case.execute(
        EditSkillRequest(
            skill_id=skill_id,
            name=skill_data.name,
            category=skill_data.category,
            level=skill_data.level,
        )
    )
    return result


@router.delete(
    "/{skill_id}",
    response_model=MessageResponse,
    summary="Eliminar habilidad técnica",
    description="Elimina una habilidad técnica del perfil",
)
async def delete_skill(
    skill_id: str,
    use_case: DeleteSkillUseCase = Depends(get_delete_skill_use_case),
):
    await use_case.execute(DeleteSkillRequest(skill_id=skill_id))
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
    # TODO: Implement with ReorderSkillsUseCase
    return []


@router.get(
    "/grouped/by-category",
    response_model=dict,
    summary="Agrupar habilidades por categoría",
    description="Obtiene habilidades agrupadas por categoría",
)
async def get_skills_grouped_by_category(
    use_case: ListSkillsUseCase = Depends(get_list_skills_use_case),
):
    result = await use_case.execute(ListSkillsRequest(profile_id=PROFILE_ID))
    grouped: dict[str, list] = {}
    for skill in result.skills:
        grouped.setdefault(skill.category, []).append(skill)
    return grouped


@router.get(
    "/grouped/by-level",
    response_model=dict,
    summary="Agrupar habilidades por nivel",
    description="Obtiene habilidades agrupadas por nivel de dominio",
)
async def get_skills_grouped_by_level(
    use_case: ListSkillsUseCase = Depends(get_list_skills_use_case),
):
    result = await use_case.execute(ListSkillsRequest(profile_id=PROFILE_ID))
    grouped: dict[str, list] = {}
    for skill in result.skills:
        level = skill.level if skill.level is not None else "none"
        grouped.setdefault(level, []).append(skill)
    return grouped


@router.get(
    "/stats/summary",
    response_model=dict,
    summary="Estadísticas de habilidades",
    description="Obtiene estadísticas sobre las habilidades del perfil",
)
async def get_skills_stats(
    use_case: ListSkillsUseCase = Depends(get_list_skills_use_case),
):
    result = await use_case.execute(ListSkillsRequest(profile_id=PROFILE_ID))
    stats: dict[str, Any] = {
        "total": result.total,
        "by_level": {},
        "by_category": {},
    }
    for skill in result.skills:
        level = skill.level if skill.level is not None else "none"
        stats["by_level"][level] = stats["by_level"].get(level, 0) + 1
        stats["by_category"][skill.category] = (
            stats["by_category"].get(skill.category, 0) + 1
        )
    return stats
