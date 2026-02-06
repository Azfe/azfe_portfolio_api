from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from app.api.schemas.additional_training_schema import (
    AdditionalTrainingCreate,
    AdditionalTrainingResponse,
    AdditionalTrainingUpdate,
)
from app.api.schemas.common_schema import MessageResponse

router = APIRouter(prefix="/additional-training", tags=["Additional Training"])

# Mock data - Formación adicional del perfil único
MOCK_TRAININGS = [
    AdditionalTrainingResponse(
        id="train_001",
        title="Clean Architecture y Domain-Driven Design en Python",
        provider="Udemy",
        completion_date=datetime(2023, 4, 15),
        duration="40 horas",
        description="Curso avanzado sobre arquitecturas limpias, DDD y principios SOLID aplicados a Python. Incluye implementación práctica de casos de uso, repositorios y mappers.",
        order_index=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    AdditionalTrainingResponse(
        id="train_002",
        title="Advanced React Patterns and Performance",
        provider="Frontend Masters",
        completion_date=datetime(2023, 7, 1),
        duration="30 horas",
        description="Patrones avanzados de React: Custom Hooks, Compound Components, Render Props, Context optimization. Técnicas de optimización de rendimiento.",
        order_index=2,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    AdditionalTrainingResponse(
        id="train_003",
        title="Docker y Kubernetes: De Cero a Experto",
        provider="Platzi",
        completion_date=datetime(2022, 11, 20),
        duration="50 horas",
        description="Containerización con Docker, orquestación con Kubernetes, CI/CD pipelines, y despliegue en producción.",
        order_index=3,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    AdditionalTrainingResponse(
        id="train_004",
        title="MongoDB University: M320 Data Modeling",
        provider="MongoDB University",
        completion_date=datetime(2024, 1, 10),
        duration="20 horas",
        description="Diseño de modelos de datos para MongoDB. Patrones de modelado, optimización de queries y buenas prácticas.",
        order_index=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    AdditionalTrainingResponse(
        id="train_005",
        title="Testing en Python: Pytest y TDD",
        provider="Real Python",
        completion_date=datetime(2023, 9, 15),
        duration="25 horas",
        description="Test-Driven Development con Pytest. Fixtures, mocking, coverage y testing de APIs.",
        order_index=4,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    AdditionalTrainingResponse(
        id="train_006",
        title="Bootcamp Full Stack Development",
        provider="Ironhack",
        completion_date=datetime(2021, 8, 30),
        duration="400 horas",
        description="Bootcamp intensivo de 10 semanas en desarrollo Full Stack. Proyectos reales, metodologías ágiles y preparación para el mercado laboral.",
        order_index=5,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]


@router.get(
    "",
    response_model=list[AdditionalTrainingResponse],
    summary="Listar formación adicional",
    description="Obtiene toda la formación complementaria ordenada por orderIndex",
)
async def get_additional_trainings():
    """
    Lista toda la formación adicional del perfil único del sistema.

    La formación se retorna ordenada por `order_index` ascendente.
    Típicamente, la formación más reciente tiene order_index menor.

    Returns:
        List[AdditionalTrainingResponse]: Lista de formación adicional ordenada

    Relación:
    - Toda la formación pertenece al Profile único del sistema

    TODO: Implementar con GetAdditionalTrainingsUseCase
    TODO: Ordenar por order_index ASC (más reciente primero)
    """
    return sorted(MOCK_TRAININGS, key=lambda x: x.order_index)


@router.get(
    "/{training_id}",
    response_model=AdditionalTrainingResponse,
    summary="Obtener formación adicional",
    description="Obtiene una formación adicional específica por ID",
)
async def get_additional_training(training_id: str):
    """
    Obtiene una formación adicional por su ID.

    Args:
        training_id: ID único de la formación

    Returns:
        AdditionalTrainingResponse: Formación encontrada

    Raises:
        HTTPException 404: Si la formación no existe

    TODO: Implementar con GetAdditionalTrainingUseCase
    """
    for train in MOCK_TRAININGS:
        if train.id == training_id:
            return train

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Formación adicional con ID '{training_id}' no encontrada",
    )


@router.post(
    "",
    response_model=AdditionalTrainingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear formación adicional",
    description="Crea una nueva formación adicional asociada al perfil",
)
async def create_additional_training(_training_data: AdditionalTrainingCreate):
    """
    Crea una nueva formación adicional y la asocia al perfil único del sistema.

    TODO: Implementar con CreateAdditionalTrainingUseCase
    TODO: Requiere autenticación de admin
    """
    return MOCK_TRAININGS[0]


@router.put(
    "/{training_id}",
    response_model=AdditionalTrainingResponse,
    summary="Actualizar formación adicional",
    description="Actualiza una formación adicional existente",
)
async def update_additional_training(
    training_id: str, _training_data: AdditionalTrainingUpdate
):
    """
    Actualiza una formación adicional existente.

    TODO: Implementar con UpdateAdditionalTrainingUseCase
    TODO: Requiere autenticación de admin
    """
    for train in MOCK_TRAININGS:
        if train.id == training_id:
            return train

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Formación adicional con ID '{training_id}' no encontrada",
    )


@router.delete(
    "/{training_id}",
    response_model=MessageResponse,
    summary="Eliminar formación adicional",
    description="Elimina una formación adicional del perfil",
)
async def delete_additional_training(training_id: str):
    """
    Elimina una formación adicional del perfil.

    TODO: Implementar con DeleteAdditionalTrainingUseCase
    TODO: Requiere autenticación de admin
    """
    return MessageResponse(
        success=True,
        message=f"Formación adicional '{training_id}' eliminada correctamente",
    )


@router.patch(
    "/reorder",
    response_model=list[AdditionalTrainingResponse],
    summary="Reordenar formación adicional",
    description="Actualiza el orderIndex de múltiples formaciones de una vez",
)
async def reorder_additional_trainings(_training_orders: list[dict]):
    """
    Reordena múltiples formaciones adicionales de una sola vez.

    TODO: Implementar con ReorderAdditionalTrainingsUseCase
    TODO: Requiere autenticación de admin
    """
    return sorted(MOCK_TRAININGS, key=lambda x: x.order_index)
