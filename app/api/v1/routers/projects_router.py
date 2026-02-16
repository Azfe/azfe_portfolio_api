from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_add_project_use_case,
    get_delete_project_use_case,
    get_edit_project_use_case,
    get_list_projects_use_case,
    get_project_repository,
)
from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.projects_schema import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.application.dto import (
    AddProjectRequest,
    DeleteProjectRequest,
    EditProjectRequest,
    ListProjectsRequest,
)
from app.application.dto import ProjectResponse as ProjectDTO
from app.application.use_cases.project import (
    AddProjectUseCase,
    DeleteProjectUseCase,
    EditProjectUseCase,
    ListProjectsUseCase,
)
from app.infrastructure.repositories import ProjectRepository
from app.shared.shared_exceptions import NotFoundException

router = APIRouter(prefix="/projects", tags=["Projects"])

PROFILE_ID = "default_profile"


@router.get(
    "",
    response_model=list[ProjectResponse],
    summary="Listar proyectos",
    description="Obtiene todos los proyectos del perfil ordenados por orderIndex",
)
async def get_projects(
    use_case: ListProjectsUseCase = Depends(get_list_projects_use_case),
):
    result = await use_case.execute(ListProjectsRequest(profile_id=PROFILE_ID))
    return result.projects


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Obtener proyecto",
    description="Obtiene un proyecto específico por ID",
)
async def get_project(
    project_id: str,
    repo: ProjectRepository = Depends(get_project_repository),
):
    entity = await repo.get_by_id(project_id)
    if not entity:
        raise NotFoundException("Project", project_id)
    return ProjectDTO.from_entity(entity)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear proyecto",
    description="Crea un nuevo proyecto asociado al perfil",
)
async def create_project(
    project_data: ProjectCreate,
    use_case: AddProjectUseCase = Depends(get_add_project_use_case),
):
    result = await use_case.execute(
        AddProjectRequest(
            profile_id=PROFILE_ID,
            title=project_data.title,
            description=project_data.description,
            start_date=project_data.start_date,
            order_index=project_data.order_index,
            end_date=project_data.end_date,
            live_url=project_data.live_url,
            repo_url=project_data.repo_url,
            technologies=project_data.technologies,
        )
    )
    return result


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Actualizar proyecto",
    description="Actualiza un proyecto existente",
)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    use_case: EditProjectUseCase = Depends(get_edit_project_use_case),
):
    result = await use_case.execute(
        EditProjectRequest(
            project_id=project_id,
            title=project_data.title,
            description=project_data.description,
            start_date=project_data.start_date,
            end_date=project_data.end_date,
            live_url=project_data.live_url,
            repo_url=project_data.repo_url,
            technologies=project_data.technologies,
        )
    )
    return result


@router.delete(
    "/{project_id}",
    response_model=MessageResponse,
    summary="Eliminar proyecto",
    description="Elimina un proyecto del perfil",
)
async def delete_project(
    project_id: str,
    use_case: DeleteProjectUseCase = Depends(get_delete_project_use_case),
):
    await use_case.execute(DeleteProjectRequest(project_id=project_id))
    return MessageResponse(
        success=True, message=f"Proyecto '{project_id}' eliminado correctamente"
    )


@router.patch(
    "/reorder",
    response_model=list[ProjectResponse],
    summary="Reordenar proyectos",
    description="Actualiza el orderIndex de múltiples proyectos de una vez",
)
async def reorder_projects(_project_orders: list[dict]):
    # TODO: Implement with ReorderProjectsUseCase
    return []
