from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.api.schemas.common_schema import TimestampMixin


class ContactMessageBase(BaseModel):
    """
    Mensaje enviado desde el formulario de contacto del portfolio.
    Representa mensajes de visitantes o potenciales clientes/empleadores.
    """

    name: str = Field(
        ..., min_length=1, description="Nombre del remitente (no puede estar vacío)"
    )
    email: EmailStr = Field(
        ..., description="Correo del remitente (no puede estar vacío)"
    )
    message: str = Field(
        ..., min_length=1, description="Contenido del mensaje (no puede estar vacío)"
    )
    sent_at: datetime = Field(..., description="Fecha y hora del envío (obligatorio)")


class ContactMessageCreate(BaseModel):
    """
    Schema para crear mensaje de contacto (desde formulario público).

    Nota: sent_at se genera automáticamente en el servidor.

    Invariantes:
    - name no puede estar vacío
    - email no puede estar vacío y debe ser válido
    - message no puede estar vacío
    """

    name: str = Field(..., min_length=1)
    email: EmailStr
    message: str = Field(..., min_length=1)


class ContactMessageUpdate(BaseModel):
    """
    Schema para actualizar mensaje (solo admin).

    Normalmente solo se actualizaría para marcar como leído, respondido, etc.
    Los campos del remitente NO deberían modificarse.
    """

    # No se permite actualizar name, email, message, sent_at
    # Solo campos administrativos (implementar según necesidad)
    pass


class ContactMessageResponse(ContactMessageBase, TimestampMixin):
    """
    Schema de respuesta de mensaje de contacto.

    Relaciones:
    - Pertenece a un único Profile
    - Un Profile tiene muchos ContactMessage

    Invariantes:
    - sent_at es obligatorio (generado al crear)
    """

    id: str

    class Config:
        from_attributes = True
