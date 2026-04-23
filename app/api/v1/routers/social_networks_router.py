from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_add_social_network_use_case,
    get_delete_social_network_use_case,
    get_edit_social_network_use_case,
    get_list_social_networks_use_case,
    get_social_network_repository,
)
from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.social_networks_schema import (
    SocialNetworkCreate,
    SocialNetworkResponse,
    SocialNetworkUpdate,
)
from app.application.dto import (
    AddSocialNetworkRequest,
    DeleteSocialNetworkRequest,
    EditSocialNetworkRequest,
    ListSocialNetworksRequest,
    SocialNetworkResponse as SocialNetworkDTO,
)
from app.application.use_cases.social_network import (
    AddSocialNetworkUseCase,
    DeleteSocialNetworkUseCase,
    EditSocialNetworkUseCase,
    ListSocialNetworksUseCase,
)
from app.infrastructure.repositories import SocialNetworkRepository
from app.shared.shared_exceptions import NotFoundException

router = APIRouter(prefix="/social-networks", tags=["Social Networks"])

PROFILE_ID = "default_profile"


@router.get(
    "",
    response_model=list[SocialNetworkResponse],
    summary="Listar redes sociales",
    description="Obtiene todas las redes sociales ordenadas por orderIndex",
)
async def get_social_networks(
    use_case: ListSocialNetworksUseCase = Depends(get_list_social_networks_use_case),
):
    result = await use_case.execute(ListSocialNetworksRequest(profile_id=PROFILE_ID))
    return result.social_networks


@router.get(
    "/by-platform/{platform}",
    response_model=list[SocialNetworkResponse],
    summary="Filtrar por plataforma",
    description="Obtiene redes sociales de una plataforma específica",
)
async def get_social_networks_by_platform(
    platform: str,
    use_case: ListSocialNetworksUseCase = Depends(get_list_social_networks_use_case),
):
    result = await use_case.execute(ListSocialNetworksRequest(profile_id=PROFILE_ID))
    return [s for s in result.social_networks if s.platform == platform]


@router.get(
    "/grouped/by-platform",
    response_model=dict,
    summary="Agrupar por plataforma",
    description="Obtiene redes sociales agrupadas por plataforma",
)
async def get_social_networks_grouped(
    use_case: ListSocialNetworksUseCase = Depends(get_list_social_networks_use_case),
):
    result = await use_case.execute(ListSocialNetworksRequest(profile_id=PROFILE_ID))
    grouped: dict[str, list] = {}
    for s in result.social_networks:
        if s.platform not in grouped:
            grouped[s.platform] = []
        grouped[s.platform].append(s)
    return grouped


@router.get(
    "/{social_id}",
    response_model=SocialNetworkResponse,
    summary="Obtener red social",
    description="Obtiene una red social específica por ID",
)
async def get_social_network(
    social_id: str,
    repo: SocialNetworkRepository = Depends(get_social_network_repository),
):
    entity = await repo.get_by_id(social_id)
    if not entity:
        raise NotFoundException("SocialNetwork", social_id)
    return SocialNetworkDTO.from_entity(entity)


@router.post(
    "",
    response_model=SocialNetworkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear red social",
    description="Crea una nueva red social asociada al perfil",
)
async def create_social_network(
    social_data: SocialNetworkCreate,
    use_case: AddSocialNetworkUseCase = Depends(get_add_social_network_use_case),
):
    result = await use_case.execute(
        AddSocialNetworkRequest(
            profile_id=PROFILE_ID,
            platform=social_data.platform,
            url=social_data.url,
            order_index=social_data.order_index,
            username=social_data.username,
        )
    )
    return result


@router.put(
    "/{social_id}",
    response_model=SocialNetworkResponse,
    summary="Actualizar red social",
    description="Actualiza una red social existente",
)
async def update_social_network(
    social_id: str,
    social_data: SocialNetworkUpdate,
    use_case: EditSocialNetworkUseCase = Depends(get_edit_social_network_use_case),
):
    result = await use_case.execute(
        EditSocialNetworkRequest(
            social_network_id=social_id,
            platform=social_data.platform,
            url=social_data.url,
            username=social_data.username,
        )
    )
    return result


@router.delete(
    "/{social_id}",
    response_model=MessageResponse,
    summary="Eliminar red social",
    description="Elimina una red social del perfil",
)
async def delete_social_network(
    social_id: str,
    use_case: DeleteSocialNetworkUseCase = Depends(get_delete_social_network_use_case),
):
    await use_case.execute(DeleteSocialNetworkRequest(social_network_id=social_id))
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
    # TODO: Implementar con ReorderSocialNetworksUseCase
    return []
