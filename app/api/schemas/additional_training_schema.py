from datetime import date

from pydantic import BaseModel, Field

from app.api.schemas.common_schema import TimestampMixin


class AdditionalTrainingBase(BaseModel):
    """
    Formación complementaria no académica del usuario.
    Representa cursos, talleres, workshops, bootcamps, etc.
    """

    title: str = Field(
        ...,
        min_length=1,
        description="Nombre del curso o formación (no puede estar vacío)",
    )
    institution: str = Field(
        ..., min_length=1, description="Entidad que lo impartió (no puede estar vacía)"
    )
    end_date: date = Field(..., description="Fecha de realización (obligatoria)")
    duration_hours: int | None = Field(
        None, ge=1, description="Duración en horas (opcional)"
    )
    description: str | None = Field(
        None, description="Detalles adicionales (temario, logros, etc.)"
    )
    location: str | None = Field(
        None, description="Ubicación del centro (presencial, online, ciudad)"
    )
    technologies: list[str] = Field(
        default_factory=list,
        description="Tecnologías aprendidas (se vincula con Skills)",
    )
    order_index: int = Field(
        ..., ge=0, description="Orden de aparición en el portafolio"
    )


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

    title: str | None = Field(None, min_length=1)
    institution: str | None = Field(None, min_length=1)
    end_date: date | None = None
    duration_hours: int | None = Field(None, ge=1)
    description: str | None = None
    location: str | None = None
    technologies: list[str] | None = None
    order_index: int | None = Field(None, ge=0)


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
