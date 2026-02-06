from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.api.schemas.common_schema import TimestampMixin


class ContactInformationBase(BaseModel):
    """
    Información de contacto pública del usuario.
    Representa los datos de contacto visibles en el portfolio.
    """

    email: EmailStr = Field(
        ..., description="Correo de contacto (no puede estar vacío)"
    )
    phone: str | None = Field(None, description="Número de teléfono (opcional)")
    linkedin: str | None = Field(None, description="URL de LinkedIn (opcional)")
    github: str | None = Field(None, description="URL de GitHub (opcional)")
    website: str | None = Field(None, description="Sitio web personal (opcional)")


class ContactInformationCreate(ContactInformationBase):
    """
    Schema para crear información de contacto.

    Invariantes:
    - email no puede estar vacío
    - Solo puede existir una ContactInformation por perfil
    """

    pass


class ContactInformationUpdate(BaseModel):
    """
    Schema para actualizar información de contacto.

    Todos los campos son opcionales, pero email no puede quedar vacío si se actualiza.
    """

    email: EmailStr | None = None
    phone: str | None = None
    linkedin: str | None = None
    github: str | None = None
    website: str | None = None


class ContactInformationResponse(ContactInformationBase, TimestampMixin):
    """
    Schema de respuesta de información de contacto.

    Relaciones:
    - Pertenece a un único Profile (relación 1-a-1)
    - Un Profile tiene una única ContactInformation

    Invariantes:
    - Solo puede existir una ContactInformation por perfil
    """

    id: str

    model_config = ConfigDict(from_attributes=True)
