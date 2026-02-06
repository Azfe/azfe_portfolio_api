from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.common_schema import TimestampMixin


class ToolBase(BaseModel):
    """
    Herramienta de desarrollo utilizada por el usuario.
    Representa IDE, plataformas, servicios, software, etc.
    """

    name: str = Field(
        ..., min_length=1, max_length=50, description="Nombre de la herramienta (no puede estar vacío)"
    )
    category: str = Field(
        ..., min_length=1, max_length=50, description="Tipo de herramienta (IDE, cloud, CI/CD, etc.)"
    )
    order_index: int = Field(
        ...,
        ge=0,
        description="Orden de aparición en el portafolio (debe ser único dentro del perfil)",
    )
    icon_url: str | None = Field(
        None, description="URL del icono o logo de la herramienta (opcional)"
    )


class ToolCreate(ToolBase):
    """
    Schema para crear herramienta.

    Invariantes:
    - name no puede estar vacío
    - category debe ser un valor válido
    - orderIndex debe ser único dentro del perfil
    """

    pass


class ToolUpdate(BaseModel):
    """
    Schema para actualizar herramienta.

    Todos los campos son opcionales, pero name no puede quedar vacío si se actualiza.
    """

    name: str | None = Field(None, min_length=1, max_length=50)
    category: str | None = Field(None, min_length=1, max_length=50)
    icon_url: str | None = None
    order_index: int | None = Field(None, ge=0)


class ToolResponse(ToolBase, TimestampMixin):
    """
    Schema de respuesta de herramienta.

    Relaciones:
    - Pertenece a un único Profile
    - Un Profile tiene muchas Tool

    Invariantes:
    - orderIndex debe ser único dentro del perfil
    """

    id: str

    model_config = ConfigDict(from_attributes=True)
