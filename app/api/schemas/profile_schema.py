from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from app.api.schemas.common_schema import TimestampMixin


class ProfileBase(BaseModel):
    """
    Perfil profesional del usuario.
    Representa la información personal y profesional visible en el portfolio.
    """
    full_name: str = Field(..., min_length=1, description="Nombre completo (no puede estar vacío)")
    headline: str = Field(..., min_length=1, description="Título profesional o rol principal (no puede estar vacío)")
    about: Optional[str] = Field(None, description="Descripción o resumen profesional")
    location: Optional[str] = Field(None, description="Ubicación física o modalidad de trabajo")
    profile_image: Optional[str] = Field(None, description="URL de la imagen de perfil")
    banner_image: Optional[str] = Field(None, description="URL de la imagen de portada/banner")


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
    full_name: Optional[str] = Field(None, min_length=1)
    headline: Optional[str] = Field(None, min_length=1)
    about: Optional[str] = None
    location: Optional[str] = None
    profile_image: Optional[str] = None
    banner_image: Optional[str] = None


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