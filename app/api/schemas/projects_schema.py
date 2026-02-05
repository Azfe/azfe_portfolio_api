from pydantic import BaseModel, Field, HttpUrl

from app.api.schemas.common_schema import TimestampMixin


class ProjectBase(BaseModel):
    """
    Proyecto desarrollado por el usuario.
    Representa un proyecto con detalles técnicos, funcionales y enlaces relevantes.
    """

    title: str = Field(
        ..., min_length=1, description="Nombre del proyecto (no puede estar vacío)"
    )
    description: str = Field(
        ..., min_length=1, description="Resumen del proyecto (no puede estar vacío)"
    )
    technologies: list[str] = Field(
        default_factory=list, description="Lista de tecnologías utilizadas"
    )
    repository_url: HttpUrl | None = Field(
        None, description="Enlace al repositorio (GitHub, GitLab, etc.)"
    )
    live_demo_url: HttpUrl | None = Field(
        None, description="Enlace a la demo en vivo (opcional)"
    )
    images: list[str] = Field(
        default_factory=list, description="Lista de URLs de imágenes del proyecto"
    )
    order_index: int = Field(
        ...,
        ge=0,
        description="Orden de aparición en el portafolio (debe ser único dentro del perfil)",
    )


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

    title: str | None = Field(None, min_length=1)
    description: str | None = Field(None, min_length=1)
    technologies: list[str] | None = None
    repository_url: HttpUrl | None = None
    live_demo_url: HttpUrl | None = None
    images: list[str] | None = None
    order_index: int | None = Field(None, ge=0)


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

    class Config:
        from_attributes = True
