from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.common_schema import TimestampMixin


class CertificationBase(BaseModel):
    """
    Certificación profesional obtenida por el usuario.
    Representa certificaciones oficiales de proveedores tecnológicos, organizaciones, etc.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre de la certificación (no puede estar vacío)",
    )
    issuer: str = Field(
        ..., min_length=1, max_length=100, description="Entidad emisora (no puede estar vacía)"
    )
    issue_date: datetime = Field(..., description="Fecha de emisión (obligatoria)")
    order_index: int = Field(
        ..., ge=0, description="Orden de aparición en el portafolio"
    )
    expiry_date: datetime | None = Field(
        None, description="Fecha de expiración (opcional, None = no expira)"
    )
    credential_id: str | None = Field(
        None, description="Identificador de la credencial (opcional)"
    )
    credential_url: str | None = Field(
        None, description="URL verificable de la credencial (opcional)"
    )


class CertificationCreate(CertificationBase):
    """
    Schema para crear certificación.

    Invariantes:
    - title no puede estar vacío
    - issuer no puede estar vacío
    - issueDate es obligatoria
    """

    pass


class CertificationUpdate(BaseModel):
    """
    Schema para actualizar certificación.

    Todos los campos son opcionales, pero title e issuer
    no pueden quedar vacíos si se actualizan.
    """

    title: str | None = Field(None, min_length=1, max_length=100)
    issuer: str | None = Field(None, min_length=1, max_length=100)
    issue_date: datetime | None = None
    expiry_date: datetime | None = None
    credential_id: str | None = None
    credential_url: str | None = None
    order_index: int | None = Field(None, ge=0)


class CertificationResponse(CertificationBase, TimestampMixin):
    """
    Schema de respuesta de certificación.

    Relaciones:
    - Pertenece a un único Profile
    - Un Profile tiene muchas Certification
    """

    id: str

    model_config = ConfigDict(from_attributes=True)
