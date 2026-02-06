from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.api.schemas.common_schema import TimestampMixin

# Estados válidos de un mensaje
MessageStatus = Literal["pending", "read", "replied"]


class ContactMessageBase(BaseModel):
    """
    Mensaje enviado desde el formulario de contacto del portfolio.
    Representa mensajes de visitantes o potenciales clientes/empleadores.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre del remitente (no puede estar vacío)",
    )
    email: EmailStr = Field(
        ..., description="Correo del remitente (no puede estar vacío)"
    )
    message: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Contenido del mensaje (no puede estar vacío)",
    )


class ContactMessageCreate(ContactMessageBase):
    """
    Schema para crear mensaje de contacto (desde formulario público).

    Nota: created_at y status se generan automáticamente en el servidor.

    Invariantes:
    - name no puede estar vacío
    - email no puede estar vacío y debe ser válido
    - message no puede estar vacío (mínimo 10 caracteres)
    """

    pass


class ContactMessageUpdate(BaseModel):
    """
    Schema para actualizar mensaje (solo admin).

    Normalmente solo se actualizaría para marcar como leído, respondido, etc.
    Los campos del remitente NO deberían modificarse.
    """

    status: MessageStatus | None = None


class ContactMessageResponse(ContactMessageBase, TimestampMixin):
    """
    Schema de respuesta de mensaje de contacto.

    Relaciones:
    - Los mensajes son independientes (no pertenecen a un perfil)

    Invariantes:
    - created_at es obligatorio (generado al crear)
    """

    id: str
    status: MessageStatus = "pending"
    read_at: datetime | None = None
    replied_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
