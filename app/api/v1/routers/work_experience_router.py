from datetime import date, datetime

from fastapi import APIRouter, HTTPException, status

from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.work_experience_schema import (
    WorkExperienceCreate,
    WorkExperienceResponse,
    WorkExperienceUpdate,
)

router = APIRouter(prefix="/work-experiences", tags=["Work Experience"])

# Mock data - Experiencias laborales del perfil único
MOCK_EXPERIENCES = [
    WorkExperienceResponse(
        id="exp_001",
        role="Senior Full Stack Developer",
        company="Tech Solutions S.L.",
        location="Valencia, España",
        start_date=date(2021, 3, 1),
        end_date=None,  # Actualmente trabajando
        description="Desarrollo de aplicaciones web escalables usando FastAPI y React. Implementación de arquitectura Clean Architecture en proyectos empresariales. Liderazgo técnico de equipo de 4 desarrolladores junior. Responsable de code reviews y definición de estándares de código.",
        technologies=[
            "Python",
            "FastAPI",
            "React",
            "MongoDB",
            "Docker",
            "AWS",
            "TypeScript",
        ],
        order_index=0,  # Empleo actual, se muestra primero
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    WorkExperienceResponse(
        id="exp_002",
        role="Full Stack Developer",
        company="StartupXYZ - Fintech",
        location="Remoto",
        start_date=date(2019, 6, 1),
        end_date=date(2021, 2, 28),
        description="Desarrollo del MVP de una plataforma fintech desde cero. Implementación de sistema de pagos con Stripe. Desarrollo de API REST y dashboard administrativo. Trabajo en equipo ágil con sprints de 2 semanas.",
        technologies=["Node.js", "Vue.js", "PostgreSQL", "Stripe", "Docker", "Redis"],
        order_index=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    WorkExperienceResponse(
        id="exp_003",
        role="Backend Developer",
        company="Digital Agency Corp",
        location="Barcelona, España",
        start_date=date(2018, 9, 1),
        end_date=date(2019, 5, 31),
        description="Desarrollo de APIs RESTful para aplicaciones móviles y web. Mantenimiento de bases de datos MySQL y optimización de queries. Integración con servicios de terceros (Google Maps, SendGrid, Twilio).",
        technologies=["PHP", "Laravel", "MySQL", "Redis", "jQuery"],
        order_index=2,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    WorkExperienceResponse(
        id="exp_004",
        role="Junior Web Developer",
        company="WebStudio",
        location="Valencia, España",
        start_date=date(2017, 3, 15),
        end_date=date(2018, 8, 31),
        description="Primer empleo como desarrollador. Desarrollo de sitios web corporativos con WordPress. Maquetación HTML/CSS responsive. Mantenimiento de sitios existentes y corrección de bugs.",
        technologies=["HTML", "CSS", "JavaScript", "WordPress", "PHP", "MySQL"],
        order_index=3,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]


@router.get(
    "",
    response_model=list[WorkExperienceResponse],
    summary="Listar experiencias laborales",
    description="Obtiene todas las experiencias laborales ordenadas por orderIndex",
)
async def get_work_experiences():
    """
    Lista todas las experiencias laborales del perfil único del sistema.

    Las experiencias se retornan ordenadas por `order_index` ascendente.
    Típicamente, el empleo actual o más reciente tiene order_index menor.

    Returns:
        List[WorkExperienceResponse]: Lista de experiencias ordenadas

    Relación:
    - Todas las experiencias pertenecen al Profile único del sistema
    - technologies se relaciona con Skills del perfil

    TODO: Implementar con GetWorkExperiencesUseCase
    TODO: Ordenar por order_index ASC (empleo actual primero, luego cronológico inverso)
    """
    return sorted(MOCK_EXPERIENCES, key=lambda x: x.order_index)


@router.get(
    "/{experience_id}",
    response_model=WorkExperienceResponse,
    summary="Obtener experiencia laboral",
    description="Obtiene una experiencia laboral específica por ID",
)
async def get_work_experience(experience_id: str):
    """
    Obtiene una experiencia laboral por su ID.

    Args:
        experience_id: ID único de la experiencia

    Returns:
        WorkExperienceResponse: Experiencia encontrada

    Raises:
        HTTPException 404: Si la experiencia no existe

    TODO: Implementar con GetWorkExperienceUseCase
    """
    for exp in MOCK_EXPERIENCES:
        if exp.id == experience_id:
            return exp

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Experiencia laboral con ID '{experience_id}' no encontrada",
    )


@router.post(
    "",
    response_model=WorkExperienceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear experiencia laboral",
    description="Crea una nueva experiencia laboral asociada al perfil",
)
async def create_work_experience(_experience_data: WorkExperienceCreate):
    """
    Crea una nueva experiencia laboral y la asocia al perfil único del sistema.

    **Invariantes que se validan automáticamente:**
    - `role` no puede estar vacío (min_length=1)
    - `company` no puede estar vacía (min_length=1)
    - `startDate` es obligatoria
    - Si `endDate` existe, debe ser posterior a `startDate` (validador Pydantic)
    - `orderIndex` debe ser único dentro del perfil

    Args:
        experience_data: Datos de la experiencia a crear

    Returns:
        WorkExperienceResponse: Experiencia creada

    Raises:
        HTTPException 422: Si endDate <= startDate
        HTTPException 409: Si orderIndex ya está en uso
        HTTPException 400: Si los datos no cumplen las invariantes

    Notas sobre technologies:
    - Las tecnologías listadas deberían idealmente existir como Skills en el perfil
    - Esto ayuda a demostrar dónde se usaron las habilidades

    TODO: Implementar con CreateWorkExperienceUseCase
    TODO: Validar que orderIndex sea único dentro del perfil
    TODO: Considerar auto-incrementar orderIndex si no se proporciona
    TODO: Requiere autenticación de admin
    """
    # Mock: Validar orderIndex único
    # if any(exp.order_index == experience_data.order_index for exp in MOCK_EXPERIENCES):
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail=f"Ya existe una experiencia con orderIndex {experience_data.order_index}"
    #     )

    return MOCK_EXPERIENCES[0]


@router.put(
    "/{experience_id}",
    response_model=WorkExperienceResponse,
    summary="Actualizar experiencia laboral",
    description="Actualiza una experiencia laboral existente",
)
async def update_work_experience(
    experience_id: str, _experience_data: WorkExperienceUpdate
):
    """
    Actualiza una experiencia laboral existente.

    **Invariantes:**
    - Si se actualiza `role`, no puede estar vacío
    - Si se actualiza `company`, no puede estar vacía
    - Si se actualiza `endDate`, debe ser posterior a `startDate`
    - Si se actualiza `orderIndex`, debe ser único dentro del perfil

    Args:
        experience_id: ID de la experiencia a actualizar
        experience_data: Datos a actualizar (campos opcionales)

    Returns:
        WorkExperienceResponse: Experiencia actualizada

    Raises:
        HTTPException 404: Si la experiencia no existe
        HTTPException 422: Si endDate <= startDate
        HTTPException 409: Si el nuevo orderIndex ya está en uso
        HTTPException 400: Si los datos no cumplen las invariantes

    Casos de uso comunes:
    - Actualizar endDate cuando dejas un empleo (de None a fecha específica)
    - Actualizar description para añadir nuevos logros
    - Actualizar technologies si aprendes nuevas tecnologías en el trabajo

    TODO: Implementar con UpdateWorkExperienceUseCase
    TODO: Validar fechas si se actualizan
    TODO: Validar que orderIndex sea único si se actualiza
    TODO: Requiere autenticación de admin
    """
    for exp in MOCK_EXPERIENCES:
        if exp.id == experience_id:
            # Mock: Validar orderIndex único si se actualiza
            # if experience_data.order_index is not None:
            #     if any(e.order_index == experience_data.order_index and e.id != experience_id
            #            for e in MOCK_EXPERIENCES):
            #         raise HTTPException(
            #             status_code=status.HTTP_409_CONFLICT,
            #             detail=f"Ya existe otra experiencia con orderIndex {experience_data.order_index}"
            #         )
            return exp

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Experiencia laboral con ID '{experience_id}' no encontrada",
    )


@router.delete(
    "/{experience_id}",
    response_model=MessageResponse,
    summary="Eliminar experiencia laboral",
    description="Elimina una experiencia laboral del perfil",
)
async def delete_work_experience(experience_id: str):
    """
    Elimina una experiencia laboral del perfil.

    Nota: Al eliminar una experiencia, puede ser necesario reordenar
    los orderIndex de las experiencias restantes para mantener la coherencia.

    Args:
        experience_id: ID de la experiencia a eliminar

    Returns:
        MessageResponse: Confirmación de eliminación

    Raises:
        HTTPException 404: Si la experiencia no existe

    TODO: Implementar con DeleteWorkExperienceUseCase
    TODO: Considerar reordenamiento automático de orderIndex
    TODO: Requiere autenticación de admin
    """
    return MessageResponse(
        success=True,
        message=f"Experiencia laboral '{experience_id}' eliminada correctamente",
    )


@router.patch(
    "/reorder",
    response_model=list[WorkExperienceResponse],
    summary="Reordenar experiencias laborales",
    description="Actualiza el orderIndex de múltiples experiencias de una vez",
)
async def reorder_work_experiences(_experience_orders: list[dict]):
    """
    Reordena múltiples experiencias laborales de una sola vez.

    Útil para drag & drop en el panel de administración.

    Args:
        experience_orders: Lista de objetos con {id, orderIndex}
        Ejemplo: [
            {"id": "exp_001", "orderIndex": 0},
            {"id": "exp_002", "orderIndex": 1},
            {"id": "exp_003", "orderIndex": 2}
        ]

    Returns:
        List[WorkExperienceResponse]: Experiencias reordenadas

    Raises:
        HTTPException 400: Si hay orderIndex duplicados
        HTTPException 404: Si algún experience_id no existe

    TODO: Implementar con ReorderWorkExperiencesUseCase
    TODO: Validar que todos los orderIndex sean únicos
    TODO: Validar que todos los experience_id existan
    TODO: Hacer update en transacción (todo o nada)
    TODO: Requiere autenticación de admin
    """
    return sorted(MOCK_EXPERIENCES, key=lambda x: x.order_index)


@router.get(
    "/current/active",
    response_model=list[WorkExperienceResponse],
    summary="Obtener empleos actuales",
    description="Obtiene experiencias laborales donde aún se trabaja (endDate = None)",
)
async def get_current_work_experiences():
    """
    Lista experiencias laborales actuales (sin endDate).

    Útil para mostrar el "trabajo actual" en el perfil.

    Returns:
        List[WorkExperienceResponse]: Experiencias sin endDate

    Nota:
    - Normalmente debería haber solo 1, pero el sistema permite múltiples
      (por ejemplo, si se trabaja part-time en varios lugares)

    TODO: Implementar con GetCurrentWorkExperiencesUseCase
    """
    current = [exp for exp in MOCK_EXPERIENCES if exp.end_date is None]
    return sorted(current, key=lambda x: x.order_index)


@router.get(
    "/by-company/{company}",
    response_model=list[WorkExperienceResponse],
    summary="Filtrar experiencias por empresa",
    description="Obtiene experiencias laborales de una empresa específica",
)
async def get_experiences_by_company(company: str):
    """
    Filtra experiencias laborales por empresa.

    Útil si trabajaste en la misma empresa en diferentes períodos o roles.

    Args:
        company: Nombre de la empresa (búsqueda case-insensitive)

    Returns:
        List[WorkExperienceResponse]: Experiencias en esa empresa

    TODO: Implementar con GetExperiencesByCompanyUseCase
    TODO: Hacer búsqueda case-insensitive y parcial (contains)
    """
    company_lower = company.lower()
    filtered = [exp for exp in MOCK_EXPERIENCES if company_lower in exp.company.lower()]
    return sorted(filtered, key=lambda x: x.start_date, reverse=True)


@router.get(
    "/by-technology/{technology}",
    response_model=list[WorkExperienceResponse],
    summary="Filtrar experiencias por tecnología",
    description="Obtiene experiencias donde se usó una tecnología específica",
)
async def get_experiences_by_technology(technology: str):
    """
    Filtra experiencias laborales por tecnología usada.

    Útil para demostrar experiencia práctica con una tecnología específica.

    Args:
        technology: Nombre de la tecnología (case-insensitive)

    Returns:
        List[WorkExperienceResponse]: Experiencias que usaron esa tecnología

    Relación con Skills:
    - Este endpoint ayuda a vincular Skills con experiencia laboral real
    - Muestra dónde y cuándo se aplicó una habilidad

    TODO: Implementar con GetExperiencesByTechnologyUseCase
    TODO: Hacer búsqueda case-insensitive
    """
    tech_lower = technology.lower()
    filtered = [
        exp
        for exp in MOCK_EXPERIENCES
        if any(tech.lower() == tech_lower for tech in exp.technologies)
    ]
    return sorted(filtered, key=lambda x: x.order_index)
