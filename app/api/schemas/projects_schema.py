from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.api.schemas.common_schema import TimestampMixin


class ProjectBase(BaseModel):
    """
    Proyecto desarrollado por el usuario.
    Representa un proyecto con detalles técnicos, funcionales y enlaces relevantes.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre del proyecto (no puede estar vacío)",
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Resumen del proyecto (no puede estar vacío)",
    )
    start_date: datetime = Field(..., description="Fecha de inicio del proyecto")
    order_index: int = Field(
        ...,
        ge=0,
        description="Orden de aparición en el portafolio (debe ser único dentro del perfil)",
    )
    end_date: datetime | None = Field(
        None, description="Fecha de fin (opcional, None = en curso)"
    )
    live_url: str | None = Field(
        None, description="Enlace a la demo en vivo (opcional)"
    )
    repo_url: str | None = Field(
        None, description="Enlace al repositorio (GitHub, GitLab, etc.)"
    )
    technologies: list[str] = Field(
        default_factory=list, description="Lista de tecnologías utilizadas"
    )

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, v: datetime | None, info) -> datetime | None:
        """Valida que end_date sea posterior a start_date si existe."""
        if v is not None and "start_date" in info.data:
            start_date = info.data["start_date"]
            if v <= start_date:
                raise ValueError("end_date debe ser posterior a start_date")
        return v


class ProjectCreate(ProjectBase):
    """
    Schema para crear proyecto.

    Invariantes:
    - title no puede estar vacío
    - description no puede estar vacía
    - orderIndex debe ser único dentro del perfil
    """

    pass


class ProjectUpdate(BaseModel):
    """
    Schema para actualizar proyecto.

    Todos los campos son opcionales, pero title y description
    no pueden quedar vacíos si se actualizan.
    """

    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, min_length=10, max_length=2000)
    start_date: datetime | None = None
    end_date: datetime | None = None
    technologies: list[str] | None = None
    live_url: str | None = None
    repo_url: str | None = None
    order_index: int | None = Field(None, ge=0)

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, v: datetime | None, info) -> datetime | None:
        """Valida que end_date sea posterior a start_date si ambos están presentes."""
        if (
            v is not None
            and "start_date" in info.data
            and info.data["start_date"] is not None
            and v <= info.data["start_date"]
        ):
            raise ValueError("end_date debe ser posterior a start_date")
        return v


class ProjectResponse(ProjectBase, TimestampMixin):
    """
    Schema de respuesta de proyecto.

    Relaciones:
    - Pertenece a un único Profile
    - Un Profile tiene muchos Projects

    Invariantes:
    - orderIndex debe ser único dentro del perfil
    """

    id: str

    model_config = ConfigDict(from_attributes=True)
