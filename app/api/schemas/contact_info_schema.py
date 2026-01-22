from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional
from app.api.schemas.common_schema import TimestampMixin


class ContactInformationBase(BaseModel):
    """
    Información de contacto pública del usuario.
    Representa los datos de contacto visibles en el portfolio.
    """
    email: EmailStr = Field(..., description="Correo de contacto (no puede estar vacío)")
    phone: Optional[str] = Field(None, description="Número de teléfono (opcional)")
    location: Optional[str] = Field(None, description="Ubicación general (ciudad, país)")
    website: Optional[HttpUrl] = Field(None, description="Sitio web personal (opcional)")


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
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    website: Optional[HttpUrl] = None


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
    
    class Config:
        from_attributes = True