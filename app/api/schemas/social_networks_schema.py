from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.common_schema import TimestampMixin


class SocialNetworkBase(BaseModel):
    """
    Enlace a una red social del usuario.
    Representa perfiles en plataformas sociales y profesionales.
    """

    platform: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Nombre de la red social (linkedin, github, twitter, etc.)",
    )
    url: str = Field(..., description="Enlace al perfil (debe ser válida)")
    order_index: int = Field(
        ...,
        ge=0,
        description="Orden de aparición en el portafolio (debe ser único dentro del perfil)",
    )
    username: str | None = Field(
        None,
        max_length=100,
        description="Nombre de usuario en la plataforma (opcional)",
    )


class SocialNetworkCreate(SocialNetworkBase):
    """
    Schema para crear red social.

    Invariantes:
    - platform no puede estar vacío
    - url debe ser válida
    - orderIndex debe ser único dentro del perfil
    """

    pass


class SocialNetworkUpdate(BaseModel):
    """
    Schema para actualizar red social.

    Todos los campos son opcionales, pero platform no puede quedar vacío si se actualiza.
    """

    platform: str | None = Field(None, min_length=1, max_length=50)
    url: str | None = None
    username: str | None = Field(None, max_length=100)
    order_index: int | None = Field(None, ge=0)


class SocialNetworkResponse(SocialNetworkBase, TimestampMixin):
    """
    Schema de respuesta de red social.

    Relaciones:
    - Pertenece a un único Profile
    - Un Profile tiene muchas SocialNetwork

    Invariantes:
    - orderIndex debe ser único dentro del perfil
    """

    id: str

    model_config = ConfigDict(from_attributes=True)
