from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime, date

from app.api.schemas.additional_training_schema import (
    AdditionalTrainingResponse,
    AdditionalTrainingCreate,
    AdditionalTrainingUpdate
)
from app.api.schemas.common_schema import MessageResponse

router = APIRouter(prefix="/additional-training", tags=["Additional Training"])

# Mock data - Formación adicional del perfil único
MOCK_TRAININGS = [
    AdditionalTrainingResponse(
        id="train_001",
        title="Clean Architecture y Domain-Driven Design en Python",
        institution="Udemy",
        end_date=date(2023, 4, 15),
        duration_hours=40,
        description="Curso avanzado sobre arquitecturas limpias, DDD y principios SOLID aplicados a Python. Incluye implementación práctica de casos de uso, repositorios y mappers.",
        location="Online",
        technologies=["Python", "FastAPI", "Design Patterns", "SOLID", "DDD"],
        order_index=1,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    AdditionalTrainingResponse(
        id="train_002",
        title="Advanced React Patterns and Performance",
        institution="Frontend Masters",
        end_date=date(2023, 7, 1),
        duration_hours=30,
        description="Patrones avanzados de React: Custom Hooks, Compound Components, Render Props, Context optimization. Técnicas de optimización de rendimiento.",
        location="Online",
        technologies=["React", "TypeScript", "JavaScript", "Performance Optimization"],
        order_index=2,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    AdditionalTrainingResponse(
        id="train_003",
        title="Docker y Kubernetes: De Cero a Experto",
        institution="Platzi",
        end_date=date(2022, 11, 20),
        duration_hours=50,
        description="Containerización con Docker, orquestación con Kubernetes, CI/CD pipelines, y despliegue en producción.",
        location="Online",
        technologies=["Docker", "Kubernetes", "CI/CD", "DevOps"],
        order_index=3,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    AdditionalTrainingResponse(
        id="train_004",
        title="MongoDB University: M320 Data Modeling",
        institution="MongoDB University",
        end_date=date(2024, 1, 10),
        duration_hours=20,
        description="Diseño de modelos de datos para MongoDB. Patrones de modelado, optimización de queries y buenas prácticas.",
        location="Online",
        technologies=["MongoDB", "NoSQL", "Database Design"],
        order_index=0,  # Más reciente
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    AdditionalTrainingResponse(
        id="train_005",
        title="Testing en Python: Pytest y TDD",
        institution="Real Python",
        end_date=date(2023, 9, 15),
        duration_hours=25,
        description="Test-Driven Development con Pytest. Fixtures, mocking, coverage y testing de APIs.",
        location="Online",
        technologies=["Python", "Pytest", "TDD", "Testing"],
        order_index=4,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    AdditionalTrainingResponse(
        id="train_006",
        title="Bootcamp Full Stack Development",
        institution="Ironhack",
        end_date=date(2021, 8, 30),
        duration_hours=400,
        description="Bootcamp intensivo de 10 semanas en desarrollo Full Stack. Proyectos reales, metodologías ágiles y preparación para el mercado laboral.",
        location="Barcelona, España",
        technologies=["JavaScript", "Node.js", "React", "MongoDB", "Express"],
        order_index=5,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
]


@router.get(
    "",
    response_model=List[AdditionalTrainingResponse],
    summary="Listar formación adicional",
    description="Obtiene toda la formación complementaria ordenada por orderIndex"
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
    - technologies se relaciona con Skills del perfil
    
    TODO: Implementar con GetAdditionalTrainingsUseCase
    TODO: Ordenar por order_index ASC (más reciente primero)
    TODO: Considerar ordenar también por date DESC como criterio secundario
    """
    return sorted(MOCK_TRAININGS, key=lambda x: x.order_index)


@router.get(
    "/{training_id}",
    response_model=AdditionalTrainingResponse,
    summary="Obtener formación adicional",
    description="Obtiene una formación adicional específica por ID"
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
        detail=f"Formación adicional con ID '{training_id}' no encontrada"
    )


@router.post(
    "",
    response_model=AdditionalTrainingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear formación adicional",
    description="Crea una nueva formación adicional asociada al perfil"
)
async def create_additional_training(training_data: AdditionalTrainingCreate):
    """
    Crea una nueva formación adicional y la asocia al perfil único del sistema.
    
    **Invariantes que se validan automáticamente:**
    - `title` no puede estar vacío (min_length=1)
    - `institution` no puede estar vacía (min_length=1)
    - `date` es obligatoria
    - `duration_hours` si se proporciona, debe ser >= 1
    
    Args:
        training_data: Datos de la formación a crear
    
    Returns:
        AdditionalTrainingResponse: Formación creada
    
    Raises:
        HTTPException 422: Si los datos no cumplen las invariantes
    
    Nota sobre technologies:
    - Las tecnologías listadas deberían idealmente existir como Skills en el perfil
    - Esto ayuda a vincular la formación con las habilidades adquiridas
    
    TODO: Implementar con CreateAdditionalTrainingUseCase
    TODO: Considerar auto-incrementar orderIndex si no se proporciona
    TODO: Validar que las technologies existan como Skills (opcional)
    TODO: Requiere autenticación de admin
    """
    return MOCK_TRAININGS[0]


@router.put(
    "/{training_id}",
    response_model=AdditionalTrainingResponse,
    summary="Actualizar formación adicional",
    description="Actualiza una formación adicional existente"
)
async def update_additional_training(
    training_id: str,
    training_data: AdditionalTrainingUpdate
):
    """
    Actualiza una formación adicional existente.
    
    **Invariantes:**
    - Si se actualiza `title`, no puede estar vacío
    - Si se actualiza `institution`, no puede estar vacía
    - Si se actualiza `duration_hours`, debe ser >= 1
    
    Args:
        training_id: ID de la formación a actualizar
        training_data: Datos a actualizar (campos opcionales)
    
    Returns:
        AdditionalTrainingResponse: Formación actualizada
    
    Raises:
        HTTPException 404: Si la formación no existe
        HTTPException 422: Si los datos no cumplen las invariantes
    
    TODO: Implementar con UpdateAdditionalTrainingUseCase
    TODO: Requiere autenticación de admin
    """
    for train in MOCK_TRAININGS:
        if train.id == training_id:
            return train
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Formación adicional con ID '{training_id}' no encontrada"
    )


@router.delete(
    "/{training_id}",
    response_model=MessageResponse,
    summary="Eliminar formación adicional",
    description="Elimina una formación adicional del perfil"
)
async def delete_additional_training(training_id: str):
    """
    Elimina una formación adicional del perfil.
    
    Nota: Al eliminar una formación, puede ser necesario reordenar
    los orderIndex de la formación restante para mantener la coherencia.
    
    Args:
        training_id: ID de la formación a eliminar
    
    Returns:
        MessageResponse: Confirmación de eliminación
    
    Raises:
        HTTPException 404: Si la formación no existe
    
    TODO: Implementar con DeleteAdditionalTrainingUseCase
    TODO: Considerar reordenamiento automático de orderIndex
    TODO: Requiere autenticación de admin
    """
    return MessageResponse(
        success=True,
        message=f"Formación adicional '{training_id}' eliminada correctamente"
    )


@router.patch(
    "/reorder",
    response_model=List[AdditionalTrainingResponse],
    summary="Reordenar formación adicional",
    description="Actualiza el orderIndex de múltiples formaciones de una vez"
)
async def reorder_additional_trainings(training_orders: List[dict]):
    """
    Reordena múltiples formaciones adicionales de una sola vez.
    
    Útil para drag & drop en el panel de administración.
    
    Args:
        training_orders: Lista de objetos con {id, orderIndex}
        Ejemplo: [
            {"id": "train_001", "orderIndex": 2},
            {"id": "train_002", "orderIndex": 1},
            {"id": "train_003", "orderIndex": 0}
        ]
    
    Returns:
        List[AdditionalTrainingResponse]: Formaciones reordenadas
    
    Raises:
        HTTPException 400: Si hay orderIndex duplicados
        HTTPException 404: Si algún training_id no existe
    
    TODO: Implementar con ReorderAdditionalTrainingsUseCase
    TODO: Validar que todos los orderIndex sean únicos
    TODO: Validar que todos los training_id existan
    TODO: Hacer update en transacción (todo o nada)
    TODO: Requiere autenticación de admin
    """
    return sorted(MOCK_TRAININGS, key=lambda x: x.order_index)


@router.get(
    "/by-technology/{technology}",
    response_model=List[AdditionalTrainingResponse],
    summary="Filtrar formación por tecnología",
    description="Obtiene formaciones que incluyan una tecnología específica"
)
async def get_trainings_by_technology(technology: str):
    """
    Filtra formaciones adicionales por tecnología aprendida.
    
    Útil para mostrar qué cursos/formaciones se hicieron para aprender
    una tecnología específica.
    
    Args:
        technology: Nombre de la tecnología (case-insensitive)
    
    Returns:
        List[AdditionalTrainingResponse]: Formaciones que incluyen esa tecnología
    
    Relación con Skills:
    - Este endpoint ayuda a vincular formación con habilidades adquiridas
    - Las tecnologías deberían coincidir con Skills del perfil
    
    TODO: Implementar con GetTrainingsByTechnologyUseCase
    TODO: Hacer búsqueda case-insensitive
    TODO: Considerar búsqueda parcial (contains)
    """
    tech_lower = technology.lower()
    filtered = [
        t for t in MOCK_TRAININGS 
        if any(tech.lower() == tech_lower for tech in t.technologies)
    ]
    return sorted(filtered, key=lambda x: x.order_index)