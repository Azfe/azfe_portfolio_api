from datetime import date

from pydantic import BaseModel, Field, HttpUrl

from app.api.schemas.common_schema import TimestampMixin


class CertificationBase(BaseModel):
    """
    Certificación profesional obtenida por el usuario.
    Representa certificaciones oficiales de proveedores tecnológicos, organizaciones, etc.
    """

    name: str = Field(
        ...,
        min_length=1,
        description="Nombre de la certificación (no puede estar vacío)",
    )
    issuer: str = Field(
        ..., min_length=1, description="Entidad emisora (no puede estar vacía)"
    )
    issue_date: date = Field(..., description="Fecha de emisión (obligatoria)")
    expiration_date: date | None = Field(
        None, description="Fecha de expiración (opcional, None = no expira)"
    )
    credential_id: str | None = Field(
        None, description="Identificador de la credencial (opcional)"
    )
    credential_url: HttpUrl | None = Field(
        None, description="URL verificable de la credencial (opcional)"
    )
    order_index: int = Field(
        ..., ge=0, description="Orden de aparición en el portafolio"
    )


class CertificationCreate(CertificationBase):
    """
    Schema para crear certificación.

    Invariantes:
    - name no puede estar vacío
    - issuer no puede estar vacío
    - issueDate es obligatoria
    """

    pass


class CertificationUpdate(BaseModel):
    """
    Schema para actualizar certificación.

    Todos los campos son opcionales, pero name e issuer
    no pueden quedar vacíos si se actualizan.
    """

    name: str | None = Field(None, min_length=1)
    issuer: str | None = Field(None, min_length=1)
    issue_date: date | None = None
    expiration_date: date | None = None
    credential_id: str | None = None
    credential_url: HttpUrl | None = None
    order_index: int | None = Field(None, ge=0)


class CertificationResponse(CertificationBase, TimestampMixin):
    """
    Schema de respuesta de certificación.

    Relaciones:
    - Pertenece a un único Profile
    - Un Profile tiene muchas Certification
    """

    id: str

    class Config:
        from_attributes = True
