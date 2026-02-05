from typing import Literal

from pydantic import BaseModel, Field

from app.api.schemas.common_schema import TimestampMixin

# Niveles de conocimiento permitidos (opcional)
ToolKnowledgeLevel = Literal["basic", "intermediate", "advanced", "expert"]

# Categorías de herramientas permitidas
ToolCategory = Literal[
    "ide",
    "cloud",
    "ci_cd",
    "design",
    "project_management",
    "communication",
    "version_control",
    "database_tools",
    "testing_tools",
    "monitoring",
    "containerization",
    "other",
]


class ToolBase(BaseModel):
    """
    Herramienta de desarrollo utilizada por el usuario.
    Representa IDE, plataformas, servicios, software, etc.
    """

    name: str = Field(
        ..., min_length=1, description="Nombre de la herramienta (no puede estar vacío)"
    )
    category: ToolCategory = Field(
        ..., description="Tipo de herramienta (IDE, cloud, CI/CD, etc.)"
    )
    knowledge_level: ToolKnowledgeLevel | None = Field(
        None, description="Nivel de conocimiento (opcional)"
    )
    order_index: int = Field(
        ...,
        ge=0,
        description="Orden de aparición en el portafolio (debe ser único dentro del perfil)",
    )


class ToolCreate(ToolBase):
    """
    Schema para crear herramienta.

    Invariantes:
    - name no puede estar vacío
    - category debe ser un valor permitido
    - orderIndex debe ser único dentro del perfil
    """

    pass


class ToolUpdate(BaseModel):
    """
    Schema para actualizar herramienta.

    Todos los campos son opcionales, pero name no puede quedar vacío si se actualiza.
    """

    name: str | None = Field(None, min_length=1)
    category: ToolCategory | None = None
    knowledge_level: ToolKnowledgeLevel | None = None
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

    class Config:
        from_attributes = True
