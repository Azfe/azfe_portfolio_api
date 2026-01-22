from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Literal
from app.api.schemas.common_schema import TimestampMixin


# Plataformas de redes sociales más comunes
SocialPlatform = Literal[
    "github",
    "gitlab",
    "linkedin",
    "twitter",      # X (Twitter)
    "x",            # Alias para Twitter
    "stackoverflow",
    "medium",
    "dev_to",
    "hashnode",
    "youtube",
    "instagram",
    "facebook",
    "discord",
    "telegram",
    "website",      # Sitio web personal
    "blog",         # Blog personal
    "other"
]


class SocialNetworkBase(BaseModel):
    """
    Enlace a una red social del usuario.
    Representa perfiles en plataformas sociales y profesionales.
    """
    platform: SocialPlatform = Field(..., description="Nombre de la red social (linkedin, github, twitter, etc.)")
    url: HttpUrl = Field(..., description="Enlace al perfil (debe ser válida)")
    icon: Optional[str] = Field(None, description="Icono o identificador visual (URL, emoji, nombre del icono)")
    order_index: int = Field(..., ge=0, description="Orden de aparición en el portafolio (debe ser único dentro del perfil)")


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
    platform: Optional[SocialPlatform] = None
    url: Optional[HttpUrl] = None
    icon: Optional[str] = None
    order_index: Optional[int] = Field(None, ge=0)


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
    
    class Config:
        from_attributes = True