from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.common_schema import TimestampMixin

# Niveles de dominio permitidos
ProgrammingLanguageLevel = Literal["basic", "intermediate", "advanced", "expert"]


class ProgrammingLanguageBase(BaseModel):
    """
    Lenguaje de programación del usuario.
    Representa un lenguaje con su nivel de dominio.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Nombre del lenguaje (no puede estar vacío)",
    )
    order_index: int = Field(
        ...,
        ge=0,
        description="Orden de aparición en el portafolio",
    )
    level: ProgrammingLanguageLevel | None = Field(
        None, description="Nivel de dominio (basic, intermediate, advanced, expert)"
    )


class ProgrammingLanguageCreate(ProgrammingLanguageBase):
    """Schema para crear lenguaje de programación."""

    pass


class ProgrammingLanguageUpdate(BaseModel):
    """Schema para actualizar lenguaje de programación. Todos los campos son opcionales."""

    name: str | None = Field(None, min_length=1, max_length=50)
    level: ProgrammingLanguageLevel | None = None
    order_index: int | None = Field(None, ge=0)


class ProgrammingLanguageResponse(ProgrammingLanguageBase, TimestampMixin):
    """Schema de respuesta de lenguaje de programación."""

    id: str

    model_config = ConfigDict(from_attributes=True)
