from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from app.api.schemas.common_schema import TimestampMixin


class AdditionalTrainingBase(BaseModel):
    """
    Formación complementaria no académica del usuario.
    Representa cursos, talleres, workshops, bootcamps, etc.
    """
    title: str = Field(..., min_length=1, description="Nombre del curso o formación (no puede estar vacío)")
    institution: str = Field(..., min_length=1, description="Entidad que lo impartió (no puede estar vacía)")
    end_date: date = Field(..., description="Fecha de realización (obligatoria)")
    duration_hours: Optional[int] = Field(None, ge=1, description="Duración en horas (opcional)")
    description: Optional[str] = Field(None, description="Detalles adicionales (temario, logros, etc.)")
    location: Optional[str] = Field(None, description="Ubicación del centro (presencial, online, ciudad)")
    technologies: List[str] = Field(default_factory=list, description="Tecnologías aprendidas (se vincula con Skills)")
    order_index: int = Field(..., ge=0, description="Orden de aparición en el portafolio")


class AdditionalTrainingCreate(AdditionalTrainingBase):
    """
    Schema para crear formación adicional.
    
    Invariantes:
    - title no puede estar vacío
    - institution no puede estar vacía
    - date es obligatoria
    """
    pass


class AdditionalTrainingUpdate(BaseModel):
    """
    Schema para actualizar formación adicional.
    
    Todos los campos son opcionales, pero title e institution
    no pueden quedar vacíos si se actualizan.
    """
    title: Optional[str] = Field(None, min_length=1)
    institution: Optional[str] = Field(None, min_length=1)
    end_date: Optional[date] = None
    duration_hours: Optional[int] = Field(None, ge=1)
    description: Optional[str] = None
    location: Optional[str] = None
    technologies: Optional[List[str]] = None
    order_index: Optional[int] = Field(None, ge=0)


class AdditionalTrainingResponse(AdditionalTrainingBase, TimestampMixin):
    """
    Schema de respuesta de formación adicional.
    
    Relaciones:
    - Pertenece a un único Profile
    - Un Profile tiene muchos AdditionalTraining
    - technologies se vincula con Skills (tecnologías aprendidas)
    """
    id: str
    
    class Config:
        from_attributes = True