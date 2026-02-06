from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.common_schema import TimestampMixin

# Niveles de dominio permitidos
SkillLevel = Literal["basic", "intermediate", "advanced", "expert"]


class SkillBase(BaseModel):
    """
    Habilidad técnica del usuario.
    Representa una tecnología con su nivel de dominio y categoría.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Nombre de la tecnología (no puede estar vacío)",
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Categoría (backend, frontend, devops, etc.)",
    )
    order_index: int = Field(
        ...,
        ge=0,
        description="Orden de aparición en el portafolio (debe ser único dentro del perfil)",
    )
    level: SkillLevel | None = Field(
        None, description="Nivel de dominio (basic, intermediate, advanced, expert)"
    )


class SkillCreate(SkillBase):
    """
    Schema para crear habilidad técnica.

    Invariantes:
    - name no puede estar vacío
    - category no puede estar vacía
    - orderIndex debe ser único dentro del perfil
    """

    pass


class SkillUpdate(BaseModel):
    """
    Schema para actualizar habilidad técnica.

    Todos los campos son opcionales, pero name no puede quedar vacío si se actualiza.
    """

    name: str | None = Field(None, min_length=1, max_length=50)
    category: str | None = Field(None, min_length=1, max_length=50)
    level: SkillLevel | None = None
    order_index: int | None = Field(None, ge=0)


class SkillResponse(SkillBase, TimestampMixin):
    """
    Schema de respuesta de habilidad técnica.

    Relaciones:
    - Pertenece a un único Profile
    - Un Profile tiene muchas TechnicalSkill (Skills)

    Invariantes:
    - orderIndex debe ser único dentro del perfil
    """

    id: str

    model_config = ConfigDict(from_attributes=True)
