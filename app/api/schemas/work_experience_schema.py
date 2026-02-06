from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.api.schemas.common_schema import TimestampMixin


class WorkExperienceBase(BaseModel):
    """
    Experiencia laboral dentro del perfil profesional del usuario.
    Incluye información sobre el cargo, empresa, fechas y responsabilidades.
    """

    role: str = Field(
        ..., min_length=1, max_length=100, description="Cargo desempeñado (no puede estar vacío)"
    )
    company: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Empresa donde se trabajó (no puede estar vacía)",
    )
    start_date: datetime = Field(..., description="Fecha de inicio (obligatoria)")
    order_index: int = Field(
        ...,
        ge=0,
        description="Orden de aparición en el CV (debe ser único dentro del perfil)",
    )
    description: str | None = Field(
        None, max_length=2000, description="Resumen de tareas, responsabilidades o logros"
    )
    end_date: datetime | None = Field(
        None, description="Fecha de fin (opcional, None = actualmente trabajando)"
    )
    responsibilities: list[str] = Field(
        default_factory=list, description="Lista de responsabilidades"
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


class WorkExperienceCreate(WorkExperienceBase):
    """
    Schema para crear experiencia laboral.

    Invariantes:
    - role no puede estar vacío
    - company no puede estar vacía
    - startDate es obligatoria
    - Si endDate existe, debe ser posterior a startDate
    - orderIndex debe ser único dentro del perfil
    """

    pass


class WorkExperienceUpdate(BaseModel):
    """
    Schema para actualizar experiencia laboral.

    Todos los campos son opcionales, pero role y company
    no pueden quedar vacíos si se actualizan.
    """

    role: str | None = Field(None, min_length=1, max_length=100)
    company: str | None = Field(None, min_length=1, max_length=100)
    start_date: datetime | None = None
    end_date: datetime | None = None
    description: str | None = Field(None, max_length=2000)
    responsibilities: list[str] | None = None
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


class WorkExperienceResponse(WorkExperienceBase, TimestampMixin):
    """
    Schema de respuesta de experiencia laboral.

    Relaciones:
    - Pertenece a un único Profile
    - Un Profile tiene muchas WorkExperience

    Invariantes:
    - orderIndex debe ser único dentro del mismo perfil
    """

    id: str

    model_config = ConfigDict(from_attributes=True)
