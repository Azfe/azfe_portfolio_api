from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.api.schemas.common_schema import TimestampMixin


class EducationBase(BaseModel):
    """
    Formación académica formal del usuario.
    Representa estudios universitarios, ciclos formativos, etc.
    """

    institution: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre de la institución (no puede estar vacía)",
    )
    degree: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Título obtenido o en curso (no puede estar vacío)",
    )
    field: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Campo de estudio (no puede estar vacío)",
    )
    start_date: datetime = Field(..., description="Fecha de inicio (obligatoria)")
    order_index: int = Field(
        ..., ge=0, description="Orden de aparición en el portafolio"
    )
    description: str | None = Field(
        None,
        max_length=1000,
        description="Detalles adicionales (especialización, logros, etc.)",
    )
    end_date: datetime | None = Field(
        None, description="Fecha de fin (opcional, None = en curso)"
    )

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, v: datetime | None, info) -> datetime | None:
        """
        Valida que endDate sea posterior a startDate si existe.

        Invariante: Si endDate existe, debe ser posterior a startDate.
        """
        if v is not None and "start_date" in info.data:
            start_date = info.data["start_date"]
            if v <= start_date:
                raise ValueError("end_date debe ser posterior a start_date")
        return v


class EducationCreate(EducationBase):
    """
    Schema para crear formación académica.

    Invariantes:
    - institution no puede estar vacía
    - degree no puede estar vacío
    - field no puede estar vacío
    - startDate es obligatoria
    - Si endDate existe, debe ser posterior a startDate
    """

    pass


class EducationUpdate(BaseModel):
    """
    Schema para actualizar formación académica.

    Todos los campos son opcionales, pero institution, degree y field
    no pueden quedar vacíos si se actualizan.
    """

    institution: str | None = Field(None, min_length=1, max_length=100)
    degree: str | None = Field(None, min_length=1, max_length=100)
    field: str | None = Field(None, min_length=1, max_length=100)
    start_date: datetime | None = None
    end_date: datetime | None = None
    description: str | None = Field(None, max_length=1000)
    order_index: int | None = Field(None, ge=0)

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, v: datetime | None, info) -> datetime | None:
        """Valida que endDate sea posterior a startDate si ambos están presentes."""
        if (
            v is not None
            and "start_date" in info.data
            and info.data["start_date"] is not None
            and v <= info.data["start_date"]
        ):
            raise ValueError("end_date debe ser posterior a start_date")
        return v


class EducationResponse(EducationBase, TimestampMixin):
    """
    Schema de respuesta de formación académica.

    Relaciones:
    - Pertenece a un único Profile
    - Un Profile tiene muchas Education
    """

    id: str

    model_config = ConfigDict(from_attributes=True)
