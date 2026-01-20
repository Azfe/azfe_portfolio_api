from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime, date

from app.api.schemas.certification_schema import (
    CertificationResponse,
    CertificationCreate,
    CertificationUpdate
)
from app.api.schemas.common_schema import MessageResponse

router = APIRouter(prefix="/certifications", tags=["Certifications"])

# Mock data - Certificaciones del perfil único
MOCK_CERTIFICATIONS = [
    CertificationResponse(
        id="cert_001",
        name="AWS Certified Solutions Architect - Associate",
        issuer="Amazon Web Services",
        issue_date=date(2023, 6, 15),
        expiration_date=date(2026, 6, 15),
        credential_id="AWS-SAA-123456789",
        credential_url="https://www.credly.com/badges/aws-saa-123456789",
        order_index=1,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    CertificationResponse(
        id="cert_002",
        name="MongoDB Certified Developer Associate",
        issuer="MongoDB University",
        issue_date=date(2024, 2, 10),
        expiration_date=None,  # No expira
        credential_id="MONGODB-DEV-987654321",
        credential_url="https://university.mongodb.com/certification/certificate/987654321",
        order_index=0,  # Más reciente
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    CertificationResponse(
        id="cert_003",
        name="Professional Scrum Master I (PSM I)",
        issuer="Scrum.org",
        issue_date=date(2022, 11, 5),
        expiration_date=None,  # No expira
        credential_id="PSM-I-555666777",
        credential_url="https://www.scrum.org/certificates/555666777",
        order_index=3,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    CertificationResponse(
        id="cert_004",
        name="Microsoft Certified: Azure Fundamentals",
        issuer="Microsoft",
        issue_date=date(2023, 3, 20),
        expiration_date=None,  # No expira
        credential_id="AZ-900-111222333",
        credential_url="https://www.credly.com/badges/az900-111222333",
        order_index=2,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    CertificationResponse(
        id="cert_005",
        name="Docker Certified Associate (DCA)",
        issuer="Docker Inc.",
        issue_date=date(2021, 9, 12),
        expiration_date=date(2023, 9, 12),  # Expirada
        credential_id="DCA-444555666",
        credential_url="https://credentials.docker.com/444555666",
        order_index=4,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
]


@router.get(
    "",
    response_model=List[CertificationResponse],
    summary="Listar certificaciones",
    description="Obtiene todas las certificaciones ordenadas por orderIndex"
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
            cert for cert in certifications
            if cert.expiration_date is None or cert.expiration_date > today
        ]
    
    return sorted(certifications, key=lambda x: x.order_index)


@router.get(
    "/{certification_id}",
    response_model=CertificationResponse,
    summary="Obtener certificación",
    description="Obtiene una certificación específica por ID"
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
        detail=f"Certificación con ID '{certification_id}' no encontrada"
    )


@router.post(
    "",
    response_model=CertificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear certificación",
    description="Crea una nueva certificación asociada al perfil"
)
async def create_certification(certification_data: CertificationCreate):
    """
    Crea una nueva certificación y la asocia al perfil único del sistema.
    
    **Invariantes que se validan automáticamente:**
    - `name` no puede estar vacío (min_length=1)
    - `issuer` no puede estar vacío (min_length=1)
    - `issueDate` es obligatoria
    
    Args:
        certification_data: Datos de la certificación a crear
    
    Returns:
        CertificationResponse: Certificación creada
    
    Raises:
        HTTPException 422: Si los datos no cumplen las invariantes
    
    Notas:
    - Si la certificación no expira, dejar `expirationDate` como None
    - `credentialUrl` debe ser una URL válida si se proporciona
    
    TODO: Implementar con CreateCertificationUseCase
    TODO: Considerar auto-incrementar orderIndex si no se proporciona
    TODO: Validar formato de credentialId según issuer (opcional)
    TODO: Requiere autenticación de admin
    """
    return MOCK_CERTIFICATIONS[0]


@router.put(
    "/{certification_id}",
    response_model=CertificationResponse,
    summary="Actualizar certificación",
    description="Actualiza una certificación existente"
)
async def update_certification(
    certification_id: str,
    certification_data: CertificationUpdate
):
    """
    Actualiza una certificación existente.
    
    **Invariantes:**
    - Si se actualiza `name`, no puede estar vacío
    - Si se actualiza `issuer`, no puede estar vacío
    - Si se actualiza `credentialUrl`, debe ser una URL válida
    
    Args:
        certification_id: ID de la certificación a actualizar
        certification_data: Datos a actualizar (campos opcionales)
    
    Returns:
        CertificationResponse: Certificación actualizada
    
    Raises:
        HTTPException 404: Si la certificación no existe
        HTTPException 422: Si los datos no cumplen las invariantes
    
    Casos de uso comunes:
    - Actualizar expirationDate cuando se renueva la certificación
    - Actualizar credentialUrl si cambia el sistema de verificación
    
    TODO: Implementar con UpdateCertificationUseCase
    TODO: Requiere autenticación de admin
    """
    for cert in MOCK_CERTIFICATIONS:
        if cert.id == certification_id:
            return cert
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Certificación con ID '{certification_id}' no encontrada"
    )


@router.delete(
    "/{certification_id}",
    response_model=MessageResponse,
    summary="Eliminar certificación",
    description="Elimina una certificación del perfil"
)
async def delete_certification(certification_id: str):
    """
    Elimina una certificación del perfil.
    
    Nota: Al eliminar una certificación, puede ser necesario reordenar
    los orderIndex de las certificaciones restantes para mantener la coherencia.
    
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
        message=f"Certificación '{certification_id}' eliminada correctamente"
    )


@router.patch(
    "/reorder",
    response_model=List[CertificationResponse],
    summary="Reordenar certificaciones",
    description="Actualiza el orderIndex de múltiples certificaciones de una vez"
)
async def reorder_certifications(certification_orders: List[dict]):
    """
    Reordena múltiples certificaciones de una sola vez.
    
    Útil para drag & drop en el panel de administración.
    
    Args:
        certification_orders: Lista de objetos con {id, orderIndex}
        Ejemplo: [
            {"id": "cert_001", "orderIndex": 2},
            {"id": "cert_002", "orderIndex": 1},
            {"id": "cert_003", "orderIndex": 0}
        ]
    
    Returns:
        List[CertificationResponse]: Certificaciones reordenadas
    
    Raises:
        HTTPException 400: Si hay orderIndex duplicados
        HTTPException 404: Si algún certification_id no existe
    
    TODO: Implementar con ReorderCertificationsUseCase
    TODO: Validar que todos los orderIndex sean únicos
    TODO: Validar que todos los certification_id existan
    TODO: Hacer update en transacción (todo o nada)
    TODO: Requiere autenticación de admin
    """
    return sorted(MOCK_CERTIFICATIONS, key=lambda x: x.order_index)


@router.get(
    "/by-issuer/{issuer}",
    response_model=List[CertificationResponse],
    summary="Filtrar certificaciones por emisor",
    description="Obtiene certificaciones de un emisor específico"
)
async def get_certifications_by_issuer(issuer: str):
    """
    Filtra certificaciones por entidad emisora.
    
    Útil para agrupar certificaciones del mismo proveedor
    (ej: todas las certificaciones AWS, todas las de Microsoft).
    
    Args:
        issuer: Nombre del emisor (búsqueda case-insensitive)
    
    Returns:
        List[CertificationResponse]: Certificaciones del emisor
    
    TODO: Implementar con GetCertificationsByIssuerUseCase
    TODO: Hacer búsqueda case-insensitive y parcial (contains)
    """
    issuer_lower = issuer.lower()
    filtered = [
        cert for cert in MOCK_CERTIFICATIONS
        if issuer_lower in cert.issuer.lower()
    ]
    return sorted(filtered, key=lambda x: x.order_index)


@router.get(
    "/status/expired",
    response_model=List[CertificationResponse],
    summary="Listar certificaciones expiradas",
    description="Obtiene certificaciones que ya expiraron"
)
async def get_expired_certifications():
    """
    Lista certificaciones que ya han expirado.
    
    Útil para identificar qué certificaciones necesitan renovación.
    
    Returns:
        List[CertificationResponse]: Certificaciones expiradas
    
    Nota:
    - Las certificaciones sin expirationDate (None) nunca se consideran expiradas
    
    TODO: Implementar con GetExpiredCertificationsUseCase
    TODO: Ordenar por fecha de expiración (más reciente primero)
    """
    today = date.today()
    expired = [
        cert for cert in MOCK_CERTIFICATIONS
        if cert.expiration_date is not None and cert.expiration_date < today
    ]
    return sorted(expired, key=lambda x: x.expiration_date or date.max, reverse=True)


@router.get(
    "/status/expiring-soon",
    response_model=List[CertificationResponse],
    summary="Listar certificaciones próximas a expirar",
    description="Obtiene certificaciones que expiran en los próximos N días"
)
async def get_expiring_soon_certifications(days: int = 90):
    """
    Lista certificaciones que expiran pronto.
    
    Útil para mostrar alertas de renovación en el admin panel.
    
    Args:
        days: Número de días hacia el futuro para considerar (default: 90)
    
    Returns:
        List[CertificationResponse]: Certificaciones que expiran pronto
    
    Ejemplo:
    - GET /certifications/status/expiring-soon?days=30
      (certificaciones que expiran en los próximos 30 días)
    
    TODO: Implementar con GetExpiringSoonCertificationsUseCase
    TODO: Ordenar por fecha de expiración (más cercana primero)
    """
    from datetime import timedelta
    
    today = date.today()
    threshold = today + timedelta(days=days)
    
    expiring = [
        cert for cert in MOCK_CERTIFICATIONS
        if cert.expiration_date is not None
        and today < cert.expiration_date <= threshold
    ]
    return sorted(expiring, key=lambda x: x.expiration_date or date.max)