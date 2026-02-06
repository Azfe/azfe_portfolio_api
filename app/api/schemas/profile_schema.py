from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.common_schema import TimestampMixin


class ProfileBase(BaseModel):
    """
    Perfil profesional del usuario.
    Representa la información personal y profesional visible en el portfolio.
    """

    name: str = Field(
        ..., min_length=1, max_length=100, description="Nombre completo (no puede estar vacío)"
    )
    headline: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Título profesional o rol principal (no puede estar vacío)",
    )
    bio: str | None = Field(None, max_length=1000, description="Descripción o resumen profesional")
    location: str | None = Field(
        None, max_length=100, description="Ubicación física o modalidad de trabajo"
    )
    avatar_url: str | None = Field(None, description="URL de la imagen de perfil")


class ProfileCreate(ProfileBase):
    """
    Schema para crear perfil.

    Nota: Solo puede existir UN perfil activo en el sistema (invariante).
    """

    pass


class ProfileUpdate(BaseModel):
    """
    Schema para actualizar perfil.

    Todos los campos son opcionales excepto name y headline
    que no pueden quedar vacíos si se actualizan.
    """

    name: str | None = Field(None, min_length=1, max_length=100)
    headline: str | None = Field(None, min_length=1, max_length=100)
    bio: str | None = Field(None, max_length=1000)
    location: str | None = Field(None, max_length=100)
    avatar_url: str | None = None


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

    model_config = ConfigDict(from_attributes=True)
