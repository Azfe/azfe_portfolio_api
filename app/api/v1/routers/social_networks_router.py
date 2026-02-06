from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.social_networks_schema import (
    SocialNetworkCreate,
    SocialNetworkResponse,
    SocialNetworkUpdate,
)

router = APIRouter(prefix="/social-networks", tags=["Social Networks"])

# Mock data - Redes sociales del perfil único
MOCK_SOCIAL_NETWORKS = [
    SocialNetworkResponse(
        id="social_001",
        platform="github",
        url="https://github.com/juanperez",
        username="juanperez",
        order_index=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    SocialNetworkResponse(
        id="social_002",
        platform="linkedin",
        url="https://www.linkedin.com/in/juanperez",
        username="juanperez",
        order_index=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    SocialNetworkResponse(
        id="social_003",
        platform="twitter",
        url="https://twitter.com/juanperez",
        username="juanperez",
        order_index=2,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    SocialNetworkResponse(
        id="social_004",
        platform="stackoverflow",
        url="https://stackoverflow.com/users/12345/juanperez",
        username="juanperez",
        order_index=3,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    SocialNetworkResponse(
        id="social_005",
        platform="dev_to",
        url="https://dev.to/juanperez",
        username="juanperez",
        order_index=4,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    SocialNetworkResponse(
        id="social_006",
        platform="medium",
        url="https://medium.com/@juanperez",
        username="juanperez",
        order_index=5,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]


@router.get(
    "",
    response_model=list[SocialNetworkResponse],
    summary="Listar redes sociales",
    description="Obtiene todas las redes sociales ordenadas por orderIndex",
)
async def get_social_networks():
    """
    Lista todas las redes sociales del perfil único del sistema.

    Las redes sociales se retornan ordenadas por `order_index` ascendente.
    Típicamente, las más importantes (GitHub, LinkedIn) tienen índices menores.

    Returns:
        List[SocialNetworkResponse]: Lista de redes sociales ordenadas

    Relación:
    - Todas las redes sociales pertenecen al Profile único del sistema

    TODO: Implementar con GetSocialNetworksUseCase
    TODO: Ordenar por order_index ASC
    """
    return sorted(MOCK_SOCIAL_NETWORKS, key=lambda x: x.order_index)


@router.get(
    "/{social_id}",
    response_model=SocialNetworkResponse,
    summary="Obtener red social",
    description="Obtiene una red social específica por ID",
)
async def get_social_network(social_id: str):
    """
    Obtiene una red social por su ID.

    Args:
        social_id: ID único de la red social

    Returns:
        SocialNetworkResponse: Red social encontrada

    Raises:
        HTTPException 404: Si la red social no existe

    TODO: Implementar con GetSocialNetworkUseCase
    """
    for social in MOCK_SOCIAL_NETWORKS:
        if social.id == social_id:
            return social

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Red social con ID '{social_id}' no encontrada",
    )


@router.post(
    "",
    response_model=SocialNetworkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear red social",
    description="Crea una nueva red social asociada al perfil",
)
async def create_social_network(_social_data: SocialNetworkCreate):
    """
    Crea una nueva red social y la asocia al perfil único del sistema.

    **Invariantes que se validan automáticamente:**
    - `platform` no puede estar vacío
    - `url` debe ser una URL válida
    - `orderIndex` debe ser único dentro del perfil

    Args:
        social_data: Datos de la red social a crear

    Returns:
        SocialNetworkResponse: Red social creada

    Raises:
        HTTPException 422: Si url no es válida
        HTTPException 409: Si orderIndex ya está en uso
        HTTPException 400: Si los datos no cumplen las invariantes

    TODO: Implementar con CreateSocialNetworkUseCase
    TODO: Validar que orderIndex sea único dentro del perfil
    TODO: Considerar auto-incrementar orderIndex si no se proporciona
    TODO: Requiere autenticación de admin
    """
    return MOCK_SOCIAL_NETWORKS[0]


@router.put(
    "/{social_id}",
    response_model=SocialNetworkResponse,
    summary="Actualizar red social",
    description="Actualiza una red social existente",
)
async def update_social_network(social_id: str, _social_data: SocialNetworkUpdate):
    """
    Actualiza una red social existente.

    **Invariantes:**
    - Si se actualiza `platform`, no puede estar vacío
    - Si se actualiza `url`, debe ser válida
    - Si se actualiza `orderIndex`, debe ser único dentro del perfil

    Args:
        social_id: ID de la red social a actualizar
        social_data: Datos a actualizar (campos opcionales)

    Returns:
        SocialNetworkResponse: Red social actualizada

    Raises:
        HTTPException 404: Si la red social no existe
        HTTPException 422: Si url no es válida
        HTTPException 409: Si el nuevo orderIndex ya está en uso

    TODO: Implementar con UpdateSocialNetworkUseCase
    TODO: Validar que orderIndex sea único si se actualiza
    TODO: Requiere autenticación de admin
    """
    for social in MOCK_SOCIAL_NETWORKS:
        if social.id == social_id:
            return social

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Red social con ID '{social_id}' no encontrada",
    )


@router.delete(
    "/{social_id}",
    response_model=MessageResponse,
    summary="Eliminar red social",
    description="Elimina una red social del perfil",
)
async def delete_social_network(social_id: str):
    """
    Elimina una red social del perfil.

    Nota: Al eliminar una red social, puede ser necesario reordenar
    los orderIndex de las redes restantes para mantener la coherencia.

    Args:
        social_id: ID de la red social a eliminar

    Returns:
        MessageResponse: Confirmación de eliminación

    Raises:
        HTTPException 404: Si la red social no existe

    TODO: Implementar con DeleteSocialNetworkUseCase
    TODO: Considerar reordenamiento automático de orderIndex
    TODO: Requiere autenticación de admin
    """
    return MessageResponse(
        success=True, message=f"Red social '{social_id}' eliminada correctamente"
    )


@router.patch(
    "/reorder",
    response_model=list[SocialNetworkResponse],
    summary="Reordenar redes sociales",
    description="Actualiza el orderIndex de múltiples redes sociales de una vez",
)
async def reorder_social_networks(_social_orders: list[dict]):
    """
    Reordena múltiples redes sociales de una sola vez.

    Útil para drag & drop en el panel de administración.

    Args:
        social_orders: Lista de objetos con {id, orderIndex}
        Ejemplo: [
            {"id": "social_001", "orderIndex": 0},
            {"id": "social_002", "orderIndex": 1},
            {"id": "social_003", "orderIndex": 2}
        ]

    Returns:
        List[SocialNetworkResponse]: Redes sociales reordenadas

    Raises:
        HTTPException 400: Si hay orderIndex duplicados
        HTTPException 404: Si algún social_id no existe

    TODO: Implementar con ReorderSocialNetworksUseCase
    TODO: Validar que todos los orderIndex sean únicos
    TODO: Validar que todos los social_id existan
    TODO: Hacer update en transacción (todo o nada)
    TODO: Requiere autenticación de admin
    """
    return sorted(MOCK_SOCIAL_NETWORKS, key=lambda x: x.order_index)


@router.get(
    "/by-platform/{platform}",
    response_model=list[SocialNetworkResponse],
    summary="Filtrar por plataforma",
    description="Obtiene redes sociales de una plataforma específica",
)
async def get_social_networks_by_platform(platform: str):
    """
    Filtra redes sociales por plataforma.

    Útil si tienes múltiples perfiles en la misma plataforma
    (ej: GitHub personal y GitHub de empresa).

    Args:
        platform: Nombre de la plataforma

    Returns:
        List[SocialNetworkResponse]: Redes sociales de esa plataforma

    TODO: Implementar con GetSocialNetworksByPlatformUseCase
    """
    filtered = [s for s in MOCK_SOCIAL_NETWORKS if s.platform == platform]
    return sorted(filtered, key=lambda x: x.order_index)


@router.get(
    "/grouped/by-platform",
    response_model=dict,
    summary="Agrupar por plataforma",
    description="Obtiene redes sociales agrupadas por plataforma",
)
async def get_social_networks_grouped():
    """
    Agrupa redes sociales por plataforma.

    Útil para mostrar secciones organizadas en el portfolio.

    Returns:
        dict: Diccionario con plataformas como keys
        Ejemplo:
        {
            "github": [social1, social2],
            "linkedin": [social3],
            "twitter": [social4]
        }

    TODO: Implementar con GetSocialNetworksGroupedUseCase
    TODO: Ordenar redes dentro de cada plataforma por order_index
    """
    grouped: dict[str, list[SocialNetworkResponse]] = {}
    for social in MOCK_SOCIAL_NETWORKS:
        if social.platform not in grouped:
            grouped[social.platform] = []
        grouped[social.platform].append(social)

    # Ordenar dentro de cada grupo por order_index
    for platform in grouped:
        grouped[platform] = sorted(grouped[platform], key=lambda x: x.order_index)

    return grouped
