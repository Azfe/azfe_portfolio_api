from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.common_schema import TimestampMixin


class AdditionalTrainingBase(BaseModel):
    """
    Formación complementaria no académica del usuario.
    Representa cursos, talleres, workshops, bootcamps, etc.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre del curso o formación (no puede estar vacío)",
    )
    provider: str = Field(
        ..., min_length=1, max_length=100, description="Entidad que lo impartió (no puede estar vacía)"
    )
    completion_date: datetime = Field(..., description="Fecha de realización (obligatoria)")
    order_index: int = Field(
        ..., ge=0, description="Orden de aparición en el portafolio"
    )
    duration: str | None = Field(
        None, max_length=50, description="Duración del curso (ej: '40 horas', '3 meses')"
    )
    certificate_url: str | None = Field(
        None, description="URL del certificado (opcional)"
    )
    description: str | None = Field(
        None, max_length=1000, description="Detalles adicionales (temario, logros, etc.)"
    )


class AdditionalTrainingCreate(AdditionalTrainingBase):
    """
    Schema para crear formación adicional.

    Invariantes:
    - title no puede estar vacío
    - provider no puede estar vacía
    - completion_date es obligatoria
    """

    pass


class AdditionalTrainingUpdate(BaseModel):
    """
    Schema para actualizar formación adicional.

    Todos los campos son opcionales, pero title y provider
    no pueden quedar vacíos si se actualizan.
    """

    title: str | None = Field(None, min_length=1, max_length=100)
    provider: str | None = Field(None, min_length=1, max_length=100)
    completion_date: datetime | None = None
    duration: str | None = Field(None, max_length=50)
    certificate_url: str | None = None
    description: str | None = Field(None, max_length=1000)
    order_index: int | None = Field(None, ge=0)


class AdditionalTrainingResponse(AdditionalTrainingBase, TimestampMixin):
    """
    Schema de respuesta de formación adicional.

    Relaciones:
    - Pertenece a un único Profile
    - Un Profile tiene muchos AdditionalTraining
    """

    id: str

    model_config = ConfigDict(from_attributes=True)
