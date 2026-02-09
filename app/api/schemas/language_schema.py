from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.common_schema import TimestampMixin

# Niveles CEFR permitidos
LanguageProficiencyLevel = Literal["a1", "a2", "b1", "b2", "c1", "c2"]


class LanguageBase(BaseModel):
    """
    Idioma del usuario.
    Representa un idioma con su nivel de competencia CEFR.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Nombre del idioma (no puede estar vacío)",
    )
    order_index: int = Field(
        ...,
        ge=0,
        description="Orden de aparición en el portafolio",
    )
    proficiency: LanguageProficiencyLevel | None = Field(
        None, description="Nivel de competencia CEFR (a1, a2, b1, b2, c1, c2)"
    )


class LanguageCreate(LanguageBase):
    """Schema para crear idioma."""

    pass


class LanguageUpdate(BaseModel):
    """Schema para actualizar idioma. Todos los campos son opcionales."""

    name: str | None = Field(None, min_length=1, max_length=50)
    proficiency: LanguageProficiencyLevel | None = None
    order_index: int | None = Field(None, ge=0)


class LanguageResponse(LanguageBase, TimestampMixin):
    """Schema de respuesta de idioma."""

    id: str

    model_config = ConfigDict(from_attributes=True)
