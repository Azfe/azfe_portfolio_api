
from pydantic import BaseModel, Field

from app.api.schemas.common_schema import TimestampMixin


class ProfileBase(BaseModel):
    """
    Perfil profesional del usuario.
    Representa la información personal y profesional visible en el portfolio.
    """

    full_name: str = Field(
        ..., min_length=1, description="Nombre completo (no puede estar vacío)"
    )
    headline: str = Field(
        ...,
        min_length=1,
        description="Título profesional o rol principal (no puede estar vacío)",
    )
    about: str | None = Field(None, description="Descripción o resumen profesional")
    location: str | None = Field(
        None, description="Ubicación física o modalidad de trabajo"
    )
    profile_image: str | None = Field(None, description="URL de la imagen de perfil")
    banner_image: str | None = Field(
        None, description="URL de la imagen de portada/banner"
    )


class ProfileCreate(ProfileBase):
    """
    Schema para crear perfil.

    Nota: Solo puede existir UN perfil activo en el sistema (invariante).
    """

    pass


class ProfileUpdate(BaseModel):
    """
    Schema para actualizar perfil.

    Todos los campos son opcionales excepto full_name y headline
    que no pueden quedar vacíos si se actualizan.
    """

    full_name: str | None = Field(None, min_length=1)
    headline: str | None = Field(None, min_length=1)
    about: str | None = None
    location: str | None = None
    profile_image: str | None = None
    banner_image: str | None = None


class ProfileResponse(ProfileBase, TimestampMixin):
    """
    Schema de respuesta del perfil.

    Relaciones:
    - Tiene muchos Projects
    - Tiene muchas Education
    - Tiene muchos AdditionalTraining
    - Tiene muchas Certification
    - Tiene muchas TechnicalSkill
    - Tiene muchas Tool
    - Tiene una ContactInformation
    - Tiene muchas ContactMessage
    - Tiene muchas SocialNetwork
    """

    id: str

    class Config:
        from_attributes = True
