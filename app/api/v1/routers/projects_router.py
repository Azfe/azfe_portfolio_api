from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.projects_schema import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)

router = APIRouter(prefix="/projects", tags=["Projects"])

# Mock data - Proyectos del perfil único
MOCK_PROJECTS = [
    ProjectResponse(
        id="proj_001",
        title="Portfolio Personal con Clean Architecture",
        description="Portfolio web profesional desarrollado con Astro en el frontend y FastAPI en el backend, siguiendo principios de Clean Architecture. Incluye sistema de gestión de contenido dinámico con MongoDB, generación automática de CV en PDF y panel de administración para actualizar información sin tocar código.",
        start_date=datetime(2024, 1, 1),
        end_date=None,
        technologies=[
            "Astro",
            "FastAPI",
            "MongoDB",
            "Tailwind CSS",
            "Docker",
            "Python",
            "TypeScript",
        ],
        repo_url="https://github.com/juanperez/portfolio",
        live_url="https://juanperez.dev",
        order_index=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ProjectResponse(
        id="proj_002",
        title="E-commerce API REST",
        description="API REST completa para e-commerce con sistema de autenticación JWT, gestión de productos, inventario, carrito de compras y procesamiento de pagos con Stripe. Incluye sistema de notificaciones por email y webhooks para sincronización con sistemas externos.",
        start_date=datetime(2023, 6, 1),
        end_date=datetime(2024, 2, 15),
        technologies=[
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Stripe",
            "Redis",
            "Docker",
            "Celery",
        ],
        repo_url="https://github.com/juanperez/ecommerce-api",
        live_url="https://ecommerce-demo.juanperez.dev",
        order_index=2,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ProjectResponse(
        id="proj_003",
        title="Task Management Dashboard",
        description="Dashboard de gestión de tareas tipo Trello con drag & drop, colaboración en tiempo real usando WebSockets, notificaciones push y sistema de roles y permisos.",
        start_date=datetime(2022, 9, 1),
        end_date=datetime(2023, 3, 30),
        technologies=[
            "React",
            "Node.js",
            "Socket.io",
            "MongoDB",
            "Redux",
            "Material-UI",
        ],
        repo_url="https://github.com/juanperez/task-dashboard",
        live_url="https://tasks.juanperez.dev",
        order_index=3,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]


@router.get(
    "",
    response_model=list[ProjectResponse],
    summary="Listar proyectos",
    description="Obtiene todos los proyectos del perfil ordenados por orderIndex",
)
async def get_projects():
    """
    Lista todos los proyectos del perfil único del sistema.

    Los proyectos se retornan ordenados por `order_index` ascendente,
    mostrando primero los proyectos con menor índice (más importantes).

    Returns:
        List[ProjectResponse]: Lista de proyectos ordenados

    Relación:
    - Todos los proyectos pertenecen al Profile único del sistema

    TODO: Implementar con GetProjectsUseCase
    TODO: Ordenar por order_index ASC
    """
    return sorted(MOCK_PROJECTS, key=lambda x: x.order_index)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Obtener proyecto",
    description="Obtiene un proyecto específico por ID",
)
async def get_project(project_id: str):
    """
    Obtiene un proyecto por su ID.

    Args:
        project_id: ID único del proyecto

    Returns:
        ProjectResponse: Proyecto encontrado

    Raises:
        HTTPException 404: Si el proyecto no existe

    TODO: Implementar con GetProjectUseCase
    """
    for proj in MOCK_PROJECTS:
        if proj.id == project_id:
            return proj

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Proyecto con ID '{project_id}' no encontrado",
    )


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear proyecto",
    description="Crea un nuevo proyecto asociado al perfil",
)
async def create_project(_project_data: ProjectCreate):
    """
    Crea un nuevo proyecto y lo asocia al perfil único del sistema.

    **Invariantes que se deben validar:**
    - `title` no puede estar vacío
    - `description` no puede estar vacía
    - `orderIndex` debe ser único dentro del perfil

    Args:
        project_data: Datos del proyecto a crear

    Returns:
        ProjectResponse: Proyecto creado

    Raises:
        HTTPException 409: Si ya existe un proyecto con el mismo orderIndex
        HTTPException 400: Si los datos no cumplen las invariantes

    TODO: Implementar con CreateProjectUseCase
    TODO: Validar que orderIndex sea único
    TODO: Considerar auto-incrementar orderIndex si no se proporciona
    TODO: Requiere autenticación de admin
    """
    return MOCK_PROJECTS[0]


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Actualizar proyecto",
    description="Actualiza un proyecto existente",
)
async def update_project(project_id: str, _project_data: ProjectUpdate):
    """
    Actualiza un proyecto existente.

    **Invariantes:**
    - Si se actualiza `title`, no puede estar vacío
    - Si se actualiza `description`, no puede estar vacía
    - Si se actualiza `orderIndex`, debe ser único dentro del perfil

    Args:
        project_id: ID del proyecto a actualizar
        project_data: Datos a actualizar (campos opcionales)

    Returns:
        ProjectResponse: Proyecto actualizado

    Raises:
        HTTPException 404: Si el proyecto no existe
        HTTPException 409: Si el nuevo orderIndex ya está en uso
        HTTPException 400: Si los datos no cumplen las invariantes

    TODO: Implementar con UpdateProjectUseCase
    TODO: Validar que orderIndex sea único si se actualiza
    TODO: Requiere autenticación de admin
    """
    for proj in MOCK_PROJECTS:
        if proj.id == project_id:
            return proj

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Proyecto con ID '{project_id}' no encontrado",
    )


@router.delete(
    "/{project_id}",
    response_model=MessageResponse,
    summary="Eliminar proyecto",
    description="Elimina un proyecto del perfil",
)
async def delete_project(project_id: str):
    """
    Elimina un proyecto del perfil.

    Nota: Al eliminar un proyecto, puede ser necesario reordenar
    los orderIndex de los proyectos restantes para evitar huecos.

    Args:
        project_id: ID del proyecto a eliminar

    Returns:
        MessageResponse: Confirmación de eliminación

    Raises:
        HTTPException 404: Si el proyecto no existe

    TODO: Implementar con DeleteProjectUseCase
    TODO: Considerar reordenamiento automático de orderIndex
    TODO: Requiere autenticación de admin
    """
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
    """
    Reordena múltiples proyectos de una sola vez.

    Útil para drag & drop en el panel de administración.

    Args:
        project_orders: Lista de objetos con {id, orderIndex}
        Ejemplo: [
            {"id": "proj_001", "orderIndex": 2},
            {"id": "proj_002", "orderIndex": 1},
            {"id": "proj_003", "orderIndex": 3}
        ]

    Returns:
        List[ProjectResponse]: Proyectos reordenados

    Raises:
        HTTPException 400: Si hay orderIndex duplicados
        HTTPException 404: Si algún project_id no existe

    TODO: Implementar con ReorderProjectsUseCase
    TODO: Validar que todos los orderIndex sean únicos
    TODO: Validar que todos los project_id existan
    TODO: Hacer update en transacción (todo o nada)
    TODO: Requiere autenticación de admin
    """
    return sorted(MOCK_PROJECTS, key=lambda x: x.order_index)
