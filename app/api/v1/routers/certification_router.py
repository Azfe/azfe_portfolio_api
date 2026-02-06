from datetime import date, datetime

from fastapi import APIRouter, HTTPException, status

from app.api.schemas.certification_schema import (
    CertificationCreate,
    CertificationResponse,
    CertificationUpdate,
)
from app.api.schemas.common_schema import MessageResponse

router = APIRouter(prefix="/certifications", tags=["Certifications"])

# Mock data - Certificaciones del perfil único
MOCK_CERTIFICATIONS = [
    CertificationResponse(
        id="cert_001",
        title="AWS Certified Solutions Architect - Associate",
        issuer="Amazon Web Services",
        issue_date=datetime(2023, 6, 15),
        expiry_date=datetime(2026, 6, 15),
        credential_id="AWS-SAA-123456789",
        credential_url="https://www.credly.com/badges/aws-saa-123456789",
        order_index=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    CertificationResponse(
        id="cert_002",
        title="MongoDB Certified Developer Associate",
        issuer="MongoDB University",
        issue_date=datetime(2024, 2, 10),
        expiry_date=None,  # No expira
        credential_id="MONGODB-DEV-987654321",
        credential_url="https://university.mongodb.com/certification/certificate/987654321",
        order_index=0,  # Más reciente
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    CertificationResponse(
        id="cert_003",
        title="Professional Scrum Master I (PSM I)",
        issuer="Scrum.org",
        issue_date=datetime(2022, 11, 5),
        expiry_date=None,  # No expira
        credential_id="PSM-I-555666777",
        credential_url="https://www.scrum.org/certificates/555666777",
        order_index=3,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    CertificationResponse(
        id="cert_004",
        title="Microsoft Certified: Azure Fundamentals",
        issuer="Microsoft",
        issue_date=datetime(2023, 3, 20),
        expiry_date=None,  # No expira
        credential_id="AZ-900-111222333",
        credential_url="https://www.credly.com/badges/az900-111222333",
        order_index=2,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    CertificationResponse(
        id="cert_005",
        title="Docker Certified Associate (DCA)",
        issuer="Docker Inc.",
        issue_date=datetime(2021, 9, 12),
        expiry_date=datetime(2023, 9, 12),  # Expirada
        credential_id="DCA-444555666",
        credential_url="https://credentials.docker.com/444555666",
        order_index=4,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]


@router.get(
    "",
    response_model=list[CertificationResponse],
    summary="Listar certificaciones",
    description="Obtiene todas las certificaciones ordenadas por orderIndex",
)
async def get_certifications(active_only: bool = False):
    """
    Lista todas las certificaciones del perfil único del sistema.

    Las certificaciones se retornan ordenadas por `order_index` ascendente.
    Típicamente, las certificaciones más recientes o vigentes tienen order_index menor.

    Args:
        active_only: Si es True, solo retorna certificaciones vigentes (no expiradas)

    Returns:
        List[CertificationResponse]: Lista de certificaciones ordenadas

    Relación:
    - Todas las certificaciones pertenecen al Profile único del sistema

    TODO: Implementar con GetCertificationsUseCase
    TODO: Ordenar por order_index ASC (vigentes primero, luego más recientes)
    TODO: Filtrar por vigencia si active_only=True
    """
    certifications = MOCK_CERTIFICATIONS

    if active_only:
        today = date.today()
        certifications = [
            cert
            for cert in certifications
            if cert.expiry_date is None or cert.expiry_date.date() > today
        ]

    return sorted(certifications, key=lambda x: x.order_index)


@router.get(
    "/{certification_id}",
    response_model=CertificationResponse,
    summary="Obtener certificación",
    description="Obtiene una certificación específica por ID",
)
async def get_certification(certification_id: str):
    """
    Obtiene una certificación por su ID.

    Args:
        certification_id: ID único de la certificación

    Returns:
        CertificationResponse: Certificación encontrada

    Raises:
        HTTPException 404: Si la certificación no existe

    TODO: Implementar con GetCertificationUseCase
    """
    for cert in MOCK_CERTIFICATIONS:
        if cert.id == certification_id:
            return cert

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Certificación con ID '{certification_id}' no encontrada",
    )


@router.post(
    "",
    response_model=CertificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear certificación",
    description="Crea una nueva certificación asociada al perfil",
)
async def create_certification(_certification_data: CertificationCreate):
    """
    Crea una nueva certificación y la asocia al perfil único del sistema.

    **Invariantes que se validan automáticamente:**
    - `title` no puede estar vacío (min_length=1)
    - `issuer` no puede estar vacío (min_length=1)
    - `issueDate` es obligatoria

    Args:
        certification_data: Datos de la certificación a crear

    Returns:
        CertificationResponse: Certificación creada

    Raises:
        HTTPException 422: Si los datos no cumplen las invariantes

    TODO: Implementar con CreateCertificationUseCase
    TODO: Considerar auto-incrementar orderIndex si no se proporciona
    TODO: Requiere autenticación de admin
    """
    return MOCK_CERTIFICATIONS[0]


@router.put(
    "/{certification_id}",
    response_model=CertificationResponse,
    summary="Actualizar certificación",
    description="Actualiza una certificación existente",
)
async def update_certification(
    certification_id: str, _certification_data: CertificationUpdate
):
    """
    Actualiza una certificación existente.

    **Invariantes:**
    - Si se actualiza `title`, no puede estar vacío
    - Si se actualiza `issuer`, no puede estar vacío

    Args:
        certification_id: ID de la certificación a actualizar
        certification_data: Datos a actualizar (campos opcionales)

    Returns:
        CertificationResponse: Certificación actualizada

    Raises:
        HTTPException 404: Si la certificación no existe
        HTTPException 422: Si los datos no cumplen las invariantes

    TODO: Implementar con UpdateCertificationUseCase
    TODO: Requiere autenticación de admin
    """
    for cert in MOCK_CERTIFICATIONS:
        if cert.id == certification_id:
            return cert

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Certificación con ID '{certification_id}' no encontrada",
    )


@router.delete(
    "/{certification_id}",
    response_model=MessageResponse,
    summary="Eliminar certificación",
    description="Elimina una certificación del perfil",
)
async def delete_certification(certification_id: str):
    """
    Elimina una certificación del perfil.

    Args:
        certification_id: ID de la certificación a eliminar

    Returns:
        MessageResponse: Confirmación de eliminación

    Raises:
        HTTPException 404: Si la certificación no existe

    TODO: Implementar con DeleteCertificationUseCase
    TODO: Considerar reordenamiento automático de orderIndex
    TODO: Requiere autenticación de admin
    """
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
    """
    Reordena múltiples certificaciones de una sola vez.

    Útil para drag & drop en el panel de administración.

    Args:
        certification_orders: Lista de objetos con {id, orderIndex}

    Returns:
        List[CertificationResponse]: Certificaciones reordenadas

    Raises:
        HTTPException 400: Si hay orderIndex duplicados
        HTTPException 404: Si algún certification_id no existe

    TODO: Implementar con ReorderCertificationsUseCase
    TODO: Requiere autenticación de admin
    """
    return sorted(MOCK_CERTIFICATIONS, key=lambda x: x.order_index)


@router.get(
    "/by-issuer/{issuer}",
    response_model=list[CertificationResponse],
    summary="Filtrar certificaciones por emisor",
    description="Obtiene certificaciones de un emisor específico",
)
async def get_certifications_by_issuer(issuer: str):
    """
    Filtra certificaciones por entidad emisora.

    Args:
        issuer: Nombre del emisor (búsqueda case-insensitive)

    Returns:
        List[CertificationResponse]: Certificaciones del emisor

    TODO: Implementar con GetCertificationsByIssuerUseCase
    """
    issuer_lower = issuer.lower()
    filtered = [
        cert for cert in MOCK_CERTIFICATIONS if issuer_lower in cert.issuer.lower()
    ]
    return sorted(filtered, key=lambda x: x.order_index)


@router.get(
    "/status/expired",
    response_model=list[CertificationResponse],
    summary="Listar certificaciones expiradas",
    description="Obtiene certificaciones que ya expiraron",
)
async def get_expired_certifications():
    """
    Lista certificaciones que ya han expirado.

    Returns:
        List[CertificationResponse]: Certificaciones expiradas

    TODO: Implementar con GetExpiredCertificationsUseCase
    """
    today = date.today()
    expired = [
        cert
        for cert in MOCK_CERTIFICATIONS
        if cert.expiry_date is not None and cert.expiry_date.date() < today
    ]
    return sorted(expired, key=lambda x: x.expiry_date or datetime.max, reverse=True)


@router.get(
    "/status/expiring-soon",
    response_model=list[CertificationResponse],
    summary="Listar certificaciones próximas a expirar",
    description="Obtiene certificaciones que expiran en los próximos N días",
)
async def get_expiring_soon_certifications(days: int = 90):
    """
    Lista certificaciones que expiran pronto.

    Args:
        days: Número de días hacia el futuro para considerar (default: 90)

    Returns:
        List[CertificationResponse]: Certificaciones que expiran pronto

    TODO: Implementar con GetExpiringSoonCertificationsUseCase
    """
    from datetime import timedelta

    today = date.today()
    threshold = today + timedelta(days=days)

    expiring = [
        cert
        for cert in MOCK_CERTIFICATIONS
        if cert.expiry_date is not None and today < cert.expiry_date.date() <= threshold
    ]
    return sorted(expiring, key=lambda x: x.expiry_date or datetime.max)
