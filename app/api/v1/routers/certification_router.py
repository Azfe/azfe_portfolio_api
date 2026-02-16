from datetime import date, timedelta

from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_add_certification_use_case,
    get_certification_repository,
    get_delete_certification_use_case,
    get_edit_certification_use_case,
    get_list_certifications_use_case,
)
from app.api.schemas.certification_schema import (
    CertificationCreate,
    CertificationResponse,
    CertificationUpdate,
)
from app.api.schemas.common_schema import MessageResponse
from app.application.dto import AddCertificationRequest
from app.application.dto import CertificationResponse as CertificationDTO
from app.application.dto import (
    DeleteCertificationRequest,
    EditCertificationRequest,
    ListCertificationsRequest,
)
from app.application.use_cases.certification import (
    AddCertificationUseCase,
    DeleteCertificationUseCase,
    EditCertificationUseCase,
    ListCertificationsUseCase,
)
from app.infrastructure.repositories import CertificationRepository
from app.shared.shared_exceptions import NotFoundException

router = APIRouter(prefix="/certifications", tags=["Certifications"])

PROFILE_ID = "default_profile"


@router.get(
    "",
    response_model=list[CertificationResponse],
    summary="Listar certificaciones",
    description="Obtiene todas las certificaciones ordenadas por orderIndex",
)
async def get_certifications(
    active_only: bool = False,
    use_case: ListCertificationsUseCase = Depends(get_list_certifications_use_case),
):
    result = await use_case.execute(ListCertificationsRequest(profile_id=PROFILE_ID))
    certs = result.certifications
    if active_only:
        today = date.today()
        certs = [
            c for c in certs if c.expiry_date is None or c.expiry_date.date() > today
        ]
    return certs


@router.get(
    "/{certification_id}",
    response_model=CertificationResponse,
    summary="Obtener certificación",
    description="Obtiene una certificación específica por ID",
)
async def get_certification(
    certification_id: str,
    repo: CertificationRepository = Depends(get_certification_repository),
):
    entity = await repo.get_by_id(certification_id)
    if not entity:
        raise NotFoundException("Certification", certification_id)
    return CertificationDTO.from_entity(entity)


@router.post(
    "",
    response_model=CertificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear certificación",
    description="Crea una nueva certificación asociada al perfil",
)
async def create_certification(
    certification_data: CertificationCreate,
    use_case: AddCertificationUseCase = Depends(get_add_certification_use_case),
):
    result = await use_case.execute(
        AddCertificationRequest(
            profile_id=PROFILE_ID,
            title=certification_data.title,
            issuer=certification_data.issuer,
            issue_date=certification_data.issue_date,
            order_index=certification_data.order_index,
            expiry_date=certification_data.expiry_date,
            credential_id=certification_data.credential_id,
            credential_url=certification_data.credential_url,
        )
    )
    return result


@router.put(
    "/{certification_id}",
    response_model=CertificationResponse,
    summary="Actualizar certificación",
    description="Actualiza una certificación existente",
)
async def update_certification(
    certification_id: str,
    certification_data: CertificationUpdate,
    use_case: EditCertificationUseCase = Depends(get_edit_certification_use_case),
):
    result = await use_case.execute(
        EditCertificationRequest(
            certification_id=certification_id,
            title=certification_data.title,
            issuer=certification_data.issuer,
            issue_date=certification_data.issue_date,
            expiry_date=certification_data.expiry_date,
            credential_id=certification_data.credential_id,
            credential_url=certification_data.credential_url,
        )
    )
    return result


@router.delete(
    "/{certification_id}",
    response_model=MessageResponse,
    summary="Eliminar certificación",
    description="Elimina una certificación del perfil",
)
async def delete_certification(
    certification_id: str,
    use_case: DeleteCertificationUseCase = Depends(get_delete_certification_use_case),
):
    await use_case.execute(
        DeleteCertificationRequest(certification_id=certification_id)
    )
    return MessageResponse(
        success=True,
        message=f"Certificación '{certification_id}' eliminada correctamente",
    )


@router.patch(
    "/reorder",
    response_model=list[CertificationResponse],
    summary="Reordenar certificaciones",
    description="Actualiza el orderIndex de múltiples certificaciones de una vez",
)
async def reorder_certifications(_certification_orders: list[dict]):
    # TODO: Implement with ReorderCertificationsUseCase
    return []


@router.get(
    "/by-issuer/{issuer}",
    response_model=list[CertificationResponse],
    summary="Filtrar certificaciones por emisor",
    description="Obtiene certificaciones de un emisor específico",
)
async def get_certifications_by_issuer(
    issuer: str,
    use_case: ListCertificationsUseCase = Depends(get_list_certifications_use_case),
):
    result = await use_case.execute(ListCertificationsRequest(profile_id=PROFILE_ID))
    issuer_lower = issuer.lower()
    return [c for c in result.certifications if issuer_lower in c.issuer.lower()]


@router.get(
    "/status/expired",
    response_model=list[CertificationResponse],
    summary="Listar certificaciones expiradas",
    description="Obtiene certificaciones que ya expiraron",
)
async def get_expired_certifications(
    use_case: ListCertificationsUseCase = Depends(get_list_certifications_use_case),
):
    result = await use_case.execute(ListCertificationsRequest(profile_id=PROFILE_ID))
    return [c for c in result.certifications if c.is_expired]


@router.get(
    "/status/expiring-soon",
    response_model=list[CertificationResponse],
    summary="Listar certificaciones próximas a expirar",
    description="Obtiene certificaciones que expiran en los próximos N días",
)
async def get_expiring_soon_certifications(
    days: int = 90,
    use_case: ListCertificationsUseCase = Depends(get_list_certifications_use_case),
):
    result = await use_case.execute(ListCertificationsRequest(profile_id=PROFILE_ID))
    today = date.today()
    threshold = today + timedelta(days=days)
    return [
        c
        for c in result.certifications
        if c.expiry_date is not None
        and not c.is_expired
        and c.expiry_date.date() <= threshold
    ]
