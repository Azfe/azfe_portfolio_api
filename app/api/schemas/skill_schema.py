from typing import Literal

from pydantic import BaseModel, Field

from app.api.schemas.common_schema import TimestampMixin

# Niveles de dominio permitidos
SkillLevel = Literal["beginner", "intermediate", "advanced", "expert"]

# Categorías permitidas
SkillCategory = Literal[
    "backend",
    "frontend",
    "devops",
    "database",
    "mobile",
    "cloud",
    "testing",
    "design",
    "other",
]


class SkillBase(BaseModel):
    """
    Habilidad técnica del usuario.
    Representa una tecnología con su nivel de dominio y categoría.
    """

    name: str = Field(
        ..., min_length=1, description="Nombre de la tecnología (no puede estar vacío)"
    )
    level: SkillLevel = Field(
        ..., description="Nivel de dominio (beginner, intermediate, advanced, expert)"
    )
    category: SkillCategory = Field(
        ..., description="Categoría (backend, frontend, devops, etc.)"
    )
    order_index: int = Field(
        ...,
        ge=0,
        description="Orden de aparición en el portafolio (debe ser único dentro del perfil)",
    )


class SkillCreate(SkillBase):
    """
    Schema para crear habilidad técnica.

    Invariantes:
    - name no puede estar vacío
    - level debe ser un valor permitido (beginner, intermediate, advanced, expert)
    - category debe ser un valor permitido
    - orderIndex debe ser único dentro del perfil
    """

    pass


class SkillUpdate(BaseModel):
    """
    Schema para actualizar habilidad técnica.

    Todos los campos son opcionales, pero name no puede quedar vacío si se actualiza.
    """

    name: str | None = Field(None, min_length=1)
    level: SkillLevel | None = None
    category: SkillCategory | None = None
    order_index: int | None = Field(None, ge=0)


class SkillResponse(SkillBase, TimestampMixin):
    """
    Schema de respuesta de habilidad técnica.

    Relaciones:
    - Pertenece a un único Profile
    - Un Profile tiene muchas TechnicalSkill (Skills)
    - Se relaciona conceptualmente con:
      * WorkExperience.technologies (dónde se usó)
      * AdditionalTraining.technologies (dónde se aprendió)
      * Projects.technologies (en qué proyectos)

    Invariantes:
    - orderIndex debe ser único dentro del perfil
    """

    id: str

    class Config:
        from_attributes = True
