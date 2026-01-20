from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
from app.api.schemas.common_schema import TimestampMixin


class EducationBase(BaseModel):
    """
    Formación académica formal del usuario.
    Representa estudios universitarios, ciclos formativos, etc.
    """
    institution: str = Field(..., min_length=1, description="Nombre de la institución (no puede estar vacía)")
    degree: str = Field(..., min_length=1, description="Título obtenido o en curso (no puede estar vacío)")
    start_date: date = Field(..., description="Fecha de inicio (obligatoria)")
    end_date: Optional[date] = Field(None, description="Fecha de fin (opcional, None = en curso)")
    description: Optional[str] = Field(None, description="Detalles adicionales (especialización, logros, etc.)")
    order_index: int = Field(..., ge=0, description="Orden de aparición en el portafolio")

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[date], info) -> Optional[date]:
        """
        Valida que endDate sea posterior a startDate si existe.
        
        Invariante: Si endDate existe, debe ser posterior a startDate.
        """
        if v is not None and 'start_date' in info.data:
            start_date = info.data['start_date']
            if v <= start_date:
                raise ValueError('end_date debe ser posterior a start_date')
        return v


class EducationCreate(EducationBase):
    """
    Schema para crear formación académica.
    
    Invariantes:
    - institution no puede estar vacía
    - degree no puede estar vacío
    - startDate es obligatoria
    - Si endDate existe, debe ser posterior a startDate
    """
    pass


class EducationUpdate(BaseModel):
    """
    Schema para actualizar formación académica.
    
    Todos los campos son opcionales, pero institution y degree
    no pueden quedar vacíos si se actualizan.
    """
    institution: Optional[str] = Field(None, min_length=1)
    degree: Optional[str] = Field(None, min_length=1)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    order_index: Optional[int] = Field(None, ge=0)

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[date], info) -> Optional[date]:
        """Valida que endDate sea posterior a startDate si ambos están presentes."""
        if v is not None and 'start_date' in info.data and info.data['start_date'] is not None:
            if v <= info.data['start_date']:
                raise ValueError('end_date debe ser posterior a start_date')
        return v


class EducationResponse(EducationBase, TimestampMixin):
    """
    Schema de respuesta de formación académica.
    
    Relaciones:
    - Pertenece a un único Profile
    - Un Profile tiene muchas Education
    """
    id: str
    
    class Config:
        from_attributes = True