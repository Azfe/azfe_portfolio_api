from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime, date

from app.api.schemas.education_schema import (
    EducationResponse,
    EducationCreate,
    EducationUpdate
)
from app.api.schemas.common_schema import MessageResponse

router = APIRouter(prefix="/education", tags=["Education"])

# Mock data - Formación académica del perfil único
MOCK_EDUCATION = [
    EducationResponse(
        id="edu_001",
        institution="Universidad Politécnica de Valencia",
        degree="Grado en Ingeniería Informática",
        start_date=date(2015, 9, 1),
        end_date=date(2019, 6, 30),
        description="Especialización en Ingeniería del Software. Proyecto final: Sistema de gestión hospitalaria con arquitectura microservicios. Nota media: 8.5/10",
        order_index=1,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    EducationResponse(
        id="edu_002",
        institution="IES Valencia",
        degree="Ciclo Formativo de Grado Superior en Desarrollo de Aplicaciones Web",
        start_date=date(2013, 9, 1),
        end_date=date(2015, 6, 30),
        description="Formación práctica en desarrollo web. Tecnologías: HTML, CSS, JavaScript, PHP, MySQL",
        order_index=2,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    EducationResponse(
        id="edu_003",
        institution="Universidad de Valencia",
        degree="Máster en Ingeniería del Software",
        start_date=date(2023, 9, 1),
        end_date=None,  # En curso
        description="Cursando actualmente. Enfoque en arquitecturas de software, microservicios y DevOps",
        order_index=0,  # Orden 0 para mostrar primero (en curso)
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
]


@router.get(
    "",
    response_model=List[EducationResponse],
    summary="Listar formación académica",
    description="Obtiene toda la formación académica ordenada por orderIndex"
)
async def get_education():
    """
    Lista toda la formación académica del perfil único del sistema.
    
    La formación se retorna ordenada por `order_index` ascendente.
    Típicamente, la formación más reciente o en curso tiene order_index menor.
    
    Returns:
        List[EducationResponse]: Lista de formación académica ordenada
    
    Relación:
    - Toda la formación pertenece al Profile único del sistema
    
    TODO: Implementar con GetEducationListUseCase
    TODO: Ordenar por order_index ASC (en curso primero, luego más reciente)
    """
    return sorted(MOCK_EDUCATION, key=lambda x: x.order_index)


@router.get(
    "/{education_id}",
    response_model=EducationResponse,
    summary="Obtener formación académica",
    description="Obtiene una formación académica específica por ID"
)
async def get_education_by_id(education_id: str):
    """
    Obtiene una formación académica por su ID.
    
    Args:
        education_id: ID único de la formación
    
    Returns:
        EducationResponse: Formación encontrada
    
    Raises:
        HTTPException 404: Si la formación no existe
    
    TODO: Implementar con GetEducationUseCase
    """
    for edu in MOCK_EDUCATION:
        if edu.id == education_id:
            return edu
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Formación académica con ID '{education_id}' no encontrada"
    )


@router.post(
    "",
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear formación académica",
    description="Crea una nueva formación académica asociada al perfil"
)
async def create_education(education_data: EducationCreate):
    """
    Crea una nueva formación académica y la asocia al perfil único del sistema.
    
    **Invariantes que se validan automáticamente:**
    - `institution` no puede estar vacía (min_length=1)
    - `degree` no puede estar vacío (min_length=1)
    - `startDate` es obligatoria
    - Si `endDate` existe, debe ser posterior a `startDate` (validador Pydantic)
    
    Args:
        education_data: Datos de la formación a crear
    
    Returns:
        EducationResponse: Formación creada
    
    Raises:
        HTTPException 422: Si endDate <= startDate
        HTTPException 400: Si los datos no cumplen las invariantes
    
    TODO: Implementar con CreateEducationUseCase
    TODO: Requiere autenticación de admin
    """
    return MOCK_EDUCATION[0]


@router.put(
    "/{education_id}",
    response_model=EducationResponse,
    summary="Actualizar formación académica",
    description="Actualiza una formación académica existente"
)
async def update_education(
    education_id: str,
    education_data: EducationUpdate
):
    """
    Actualiza una formación académica existente.
    
    **Invariantes:**
    - Si se actualiza `institution`, no puede estar vacía
    - Si se actualiza `degree`, no puede estar vacío
    - Si se actualiza `endDate`, debe ser posterior a `startDate`
    
    Args:
        education_id: ID de la formación a actualizar
        education_data: Datos a actualizar (campos opcionales)
    
    Returns:
        EducationResponse: Formación actualizada
    
    Raises:
        HTTPException 404: Si la formación no existe
        HTTPException 422: Si endDate <= startDate
        HTTPException 400: Si los datos no cumplen las invariantes
    
    TODO: Implementar con UpdateEducationUseCase
    TODO: Validar fechas si se actualizan ambas o una de ellas
    TODO: Requiere autenticación de admin
    """
    for edu in MOCK_EDUCATION:
        if edu.id == education_id:
            return edu
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Formación académica con ID '{education_id}' no encontrada"
    )


@router.delete(
    "/{education_id}",
    response_model=MessageResponse,
    summary="Eliminar formación académica",
    description="Elimina una formación académica del perfil"
)
async def delete_education(education_id: str):
    """
    Elimina una formación académica del perfil.
    
    Nota: Al eliminar una formación, puede ser necesario reordenar
    los orderIndex de la formación restante para mantener la coherencia.
    
    Args:
        education_id: ID de la formación a eliminar
    
    Returns:
        MessageResponse: Confirmación de eliminación
    
    Raises:
        HTTPException 404: Si la formación no existe
    
    TODO: Implementar con DeleteEducationUseCase
    TODO: Considerar reordenamiento automático de orderIndex
    TODO: Requiere autenticación de admin
    """
    return MessageResponse(
        success=True,
        message=f"Formación académica '{education_id}' eliminada correctamente"
    )


@router.patch(
    "/reorder",
    response_model=List[EducationResponse],
    summary="Reordenar formación académica",
    description="Actualiza el orderIndex de múltiples formaciones de una vez"
)
async def reorder_education(education_orders: List[dict]):
    """
    Reordena múltiples formaciones académicas de una sola vez.
    
    Útil para drag & drop en el panel de administración.
    
    Args:
        education_orders: Lista de objetos con {id, orderIndex}
        Ejemplo: [
            {"id": "edu_001", "orderIndex": 2},
            {"id": "edu_002", "orderIndex": 1},
            {"id": "edu_003", "orderIndex": 0}
        ]
    
    Returns:
        List[EducationResponse]: Formaciones reordenadas
    
    Raises:
        HTTPException 400: Si hay orderIndex duplicados
        HTTPException 404: Si algún education_id no existe
    
    TODO: Implementar con ReorderEducationUseCase
    TODO: Validar que todos los orderIndex sean únicos
    TODO: Validar que todos los education_id existan
    TODO: Hacer update en transacción (todo o nada)
    TODO: Requiere autenticación de admin
    """
    return sorted(MOCK_EDUCATION, key=lambda x: x.order_index)